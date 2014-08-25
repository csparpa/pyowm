import requests, re, codecs, collections

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


def make_it_a_csv():
    print 'Parsing file to csv ...'
    header_out = False
    with codecs.open(city_list, "r", "utf-8") as i:
        with codecs.open(csv_city_list, "w", "utf-8") as o:
            for line in i:
                newline = re.sub(r"\t", ",", line)
                if header_out:
                    o.write(newline)
                header_out = True
    print '  ... done'


def extract_keyset():
    print 'Ordering csv lines by city ID ...'
    lines = []
    with codecs.open(csv_city_list, "r", "utf-8") as f:
        for line in f.readlines():
            fields = line.split("\n")[0].split(",")
            id = long(fields[0])
            lines.append([id, ","+",".join(fields[1:])])
    print '  ... done'
    return {l[0]: l[1] for l in lines}


def split_keyset(how_many_subsets, keyset):
    print 'Splitting keyset of %d keys into %d subsets ...' % (len(keyset), how_many_subsets)
    ssets = [dict()]*how_many_subsets
    for id in keyset:
        nr = id % how_many_subsets
        ssets[nr][id] = keyset[id]
    print '  ... done'
    return ssets

def write_subsets_to_files(files_suffix, ssets):
    print 'Ordering subsets and writing subsets into files:'
    for i in range(len(ssets)):
        subset = ssets[i]
        filename = "%02d%s" % (i, files_suffix)
        with codecs.open(filename, "w", "utf-8") as f:
            print '-> '+filename
            for key in sorted(subset.iterkeys()):
                f.write(str(key)+subset[key]+"\n")
    print '  ... done'

if __name__ == '__main__':
    print 'Job started'
    download_the_file()
    make_it_a_csv()
    keyset = extract_keyset()
    ssets = split_keyset(4, keyset)  # Split into 4 subsets
    write_subsets_to_files('-city-id.txt', ssets)
    print 'Job finished'

