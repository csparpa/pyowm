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
    
    #http://api.openweathermap.org/data/2.5/forecast?q=London
    #search 3h forecast for London for the next 5 days
    owm.3hForecast('London')
    
    #http://api.openweathermap.org/data/2.5/forecast/daily?q=London
    #search daily forecast for London for the next 14 days (defaults to: limit=None)
    owm.dailyForecast('London')

    #http://api.openweathermap.org/data/2.5/forecast/daily?q=London&cnt=3
    #search daily forecast for London for the next 3 days
    owm.dailyForecast('London',limit=3)


JSON responses
--------------

    #current weather
    http://api.openweathermap.org/data/2.5/find?q=London&type=like&cnt=4

    { "cod" : "200",
      "count" : 5,
      "list" : [ { "clouds" : { "all" : 20 },
            "coord" : { "lat" : 51.50853,
                "lon" : -0.12573999999999999
              },
            "dt" : 1378237178,
            "id" : 2643743,
            "main" : { "humidity" : 56,
                "pressure" : 1025,
                "temp" : 293.74000000000001,
                "temp_max" : 296.14999999999998,
                "temp_min" : 291.48000000000002
              },
            "name" : "London",
            "sys" : { "country" : "GB" },
            "weather" : [ { "description" : "few clouds",
                  "icon" : "02n",
                  "id" : 801,
                  "main" : "Clouds"
                } ],
            "wind" : { "deg" : 0,
                "speed" : 1
              }
          },
    ...],
    "message":"like"}

    #3h forecasts
    http://api.openweathermap.org/data/2.5/forecast?q=London

    { "city" : 
        { "coord" : { "lat" : 51.50853,
              "lon" : -0.12573999999999999
            },
          "country" : "GB",
          "id" : 2643743,
          "name" : "London",
          "population" : 1000000
        },
      "cnt" : 27,
      "cod" : "200",
      "list" : [ { "clouds" : { "all" : 92 },
            "dt" : 1378231200,
            "dt_txt" : "2013-09-03 18:00:00",
            "main" : { "grnd_level" : 1030.1199999999999,
                "humidity" : 57,
                "pressure" : 1030.1199999999999,
                "sea_level" : 1038.5899999999999,
                "temp" : 294.19999999999999,
                "temp_kf" : -1.8999999999999999,
                "temp_max" : 296.09800000000001,
                "temp_min" : 294.19999999999999
              },
            "sys" : { "pod" : "d" },
            "weather" : [ { "description" : "overcast clouds",
                  "icon" : "04d",
                  "id" : 804,
                  "main" : "Clouds"
                } ],
            "wind" : { "deg" : 252.00200000000001,
                "speed" : 1.1000000000000001
              }
          },
            ...
        ],
      "message" : 0.16209999999999999
    }


    #daily forecast
    http://api.openweathermap.org/data/2.5/forecast/daily?q=London

    { "city" : { "coord" : { "lat" : 51.50853,
              "lon" : -0.12573999999999999
            },
          "country" : "GB",
          "id" : 2643743,
          "name" : "London",
          "population" : 1000000
        },
      "cnt" : 7,
      "cod" : "200",
      "list" : [ { "clouds" : 92,
            "deg" : 252,
            "dt" : 1378206000,
            "humidity" : 57,
            "pressure" : 1030.1199999999999,
            "speed" : 1.1000000000000001,
            "temp" : { "day" : 294.37,
                "eve" : 294.37,
                "max" : 294.37,
                "min" : 286.25,
                "morn" : 294.37,
                "night" : 286.25
              },
            "weather" : [ { "description" : "overcast clouds",
                  "icon" : "04d",
                  "id" : 804,
                  "main" : "Clouds"
                } ]
          },
        ...],
      "message" : 0.031
    }

    
TODOs
-----
1. Fix usage-examples.md (remove unit of measure and language configurations)
2. pay attention to the cnt "incoherent behaviour"
3. Provide utilities for human-friendly OWM data handling
