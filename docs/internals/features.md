
Feature list
------------

	# Current weather for a single location
	1. Retrieve the current weather conditions for a specific toponym
	2. Retrieve the current weather conditions for a specific lon/lat couple
	
	# Current weather for multiple locations
	3. Search for current weather conditions in all the cities whose name match 
	   a specific pattern
	4. Search for current weather conditions in all the cities that lie close to
	   the specified lon/lat couple
	
	# Weather forecasts for a location
	5. Retrieve full 3h weather forecast for a specific toponym
	6. Retrieve full daily weather forecast for a specific toponym
	
	
	# History for a city
	7. search history for city (Yet To Be Implemented)
	
	# History for a station
	8. search history for station (Yet To Be Implemented)


Features in code
----------------

    # *** Current weather for a single location ***

    #http://api.openweathermap.org/data/2.5/weather?q=London,uk
    #retrieves the current weather for London,uk
    obs = owm.weather_at('London,uk')
    
    #http://api.openweathermap.org/data/2.5/weather?lat=57&lon=-2.15
    #retrieves the current weather for lat=57,lon=-2.15
    obs = owm.weather_at_at_coords(57,2.15)
    
    
    # *** Current weather for multiple locations ***

    #http://api.openweathermap.org/data/2.5/find?q=London&type=accurate
    #search for all the cities that are named 'London' (defaults to limit=None)
    list_of_obs = owm.find_weather_by_name('London',search='accurate')

    #http://api.openweathermap.org/data/2.5/find?q=London&type=accurate&cnt=2
    #search for the first 3 cities that are named 'London'
    list_of_obs = owm.find_weather_by_name('London',search='accurate',limit=3)

    #http://api.openweathermap.org/data/2.5/find?q=London&type=like&cnt=4
    #search for the first 5 cities that contain the word 'London' in their name
    list_of_obs = owm.find_weather_by_name('London',search='like',limit=5)

    #http://api.openweathermap.org/data/2.5/find?lat=57&lon=-2.15&cnt=1
    #search for the weather at the first matching location at the specified coords (defaults to limit=None)
    list_of_obs = owm.find_weather_by_coords(-2.15, 57)

    #http://api.openweathermap.org/data/2.5/find?lat=57&lon=-2.15&cnt=3
    #search for the weather at the first 3 matching locations for the specified coords
    list_of_obs = owm.find_weather_by_coords(-2.15, 57, limit=3)


    # *** Weather forecasts for a location ***
    
    # 3h forecasts are provided for a streak of 5 days
    # daily forecasts are provided for a streak of 14 days
    
    #http://api.openweathermap.org/data/2.5/forecast?q=London
    #search 3h forecast for London for the next 5 days
    forecast = owm.three_hours_forecast('London')
    
    #http://api.openweathermap.org/data/2.5/forecast/daily?q=London
    #search daily forecast for London for the next 14 days (defaults to: limit=None)
    forecast = owm.daily_forecast('London')

    #http://api.openweathermap.org/data/2.5/forecast/daily?q=London&cnt=3
    #search daily forecast for London for the next 3 days
    forecast = owm.daily_forecast('London',limit=3)


	# *** Historic hourly weather data recordings for a location ***
	
	#http://api.openweathermap.org/data/2.5/history/city?q=London,uk
	#search all recent weather history for London (last 24h approx)
	
	#http://api.openweathermap.org/data/2.5/history/city?q=London,uk&cnt=3
	#search the first 2 items of the recent weather history for London
	
	#http://api.openweathermap.org/data/2.5/history/city?q=London,uk&start=1369728000&end=1369789200
	#search the recent weather history items for London, measured in the specified period
	
	
	# *** Historic weather data recordings for a meteostation ***
	
	#http://api.openweathermap.org/data/2.5/history/station/39276?type=tick
	#search data measurements of station 39276
	#http://api.openweathermap.org/data/2.5/history/station/39276?type=hour
	#http://api.openweathermap.org/data/2.5/history/station/39276?type=day


	#http://api.openweathermap.org/data/2.5/history/station/39276?type=tick&cnt=3

