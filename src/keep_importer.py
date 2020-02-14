#!/usr/bin/env python

import os
import src.note as note

# Owned
__author__ = "fstoaldo"
__maintainer__ = "fstoaldo"
__email__ = "fstoaldo@gmail.com"

"""keep_importer.py: this script aims to read JSON files imported from Google Keep and transform them to
    plain-text format, to facilitate backup and make it easier to import to other note taking apps"""


def open_json_directory(path):
    """Scans a directory searching for json files to import
        :param path of the directory to open"""

    file_count = 0
    json_count = 0
    success_count = 0

    # open the directory and loop through files
    for file in os.scandir(path):
        file_count += 1
        # os.stat -> checks if file size is 0 (empty file)
        if file.path.endswith(".json") and file.is_file() and os.stat(file).st_size > 0:
            json_count += 1
            # found a json file, try to import it
            print("IMPORTING: {}".format(file.name))
            # new Note object
            n = note.Note(file)
            # check if object returned was loaded correctly (hasn't raised exceptions), so it has the "data" attribute
            if hasattr(n, "data"):
                success_count += 1
                # create a new txt file from it
                n.make_note()

    print("NUMBER OF FILES IN DIRECTORY {}: ".format(file_count))
    print("NUMBER OF JSON FILES IN DIRECTORY: {}".format(json_count))


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
