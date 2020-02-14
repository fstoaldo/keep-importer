#!/usr/bin/env python

import json

# Owned
__author__ = "fstoaldo"
__maintainer__ = "fstoaldo"
__email__ = "fstoaldo@gmail.com"


class Note:
    """Note class to hold google keep json data and
        with methods to export as plain-text .txt files"""

    def __init__(self, json_file):
        """Constructs a new Note object
            :return None if json_file passed in was invalid"""
        try:
            with open(json_file, encoding="utf-8") as f:
                self.data = json.load(f)
        except json.JSONDecodeError:
            print("--> INVALID JSON - FILE: <{}>".format(json_file.name))

        self.txt_note = open(json_file.name.replace(".json", ".txt"), "w+", encoding="utf-8")

    def make_note(self):
        """Creates a new plain text note from a json file"""
        # write the title of the note as the header if present
        self._write_header()
        # write the contents of the note
        self._write_contents()
        # write footer
        self._write_footer()

        return self.txt_note

    """Helper methods to new_note defined below"""

    def _write_header(self):
        """Writes the header of the note"""
        if "title" in self.data:
            if self.data["title"] != "":
                self.txt_note.write(self.data["title"] + "\n\n")

    def _write_footer(self):
        """Write footer into new note file"""
        if "labels" in self.data:
            self.txt_note.write("\n\nTags (from Google Keep):\n\t")
            for label in self.data["labels"]:
                if label["name"] != "":
                    self.txt_note.write(label["name"] + ",")

    def _write_contents(self):
        """Write contents from data file into new note file"""
        # handle annotations (rich links)
        if "annotations" in self.data:
            self._write_annotations()

        elif "listContent" in self.data:
            self._write_list()

        elif "textContent" in self.data:
            self._write_text()

        else:
            self.txt_note.write("<<NO NOTES HAVE BEEN FOUND>>")

    """Helper methods to private method _write contents defined below"""

    def _write_annotations(self):
        """Handles annotations (rich links)"""
        self.txt_note.write("ANNOTATIONS\n===========\n")
        for item in self.data["annotations"]:
            self.txt_note.write("TITLE: " + item["title"] + "\n")
            self.txt_note.write("SOURCE: " + item["url"] + "\n")
            self.txt_note.write("DESCRIPTION: " + item["description"] + "\n--------\n")

    def _write_list(self):
        """Handles lists"""
        for item in self.data["listContent"]:
            if item["isChecked"]:
                self.txt_note.write("[X]" + item["text"] + "\n")
            else:
                self.txt_note.write("[]" + item["text"] + "\n")

    def _write_text(self):
        """Handles text notes"""
        self.txt_note.write(self.data["textContent"])
