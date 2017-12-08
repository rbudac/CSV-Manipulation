#!/usr/bin/env python3

import operator
#from datetime import datetime
#import json
import os
import re
import argparse
import csv
#import copy
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
                    if args.data == "hashtags" or args.data == "urls" or args.data == "mentions":
                        line = line.lower()
                        if b'na' in line and line in b'na':
                            continue
                        if b';' in line:
                            multi_tags = line.split(b';')
                            for tag in multi_tags:
                                total_items += 1
                                try:
                                    items[tag]
                                except KeyError:
                                    items[tag] = 1
                                else:
                                    items[tag] += 1
                            continue
                    total_items += 1
                    try:
                        items[line]
                    except KeyError:
                        items[line] = 1
                    else:
                        items[line] += 1

    label1 = b'(Total Occurences)'    
    if args.data == "screen_name":
        label1 = b'(Total Tweets)'
    elif args.data == "mentions":
        label1 = b'(Total Mentions)'
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
 
    label1 = b'(Other)'
   
    if args.data == "screen_name":
        label1 = b'(Everyone Else)'
    elif args.data == "hashtags":
        label1 = b'(Other Hashtags)'
    elif args.data == "urls":
        label1 = b'(Other URLs)'
    elif args.data == "mentions":
        label1 = b'(Other Mentions)'

    short_list = [(label1, rest)] + short_list

    return short_list
  
# Outputs the list of items to csv, adding headers
def output_csv(args, list):
    header1 = "x"
    header2 = "# of Occurrences"
    if args.data == "screen_name":
        header1 = "Tweeter"
        header2 = "# of Tweets"
    elif args.data == "hashtags":
        header1 = "Hashtag"
    elif args.data == "urls":
        header1 = "URL"
    elif args.data == "mentions":
        header1 = "Twitter User"
        header2 = "# of Times Mentioned"
    with open(args.output, 'w+', encoding="utf-8") as output:
        print("Opened", args.output)
        csv_writer = csv.writer(output, dialect=args.dialect)
        csv_writer.writerow([header1, header2])
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
    parser.add_argument("-data", default="screen_name", help="What tweet data to check the frequency of. Defaults to screen_name.")
    parser.add_argument("-dialect", default="excel", help="Sets dialect for csv output. Defaults to excel. See python module csv.list_dialects()")
    parser.add_argument("-encoding", default="utf-8", help="Sets character encoding for json files. Defaults to 'utf-8'.")
    parser.add_argument("-top", default=1000, help="Returns only the top [x]. Defaults to 1000")
    args = parser.parse_args()

    args.output += ".csv"
    if not args.path.endswith("/"):
        args.path += "/"

    list = parse(args)
    sorted_list = sort_list(list)
    output_csv(args, sorted_list)
