#!/usr/bin/python

import pyowm
from pyowm.exceptions import OWMError

import sys, argparse
from datetime import datetime



def main(argv):
   parser = argparse.ArgumentParser()
   parser.add_argument('-k', required=True, metavar='your_api_key')
   parser.add_argument('-p', required=True, metavar='\"Some Place,US\"')
   args = parser.parse_args()

   api_key = args.k
   place = args.p

   print ('Using key ' + api_key  + ' to query temperature in \"' + place  + '\"...' )   
   owm = pyowm.OWM(api_key) 
   try:
      observation = owm.weather_at_place(place)
   except OWMError as err:
      print (err)
      sys.exit(2)

   w = observation.get_weather()
   p = observation.get_location()
   print ('Coordinates of ' + p.get_name() + ': lon=' +  str(p.get_lon())  +  ' lat=' + str(p.get_lat()) )
   print ('Temperature at ' + str(datetime.fromtimestamp(w.get_reference_time())) + \
      ': ' + str(w.get_temperature('celsius')['temp']) +'C' )


if __name__ == "__main__":
   main(sys.argv[1:])


