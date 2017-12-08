#!/usr/bin/env python3

import operator
import os
import re
import argparse
import csv
import sys

# Parse the input files and create an associative array of frequencies for each item
def parse(args):
    items = {}
    total_items = 0
    ids = []
    entry = {'user:screen_name':'', 'user:name':'', 'user:description':'', 'user:profile_image_url_https':''}
    with open(args.userids) as userids:
        for line in userids:
            line = line.strip()
            if line == "":
                continue
            ids.append(line)

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
                        for id in ids:
                            if id in row['user:id_str']:
                                if dict_diff(entry, row):
                                    writer.writerow(row)
                                entry = row


def dict_diff(dict1, dict2):
    if dict1['user:screen_name'] != dict2['user:screen_name']:
        return True
    elif dict1['user:name'] != dict2['user:name']:
        return True
    elif dict1['user:description'] != dict2['user:description']:
        return True
    elif dict1['user:profile_image_url_https'] != dict2['user:profile_image_url_https']:
        return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extracts attributes from tweets.')
    parser.add_argument("-string", default="", help="Regular expression for files to parse. Defaults to empty string.")
    parser.add_argument("-path", default="./", help="Optional path to folder containing tweets. Defaults to current folder.")
    parser.add_argument("-output", default="output", help="Optional file to output results. Defaults to output.")
    parser.add_argument("-data", default="screen_name", help="What tweet data to check the frequency of. Defaults to screen_name.")
    parser.add_argument("-dialect", default="excel", help="Sets dialect for csv output. Defaults to excel. See python module csv.list_dialects()")
    parser.add_argument("-encoding", default="utf-8", help="Sets character encoding for json files. Defaults to 'utf-8'.")
    parser.add_argument("-top", default=1000, help="Returns only the top [x]. Defaults to 1000")
    parser.add_argument("-userids", default="", help="Points to file of userids that you want to keep")
    args = parser.parse_args()

    args.output += ".csv"
    if not args.path.endswith("/"):
        args.path += "/"

    list = parse(args)
