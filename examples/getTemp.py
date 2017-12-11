#!/usr/bin/python

import pyowm
from pyowm.exceptions import OWMError

import sys, getopt
from datetime import datetime

def main(argv):
   api_key = ''
   place = ''
   try:
      opts, args = getopt.getopt(argv, "k:p:",["key=","place="])
   except getopt.GetoptError:
      print 'TODO : help message'
      sys.exit(2)

   for opt, arg in opts:
      if opt in ("-k", "--key"):
         api_key = arg
      elif opt in ("-p", "--place"):
         place = arg

   if (api_key == ''):
	print ('You MUST provide a valid API key')
	sys.exit(2)
   
   if (place== ''):
	print ('You MUST provide a place like \"London,Uk\"')
	sys.exit(2)


   print ('Using key %s to query temperature in \"%s\"...' % (api_key, place) )   

   owm = pyowm.OWM(api_key) 
   try:
      observation = owm.weather_at_place(place)
   except OWMError as err:
      print (err)
      sys.exit(2)

   w = observation.get_weather()
   p = observation.get_location()
   print('Coordinates of %s: lon=%s lat=%s ' % ( p.get_name(), p.get_lon(), p.get_lat() ) )
   print ('Temperature at %s: %sC' % (datetime.fromtimestamp(w.get_reference_time()), w.get_temperature('celsius')['temp'])  )



if __name__ == "__main__":
   main(sys.argv[1:])


