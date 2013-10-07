JSON responses
--------------

    # current weather for specific location
    http://api.openweathermap.org/data/2.5/weather?q=London,uk
    
    {
        "coord": {
            "lon": -0.12574,
            "lat": 51.50853
        },
        "sys": {
            "country": "GB",
            "sunrise": 1378877413,
            "sunset": 1378923812
        },
        "weather": [{
            "id": 521,
            "main": "Rain",
            "description": "proximity shower rain",
            "icon": "09d"
        }],
        "base": "gdps stations",
        "main": {
            "temp": 288.88,
            "pressure": 1021,
            "humidity": 63,
            "temp_min": 287.15,
            "temp_max": 290.37
        },
        "wind": {
            "speed": 4.6,
            "deg": 330
        },
        "clouds": {
            "all": 75
        },
        "dt": 1378899070,
        "id": 2643743,
        "name": "London",
        "cod": 200
    }

    #current weather with find
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
    
    #City weather history
    http://api.openweathermap.org/data/2.5/history/city?q=London
    
	{
	  "message": "",
	  "cod": "200",
	  "city_id": 2643743,
	  "calctime": 0.5979,
	  "cnt": 9,
	  "list": [
		   {
		    "weather": [{
		      "id": 803,
		      "main": "Clouds",
		      "description": "broken clouds",
		      "icon": "04d"
		    }],
		    "base": "gdps stations",
		    "main": {
		      "temp": 290.16,
		      "pressure": 1009,
		      "humidity": 67,
		      "temp_min": 289.26,
		      "temp_max": 290.93
		    },
		    "wind": {
		      "speed": 5.7,
		      "deg": 90
		    },
		    "clouds": {
		      "all": 75
		    },
		    "city": {
		      "zoom": 13,
		      "country": "GB",
		      "population": 1000000,
		      "find": ["LONDON"],
		      "id": 2643743,
		      "name": "London"
		    },
		    "dt": 1380636000
		  },
	
	  ...
	  
	  ]
	}
    
    # Meteostation tick history
    http://api.openweathermap.org/data/2.5/history/station?id=39276&type=tick
    
	{
	  "message": "",
	  "cod": "200",
	  "type": "tick",
	  "station_id": 39276,
	  "calctime": " tick = 0.0128 total=1.1367",
	  "cnt": 30,
	  "list": [{
	    "temp": 266.25,
	    "main": {
	      "temp": 266.25,
	      "humidity": 27.1,
	      "pressure": 1010.03
	    },
	    "humidity": 27.1,
	    "pressure": 1010.03,
	    "dt": 1362933923
	  },
	  {
	    "temp": 266.25,
	    "main": {
	      "temp": 266.25,
	      "humidity": 27.3,
	      "pressure": 1010.02
	    },
	    "humidity": 27.3,
	    "pressure": 1010.02,
	    "dt": 1362933983
	  },
	  {
	    "temp": 266.25,
	    "main": {
	      "temp": 266.25,
	      "humidity": 27.7,
	      "pressure": 1010.09
	    },
	    "humidity": 27.7,
	    "pressure": 1010.09,
	    "dt": 1362934043
	  }
	    ...
	    ]
	}
	
    # Meteostation hour history
	#http://api.openweathermap.org/data/2.5/history/station?id=35579&type=hour
	
	{
	  "message": "",
	  "cod": "200",
	  "type": "hour",
	  "station_id": 35579,
	  "calctime": 0.1122,
	  "cnt": 1,
	  "list": [{
	    "temp": {
	      "v": 281.48,
	      "c": 2,
	      "mi": 281.48,
	      "ma": 281.48
	    },
	    "pressure": {
	      "v": 1024,
	      "c": 2,
	      "mi": 1024,
	      "ma": 1024
	    },
	    "humidity": {
	      "v": 98,
	      "c": 2,
	      "mi": 98,
	      "ma": 98
	    },
	    "rain": {
	      "today": {
	        "v": 19.81,
	        "c": 2,
	        "mi": 19.812,
	        "ma": 19.812
	      }
	    },
	    "wind": {
	      "speed": {
	        "v": 4.37,
	        "c": 2,
	        "mi": 4.11,
	        "ma": 4.63
	      },
	      "deg": {
	        "v": 356
	      }
	    },
	    "main": {
	      "humidity": {
	        "v": 98,
	        "c": 2,
	        "mi": 98,
	        "ma": 98
	      },
	      "temp": {
	        "v": 281.48,
	        "c": 2,
	        "mi": 281.48,
	        "ma": 281.48
	      },
	      "temp_max": 281.48,
	      "pressure": {
	        "v": 1024,
	        "c": 2,
	        "mi": 1024,
	        "ma": 1024
	      }
	    },
	    "dt": 1381140000
	  }]
	}
	
	# Meteostation day history
	# http://api.openweathermap.org/data/2.5/history/station?id=35579&type=day
	{
	  "message": "",
	  "cod": "200",
	  "type": "day",
	  "station_id": 35579,
	  "calctime": 0.1868,
	  "cnt": 14,
	  "list": [{
	    "temp": {
	      "v": 287.78,
	      "c": 3,
	      "mi": 287.59,
	      "ma": 288.15
	    },
	    "pressure": {
	      "v": 1021,
	      "c": 3,
	      "mi": 1021,
	      "ma": 1021
	    },
	    "humidity": {
	      "v": 84.33,
	      "c": 3,
	      "mi": 84,
	      "ma": 85
	    },
	    "rain": {
	      "today": {
	        "v": 0.76,
	        "c": 3,
	        "mi": 0.762,
	        "ma": 0.762
	      }
	    },
	    "wind": {
	      "speed": {
	        "v": 11.82,
	        "c": 3,
	        "mi": 10.79,
	        "ma": 12.85
	      },
	      "deg": {
	        "v": 197
	      }
	    },
	    "main": {
	      "humidity": {
	        "v": 84.33,
	        "c": 3,
	        "mi": 84,
	        "ma": 85
	      },
	      "temp": {
	        "v": 287.78,
	        "c": 3,
	        "mi": 287.59,
	        "ma": 288.15
	      },
	      "temp_max": 287.59,
	      "pressure": {
	        "v": 1021,
	        "c": 3,
	        "mi": 1021,
	        "ma": 1021
	      }
	    },
	    "dt": 1378598400
	  },
	  {
	    "temp": {
	      "v": 287.97,
	      "c": 31,
	      "mi": 285.93,
	      "ma": 289.26
	    },
	    "pressure": {
	      "v": 1020.35,
	      "c": 31,
	      "mi": 1019,
	      "ma": 1021
	    },
	    "humidity": {
	      "v": 74.74,
	      "c": 31,
	      "mi": 62,
	      "ma": 87
	    },
	    "rain": {
	      "today": {
	        "v": 0,
	        "c": 31,
	        "mi": 0,
	        "ma": 0
	      }
	    },
	    "wind": {
	      "speed": {
	        "v": 2.97,
	        "c": 31,
	        "mi": 0,
	        "ma": 15.93
	      },
	      "deg": {
	        "v": 196
	      }
	    },
	    "main": {
	      "humidity": {
	        "v": 74.74,
	        "c": 31,
	        "mi": 62,
	        "ma": 87
	      },
	      "temp": {
	        "v": 287.97,
	        "c": 31,
	        "mi": 285.93,
	        "ma": 289.26
	      },
	      "temp_max": 285.93,
	      "pressure": {
	        "v": 1020.35,
	        "c": 31,
	        "mi": 1019,
	        "ma": 1021
	      }
	    },
	    "dt": 1378684800
	  },
	  ...
	  ]
	}

API key usage
-------------

Add the following parameter to the GET request: _APPID=<APIKEY>_
Example: 

    http://openweathermap.org/data/2.3/forecast/city?id=524901&APPID=<APIKEY>

or add the following line to HTTP request header:

    x-api-key:<APIKEY>