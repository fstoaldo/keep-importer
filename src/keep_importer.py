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

    # open the directory and loop through files
    for file in os.scandir(path):
        if file.path.endswith(".json") and file.is_file():
            # found a json file, try to import it
            print("IMPORTING: {}".format(file.name))
            # new Note object
            n = note.Note(file)
            # create a new txt file from it
            n.make_note()


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
