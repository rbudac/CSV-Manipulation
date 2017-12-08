#!/usr/bin/env python3

import operator
import os
import re
import argparse
import csv
import sys

def parse(args):
# Parse the input files and only keeps the column that is specified by
# the "-row" command line argument. (Yes, it should be a "-column" command
# line argument, but it is not.)

    for filename in os.listdir(args.path):
        if re.search(args.string, filename) and ".csv" in filename:
            print("parsing", filename)
            with open(args.path + filename) as csvfile:
                reader = csv.DictReader(csvfile)
                fieldnames = reader.fieldnames
                with open(args.output, 'w+', encoding="utf-8") as outfile:
                    for row in reader:
                        outfile.write(row[args.row])
                        outfile.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extracts attributes from tweets.')
    parser.add_argument("-string", default="", help="Regular expression for files to parse. Defaults to empty string.")
    parser.add_argument("-path", default="./", help="Optional path to folder containing tweets. Defaults to current folder.")
    parser.add_argument("-output", default="output", help="Optional file to output results. Defaults to output.")
    parser.add_argument("-row", default="", help="Which row of the csv to output as raw text.")
    parser.add_argument("-dialect", default="excel", help="Sets dialect for csv output. Defaults to excel. See python module csv.list_dialects()")
    parser.add_argument("-encoding", default="utf-8", help="Sets character encoding for json files. Defaults to 'utf-8'.")
    args = parser.parse_args()

    args.output += ".txt"
    if not args.path.endswith("/"):
        args.path += "/"
    list = parse(args)
