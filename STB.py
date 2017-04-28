#!/usr/bin/python3

from util import xFile
import json


class STB:
    class STBLabel:
        def __init__(self, bank_id, sound_count, start_offset, sounds_ids = {}):
            self.bank_id = bank_id
            self.sound_count = sound_count
            self.start_offset = start_offset
            self.sound_ids = sounds_ids

        def get_table(self):
            return self.__str__()

        def __str__(self):
            return json.dump(self.sound_ids, indent=4)

        def __dict__(self):
            return dict(bank_id=self.bank_id, sound_ids=self.sound_ids)

    def read_from_json(self, json_file):
        """Import data from a JSON file."""
        self.raw_json = json.loads(open(json_file, 'r').read())
        self.labels = {}
        next_offset = 0
        for key, val in self.raw_json.items():
            if val["bank_id"] != -1:
                current_offset = next_offset
                next_offset += len(val["sound_ids"]) * 4
            else:
                current_offset = 0
            self.labels[key] = self.STBLabel(val["bank_id"], len(val["sound_ids"]), current_offset, val["sound_ids"])
        print(self.labels)

    def read_from_file(self, file):
        """Import data from a binary STB file."""
        self.file = xFile(file)
        self.parse_header()
        self.parse_labels()
        self.parse_label_tables()

    def parse_header(self):
        """Verify and parse the header of the sound table binary file."""
        self.file.seek(0)
        if self.file.read(3) != b"STB":
            self.file.close()
            return False
        self.file.seek(4)
        self.table_count = self.file.read_int()
        self.label_count = self.file.read_int()
        self.label_table_start_offset = self.file.read_int()
        return True

    def parse_labels(self):
        """Read the NUS3Bank IDs, sound count, and offsets for each label."""
        self.labels = {}
        for i in range(self.label_count):
            self.file.seek((i + 1) * 0x10)
            bank_id = self.file.read_int()
            sound_count = self.file.read_int()
            start_offset = self.file.read_int()
            self.labels[i] = self.STBLabel(bank_id, sound_count, start_offset)

    def parse_label_tables(self):
        """Read the sound ID tables for each label."""
        for label in self.labels:
            self.file.seek(0x10 + self.label_table_start_offset + self.labels[label].start_offset)
            for i in range(self.labels[label].sound_count):
                self.labels[label].sound_ids[i] = self.file.read_int()

    def label_to_json(self, label):
        """Serialize as a JSON object."""
        if isinstance(label, self.STBLabel):
            return label.__dict__()

    def export_tables_to_json(self, outfile):
        """Write the current data out as a JSON file."""
        out = open(outfile, 'w')
        json.dump(self.labels, out, indent=4, default=self.label_to_json)
        out.close()

    def export_tables_to_file(self, outfile):
        """Write the current data out as an STB binary file."""
        out = xFile(outfile, 'wb')
        out.write(b"STB\x00")
        out.write_int(1)
        out.write_int(len(self.labels))
        out.write_int(len(self.labels) * 0x10)
        for label in self.labels:
            out.write_int(self.labels[label].bank_id)
            out.write_int(len(self.labels[label].sound_ids))
            out.write_int(self.labels[label].start_offset)
            out.write_int(0)

        for label in self.labels:
            for key, val in self.labels[label].sound_ids.items():
                out.write_int(val)
        out.close()