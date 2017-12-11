#!/usr/bin/python

import pyowm
from pyowm.exceptions import OWMError

import sys, getopt
from datetime import datetime

def usage():
   print ('Usage: getTemp.py -k 60039jdfd09jf3a9 -p \"Some Place\"')
   sys.exit(2)

def main(argv):
   api_key = ''
   place = ''
   try:
      opts, args = getopt.getopt(argv, "k:p:",["key=","place="])
   except getopt.GetoptError:
      usage()

   for opt, arg in opts:
      if opt in ("-k", "--key"):
         api_key = arg
      elif opt in ("-p", "--place"):
         place = arg

   if (api_key == '' or place== ''):
      usage()

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


