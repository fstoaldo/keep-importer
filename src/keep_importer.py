#!/usr/bin/env python

import os

import tkinter
from tkinter import filedialog
from ctypes import windll

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
            success_count += json_to_txt(file)

    print("\nSUMMARY\nFILES IN DIRECTORY: {}".format(file_count))
    print("JSON FILES IN DIRECTORY: {}".format(json_count))
    print("JSON FILES NOT EXPORTED: {}".format(json_count - success_count))
    print("JSON NOTES EXPORTED: {}".format(success_count))


def json_to_txt(json_file):
    """Handles json_files to create a new plain text note from it
        :param json_file
        :return 1 if json was converted. 0 if json wasn't converted"""

    # found a json file, try to import it
    print(json_file.name, end="...")
    # new Note object
    n = note.Note(json_file)
    # check if object returned was loaded correctly (hasn't raised exceptions), so it has the "data" attribute
    if hasattr(n, "data"):
        # create a new txt file from it
        n.make_note()
        print("OK")
        return 1

    return 0


def select_dir():
    """Directory selection popup window using tkinter"""

    # display window correctly with high DPI
    windll.shcore.SetProcessDpiAwareness(1)
    # new instance of tkinter
    window = tkinter.Tk()
    # avoids window from popping up
    window.withdraw()
    # selects folder and returns it
    return filedialog.askdirectory()


def main():
    """Driver function"""

    path = select_dir()

    # creates new directory to store new notes
    new_dir = path + "/plain_text_files"
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    os.chdir(new_dir)

    # call function to handle json files in the directory
    open_json_directory(path)

    # in the end, prompts user to open path with exported notes
    ans = input("> Open folder with exported notes? [y/N] ")
    if ans.lower() == "y":
        os.startfile(os.path.realpath(new_dir))


if __name__ == '__main__':
    main()
