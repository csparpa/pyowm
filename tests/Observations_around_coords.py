from pyowm import OWM
key = "<Your Free Weather2.5+ One Call Api key here>"
owm = OWM(key)  
mgr = owm.weather_manager()


observation_list = mgr.weather_around_coords(lat,lon) #latitude, longitude
#print(observation_list)
for ix in range (len(observation_list)):
    observation = observation_list[ix]
    w = observation.weather
    print(w)      # <Weather - reference time=2013-12-18 09:20, status=Clouds>
            
    # Weather details

    print(w.wind())                  # {'speed': 4.6, 'deg': 330}
    print(w.humidity)                # 87
    print(w.temperature('celsius'))  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
