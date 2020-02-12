#!/usr/bin/env python

import os
import json
import src.note as note

# Owned
__author__ = "fstoaldo"
__maintainer__ = "fstoaldo"
__email__ = "fstoaldo@gmail.com"

"""keep_importer.py: this script aims to read JSON files imported from Google Keep and transform them to
    plain-text format, to facilitate backup and make it easier to import to other note taking apps"""


def open_json(json_file):
    """Opens a new json file
        :param json_file
        :return data contained in json_file"""

    with open(json_file, encoding="utf-8") as f:
        return json.load(f)


def write_header(file, data):
    """Writes the header of the note
        :param file: note file
        :param data: data source from json file
        :return file with the header written on it"""

    if "title" in data:
        if data["title"] != "":
            file.write(data["title"] + "\n\n")

    return file


def write_contents(file, data):
    """Write contents from data file into new note file
        :param file: note file
        :param data: data source from json file
        :return file with the contents written on it"""

    # handle annotations (rich links)
    if "annotations" in data:
        file.write("ANNOTATIONS\n===========\n")
        for item in data["annotations"]:
            file.write("TITLE: " + item["title"] + "\n")
            file.write("SOURCE: " + item["url"] + "\n")
            file.write("DESCRIPTION: " + item["description"] + "\n--------\n")

    elif "listContent" in data:
        # checklist
        for item in data["listContent"]:
            if item["isChecked"]:
                file.write("[X]" + item["text"] + "\n")
            else:
                file.write("[]" + item["text"] + "\n")

    elif "textContent" in data:
        file.write(data["textContent"])

    return file


def write_footer(file, data):
    """Write footer  into new note file
        :param file: note file
        :param data: data source from json file
        :return file with the footer written on it"""

    if "labels" in data:
        file.write("\n\n Tags (from Google Keep):\n\t")
        for label in data["labels"]:
            file.write(label["name"] + ",")

    return file


def new_note(json_file):
    """Creates a new plain text note from a json file
        :param json_file: a google keep json file note"""

    # open json file and get its data
    data = open_json(json_file)
    # create a new txt file to paste the notes into only if the required fields are present
    if "listContent" in data or "textContent" in data:
        new_file = open(json_file.name.replace(".json", ".txt"), "w+")
        # write the title of the note as the header if present
        new_file = write_header(new_file, data)
        # write the contents of the note
        new_file = write_contents(new_file, data)
        # write footer
        new_file = write_footer(new_file, data)
    else:
        print("Could not import file <{}>: 'listContent' or"
              "'textContent' fields missing".format(json_file.name))


def open_json_directory(path):
    """Opens up a directory containing json files to import
        :param path of the directory to open"""

    # open the directory and loop through files
    for file in os.scandir(path):
        if file.path.endswith(".json") and file.is_file():
            # found a json file, try to import it
            print("IMPORTING: {}".format(file.name))
            new_note(file)


def main():
    """Driver function"""
    # get directory with json files from user
    # direc = input("ENTER THE DIRECTORY WITH JSON FILES: ")
    direc = "../data/test"
    # creates new directory to store new notes
    if not os.path.exists("../plain_text_files"):
        os.mkdir("../plain_text_files")

    os.chdir("../plain_text_files")
    # call function to handle json files in the directory
    open_json_directory(direc)


if __name__ == '__main__':
    main()
