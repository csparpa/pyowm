#!/usr/bin/env python

import requests, sys, os, codecs, json, gzip, collections

city_list_url = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
us_city_list_url = 'http://bulk.openweathermap.org/sample/city.list.us.json.gz'
city_list_gz = "city.list.json.gz"
us_city_list_gz = "city.list.us.json.gz"
csv_city_list = "city_list.csv"
us_csv_city_list = "us_city_list.csv"
ordered_csv_city_list = "city_list.ordered.csv"


"""
This script is used to retrieve the city IDs list from the OWM web 2.5 API
and then to divide the list into smaller chunks: each chunk is ordered by
city ID and written to a separate file

URLs of source files:
  http://bulk.openweathermap.org/sample/city.list.json.gz
  http://bulk.openweathermap.org/sample/city.list.us.json.gz
"""

def download_the_files():
    print 'Downloading file '+city_list_url+' ...'
    with open(city_list_gz, 'wb') as h:
        response = requests.get(city_list_url, stream=True)
        for block in response.iter_content(1024):
            h.write(block)

    print 'Downloading file '+us_city_list_url+' ...'
    with open(us_city_list_gz, 'wb') as g:
        response = requests.get(us_city_list_url, stream=True)
        for block in response.iter_content(1024):
            g.write(block)

    print '  ... done'


def read_all_cities_into_dict():
    print 'Reading city data from files ...'
    all_cities = dict()

    # All cities
    with gzip.open(city_list_gz, "rb", "utf-8") as i:
        cities = i.readlines()
        for city in cities:
            # eg. {"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
            city_dict = json.loads(city)
            if city_dict['_id'] in all_cities:
                print 'Warning: city ID %d was already processed! Data chunk is: %s' % (city_dict['_id'], city_dict)
                continue
            else:
                all_cities[city_dict['_id']] = dict(name=city_dict['name'],
                                                    country=city_dict['country'],
                                                    lon=city_dict['coord']['lon'],
                                                    lat=city_dict['coord']['lat'])

    # US cities
    with gzip.open(us_city_list_gz, "rb", "utf-8") as f:
        cities = f.readlines()
        for city in cities:
            # eg. {"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
            city_dict = json.loads(city)
            if city_dict['_id'] in all_cities:
                print 'Warning: city ID %d was already processed! Data chunk is: %s' % (city_dict['_id'], city_dict)
                continue
            else:
                all_cities[city_dict['_id']] = dict(name=city_dict['name'],
                                                    country=city_dict['country'],
                                                    lon=city_dict['coord']['lon'],
                                                    lat=city_dict['coord']['lat'])

    print '... done'
    return all_cities


def order_dict_by_city_id(all_cities):
    print 'Ordering city dict by city ID ...'
    all_cities_ordered = collections.OrderedDict(sorted(all_cities.items()))
    print '... done'
    return all_cities_ordered


def city_to_string(city_id, city_dict):
    return ','.join([city_dict['name'], str(city_id), str(city_dict['lat']), str(city_dict['lon']),
                     city_dict['country']])

def split_keyset(cities_dict):
    print 'Splitting keyset of %d city names into 4 subsets based on the initial letter:' % (len(cities_dict),)
    print '-> from "a" = ASCII 97  to "f" = ASCII 102'
    print '-> from "g" = ASCII 103 to "l" = ASCII 108'
    print '-> from "m" = ASCII 109 to "r" = ASCII 114'
    print '-> from "s" = ASCII 115 to "z" = ASCII 122'
    ss = [list(), list(), list(), list()]
    for city_id in cities_dict:
        name = cities_dict[city_id]['name'].lower()
        if not name:
            continue
        c = ord(name[0])
        if c < 97: # not a letter
            continue
        elif c in range(97, 103):  # from a to f
            ss[0].append(city_to_string(city_id, cities_dict[city_id]))
            continue
        elif c in range(103, 109): # from g to l
            ss[1].append(city_to_string(city_id, cities_dict[city_id]))
            continue
        elif c in range(109, 115): # from m to r
            ss[2].append(city_to_string(city_id, cities_dict[city_id]))
            continue
        elif c in range (115, 123): # from s to z
            ss[3].append(city_to_string(city_id, cities_dict[city_id]))
            continue
        else:
            continue # not a letter
    print '... done'
    return ss


def write_subsets_to_files(ssets, outdir):
    print 'Writing subsets to files ...'
    with codecs.open("%s%s097-102.txt" % (outdir, os.sep),
                     "w", "utf-8") as f:
        for city_string in sorted(ssets[0]):
            f.write(city_string+"\n")
    with codecs.open("%s%s103-108.txt" % (outdir, os.sep),
                     "w", "utf-8") as f:
        for city_string in sorted(ssets[1]):
            f.write(city_string+"\n")
    with codecs.open("%s%s109-114.txt" % (outdir, os.sep),
                     "w", "utf-8") as f:
        for city_string in sorted(ssets[2]):
            f.write(city_string+"\n")
    with codecs.open("%s%s115-122.txt" % (outdir, os.sep),
                     "w", "utf-8") as f:
        for city_string in sorted(ssets[3]):
            f.write(city_string+"\n")
    print '... done'


if __name__ == '__main__':
    target_folder = os.path.abspath(sys.argv[1])
    print 'Will save output files to folder: %s' % (target_folder,)
    print 'Job started'
    download_the_files()
    cities = read_all_cities_into_dict()
    ordered_cities = order_dict_by_city_id(cities)
    ssets = split_keyset(ordered_cities)
    write_subsets_to_files(ssets, target_folder)
    print 'Job finished'

