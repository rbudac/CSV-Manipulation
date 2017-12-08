#!/usr/bin/env python3

import operator
import os
import re
import argparse
import csv
import sys

def parse(args):
# Parse the input files and remove rows that contain certain values.

    for filename in os.listdir(args.path):
        if re.search(args.string, filename) and ".csv" in filename:
            print("parsing", filename)
            with open(args.path + filename) as csvfile:
                reader = csv.DictReader(csvfile)
                fieldnames = reader.fieldnames
                with open(args.output, 'w+', encoding="utf-8") as outcsvfile:
                    writer = csv.DictWriter(outcsvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in reader:
                        if args.special:
                            if (row[args.row] != '123456789'): # Fake ID. Put in actual Twitter IDs here.
                                writer.writerow(row)
                        else:
                            if row[args.row] == args.data:
                                writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extracts attributes from tweets.')
    parser.add_argument("-string", default="", help="Regular expression for files to parse. Defaults to empty string.")
    parser.add_argument("-path", default="./", help="Optional path to folder containing tweets. Defaults to current folder.")
    parser.add_argument("-output", default="output", help="Optional file to output results. Defaults to output.")
    parser.add_argument("-row", default="", help="What tweet data to check the status of.")
    parser.add_argument("-data", default="NA", help="What values for the data field should constitute removing the row from the csv file. Defaults to NA.")
    parser.add_argument("-dialect", default="excel", help="Sets dialect for csv output. Defaults to excel. See python module csv.list_dialects()")
    parser.add_argument("-encoding", default="utf-8", help="Sets character encoding for json files. Defaults to 'utf-8'.")
    parser.add_argument("-special", default=False, help="A hack for bot removal. If true, remove hardcoded bot IDs.")
    args = parser.parse_args()

    args.output += ".csv"
    if not args.path.endswith("/"):
        args.path += "/"
    list = parse(args)
