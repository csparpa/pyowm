Features
========

    owm = OWM(APIkey)

    # *** Current weather for a location (each list contains Weather objects) ***

    #http://api.openweathermap.org/data/2.5/find?q=London&type=accurate&cnt=0
    #search for the first matching city (defaults to search='accurate', limit=1)
    list = owm.currentWeather('London')

    #http://api.openweathermap.org/data/2.5/find?q=London&type=accurate
    #search for all the cities that are named 'London'
    list = owm.currentWeather('London',search='accurate',limit=None)

    #http://api.openweathermap.org/data/2.5/find?q=London&type=accurate&cnt=2
    #search for the first 3 cities that are named 'London'
    list = owm.currentWeather('London',search='accurate',limit=3)

    #http://api.openweathermap.org/data/2.5/find?q=London&type=like&cnt=4
    #search for the first 5 cities that contain the word 'London' in their name
    list = owm.currentWeather('London',search='like',limit=5)

    #http://api.openweathermap.org/data/2.5/find?lat=57&lon=-2.15&cnt=1
    #search for the weather at the first matching location at the specified coords (defaults to limit=1)
    list = owm.currentWeather({'lon':-2.15,'lat':57})

    #http://api.openweathermap.org/data/2.5/find?lat=57&lon=-2.15&cnt=3
    #search for the weather at the first 3 matching locations for the specified coords
    list = owm.currentWeather({'lon':-2.15,'lat':57}, limit=3)
    
    #http://api.openweathermap.org/data/2.5/find?lat=57&lon=-2.15
    #search for the weather at all matching locations for the specified coords
    list = owm.currentWeather({'lon':-2.15,'lat':57}, limit=None)


    # *** Weather forecasts for a location ***
    
    # 3h forecasts are provided for a streak of 5 days
    # daily forecasts are provided for a streak of 14 days
    
    owm.forecast('London,uk',type='3h')
    owm.forecast('London,uk',type='daily')
    
    
TODOs
-----
1. remove unit of measure and language configurations
2. pay attention to the cnt "incoherent behaviour"
3. Entities are better to be requested in XML, as it is more rich in information than JSON