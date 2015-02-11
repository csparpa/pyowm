#!/usr/bin/env python

import requests, re, codecs, json

city_list_url = 'http://openweathermap.org/help/city_list.txt'
city_list = "city_list.txt"
csv_city_list = "city_list.csv"
ordered_csv_city_list = "city_list.ordered.csv"


"""
This script is used to retrieve the city IDs list from the OWM web 2.5 API
and then to divide the list into smaller chunks: each chunk is ordered by
city ID and written to a separate file
"""

def download_the_file():
    print 'Downloading file '+city_list_url+' ...'
    resp = requests.get(city_list_url)
    with codecs.open(city_list, "w", "utf-8") as f:
        f.write(resp.text)
    print '  ... done'


def make_it_a_hsv():
    print 'Parsing file to hsv ...'
    header_out = False
    with codecs.open(city_list, "r", "utf-8") as i:
        with codecs.open(csv_city_list, "w", "utf-8") as o:
            for line in i:
                newline = re.sub(r"\t", "#", line)
                if header_out:
                    o.write(newline)
                header_out = True
    print '  ... done'


def extract_keyset():
    print 'Ordering csv lines by city ID ...'
    lines = []
    with codecs.open(csv_city_list, "r", "utf-8") as f:
        for line in f.readlines():
            fields = line.split("\n")[0].split("#")
            id = fields[0]
            name = re.sub(r",", " ", fields[1]).lower()
            if name != "":
                lines.append([name, ","+id+","+",".join(fields[2:])])
    print '  ... done'
    return {l[0]: l[1] for l in lines}


def split_keyset(keyset):
    print 'Splitting keyset of %d city names into 4 subsets based on the initial letter:' % (len(keyset),)
    print '-> from "a" = ASCII 97  to "f" = ASCII 102'
    print '-> from "g" = ASCII 103 to "l" = ASCII 108'
    print '-> from "m" = ASCII 109 to "r" = ASCII 114'
    print '-> from "s" = ASCII 115 to "z" = ASCII 122'
    ss = [dict(), dict(), dict(), dict()]
    for name in keyset:
        c = ord(name[0])
        if c < 97: # not a letter
            continue
        elif c in range(97, 103):  # from a to f
            ss[0][name] = keyset[name]
            continue
        elif c in range(103, 109): # from g to l
            ss[1][name] = keyset[name]
            continue
        elif c in range(109, 115): # from m to r
            ss[2][name] = keyset[name]
            continue
        elif c in range (115, 123): # from s to z
            ss[3][name] = keyset[name]
            continue
        else:
            continue # not a letter
    print '  ... done'
    return ss


def write_subsets_to_files(ssets):
    print 'Ordering subsets and writing subsets into files:'
    with codecs.open("097-102.txt", "w", "utf-8") as f:
        for name in sorted(ssets[0].iterkeys()):
            f.write(name+ssets[0][name]+"\n")
    with codecs.open("103-108.txt", "w", "utf-8") as f:
        for name in sorted(ssets[1].iterkeys()):
            f.write(name+ssets[1][name]+"\n")
    with codecs.open("109-114.txt", "w", "utf-8") as f:
        for name in sorted(ssets[2].iterkeys()):
            f.write(name+ssets[2][name]+"\n")
    with codecs.open("115-122.txt", "w", "utf-8") as f:
        for name in sorted(ssets[3].iterkeys()):
            f.write(name+ssets[3][name]+"\n")
    print '  ... done'


if __name__ == '__main__':
    print 'Job started'
    download_the_file()
    make_it_a_hsv()
    keyset = extract_keyset()
    ssets = split_keyset(keyset)
    write_subsets_to_files(ssets)
    print 'Job finished'

