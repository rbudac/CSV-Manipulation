#!/usr/bin/env python3

import operator
from datetime import datetime
import json
import os
import re
import argparse
import csv
import copy
import sys

# Parse the input files and create an associative array of frequencies for each item
def parse(args):
    items = {}
    total_items = 0

    for filename in os.listdir(args.path):
        if re.search(args.string, filename) and ".csv" in filename:
            f = open
            print("parsing", filename)
            with f(args.path + filename, 'rb') as data_file:
                for line in data_file:
                    line = line.strip()
                    if line == "":
                        continue
                    line = line.lower()
                    if b';' in line:
                        check1 = args.hashtag + ';'
                        check1 = check1.encode(args.encoding)
                        check2 = ';' + args.hashtag
                        check2 = check2.encode(args.encoding)
                        if (check1 in line) or (check2 in line):
                            multi_tags = line.split(b';')
                            for tag in multi_tags:
                                hashtag_bytes = args.hashtag.encode(args.encoding)
                                if not (tag in hashtag_bytes and hashtag_bytes in tag):
                                    total_items += 1
                                    try:
                                        items[tag]
                                    except KeyError:
                                        items[tag] = 1
                                    else:
                                        items[tag] += 1
    label1 = b'(Total Occurences)'
    items[label1] = total_items
    return items

# Sort the list by most frequent to least.
# Also collapses any items that don't make the top cut into an "other" category.
def sort_list(list):

    sorted_list = sorted(list.items(), key=operator.itemgetter(1), reverse=True)

    i = 0
    rest = 0
    short_list = []
    for item in sorted_list:
        i += 1
        if i <= int(args.top) + 1:
            short_list.append(item)
        else:
            rest += item[1]
   
    label1 = b'(Other Hashtags)'
    short_list = [(label1, rest)] + short_list

    return short_list

# Outputs the list of items to csv, adding headers
def output_csv(args, list):
    heading1 = "Hashtag"
    heading2 = "# of concurences with " + args.hashtag

    with open(args.output, 'w+', encoding="utf-8") as output:
        print("Opened", args.output)
        csv_writer = csv.writer(output, dialect=args.dialect)
        csv_writer.writerow([heading1, heading2])
        count = 0

        for item in list:

            #Write this tweet to csv.
            item = [item[0].decode("utf-8"), item[1]]
            csv_writer.writerow(item)
            count += 1

        print("Recorded {} items.".format(count))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extracts attributes from tweets.')
    parser.add_argument("-string", default="", help="Regular expression for files to parse. Defaults to empty string.")
    parser.add_argument("-path", default="./", help="Optional path to folder containing tweets. Defaults to current folder.")
    parser.add_argument("-output", default="output", help="Optional file to output results. Defaults to output.")
    parser.add_argument("-hashtag", default="", help="Which hashtag to check against other hashtags.")
    parser.add_argument("-dialect", default="excel", help="Sets dialect for csv output. Defaults to excel. See python module csv.list_dialects()")
    parser.add_argument("-encoding", default="utf-8", help="Sets character encoding for json files. Defaults to 'utf-8'.")
    parser.add_argument("-top", default=1000, help="Returns only the top [x]. Defaults to 1000")
    args = parser.parse_args()

    args.output += ".csv"
    if not args.path.endswith("/"):
        args.path += "/"

    """Iterates over entries in path."""

    hashtags = parse(args)
    sorted_hash = sort_list(hashtags)
    output_csv(args, sorted_hash)
