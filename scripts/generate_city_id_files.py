import requests, re, codecs, csv

city_list_url = 'http://openweathermap.org/help/city_list.txt'
city_list = "city_list.txt"
csv_city_list = "city_list.csv"
ordered_csv_city_list = "city_list.ordered.csv"

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

def order_its_lines_by_id():
    print 'Ordering csv lines by city ID ...'
    lines = []
    with codecs.open(csv_city_list, "r", "utf-8") as f:
        for line in f.readlines():
            fields = line.split("\n")[0].split(",")
            try:
                if isinstance(fields[2], unicode):
                    if isinstance(fields[4], str):
                        fields = [ long(fields[0]), fields[1], float(fields[2]), float(fields[3]), fields[4] ]
                    else:
                        fields = [ long(fields[0]), fields[1]+fields[2], float(fields[3]), float(fields[4]), fields[5] ]
                else:
                    fields = [ long(fields[0]), fields[1], float(fields[2]), float(fields[3]), fields[4] ]
                lines.append(fields)
            except Exception as e:
                print e
    return sorted(lines, key=lambda x: x[0])
    print '  ... done'

if __name__ == '__main__':
    print 'Job started'
    download_the_file()
    make_it_a_csv()
    lines = order_its_lines_by_id()
    # TBD: now you can create a dict from the lines and then split the keyset
    # into multiple files
    print 'Job finished'

