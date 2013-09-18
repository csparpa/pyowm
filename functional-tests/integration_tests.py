'''
Functional tests for the PyOWM library
These are "live" executions, that of course need the OWM web API to be up
and running
'''
import unittest
from pyowm import OWM

class Test(unittest.TestCase):
    
    __API_key = 'b02f5370dfd0f398b5746e1a976021a0'
    __owm = OWM(__API_key)

    def test_observation_at_place(self):
        """
        Test feature: get currently observed weather at specific location
        """
        o1 = self.__owm.observation_at_place('London,uk')
        o2 = self.__owm.observation_at_place('Kiev')
        o3 = self.__owm.observation_at_place('QmFoPIlbf')  #Shall be None
        self.assertTrue(o1, "")
        self.assertFalse(o1.get_reception_time() is None, "")
        self.assertTrue(o1.get_location(), "")
        self.assertNotIn(None, o1.get_location().__dict__.values(), "")
        self.assertTrue(o1.get_weather(), "")
        self.assertNotIn(None, o1.get_weather().__dict__.values(), "")
        self.assertTrue(o2, "")
        self.assertFalse(o2.get_reception_time() is None, "")
        self.assertTrue(o2.get_location(), "")
        self.assertNotIn(None, o2.get_location().__dict__.values(), "")
        self.assertTrue(o2.get_weather(), "")
        self.assertNotIn(None, o2.get_weather().__dict__.values(), "")
        self.assertFalse(o3)

    def test_observation_at_coords(self):
        """
        Test feature: get currently observed weather at specific coordinates
        """
        o1 = self.__owm.observation_at_coords(12.484589, 41.896144)  #Rome
        o2 = self.__owm.observation_at_coords(18.503723,-33.936524)  #Cape Town
        self.assertTrue(o1, "")
        self.assertFalse(o1.get_reception_time() is None, "")
        self.assertTrue(o1.get_location(), "")
        self.assertNotIn(None, o1.get_location().__dict__.values(), "")
        self.assertTrue(o1.get_weather(), "")
        self.assertNotIn(None, o1.get_weather().__dict__.values(), "")
        self.assertTrue(o2, "")
        self.assertFalse(o2.get_reception_time() is None, "")
        self.assertTrue(o2.get_location(), "")
        self.assertNotIn(None, o2.get_location().__dict__.values(), "")
        self.assertTrue(o2.get_weather(), "")
        self.assertNotIn(None, o2.get_weather().__dict__.values(), "")
        
    def test_find_observations_by_name(self):
        """
        Test feature: find currently observed weather for locations matching
        the specified text search pattern
        """
        # Test using searchtype=accurate
        o1 = self.__owm.find_observations_by_name("London", "accurate")
        o2 = self.__owm.find_observations_by_name("Paris", "accurate", 2)
        self.assertTrue(isinstance(o1, list))
        for item in o1:
            self.assertTrue(item, "")
            self.assertTrue(item.get_reception_time(), "")
            self.assertTrue(item.get_location(), "")
            self.assertNotIn(None, item.get_location().__dict__.values(), "")
            self.assertTrue(item.get_weather(), "")
            self.assertNotIn(None, item.get_weather().__dict__.values(), "")
        self.assertTrue(isinstance(o2, list))
        self.assertEqual(2, len(o2), "")
        for item in o2:
            self.assertTrue(item, "")
            self.assertTrue(item.get_reception_time(), "")
            self.assertTrue(item.get_location(), "")
            self.assertNotIn(None, item.get_location().__dict__.values(), "")
            self.assertTrue(item.get_weather(), "")
            self.assertNotIn(None, item.get_weather().__dict__.values(), "")

        # Test using searchtype=like
        o3 = self.__owm.find_observations_by_name("London", "like")
        o4 = self.__owm.find_observations_by_name("Paris", "like", 2)
        self.assertTrue(isinstance(o3, list))
        for item in o3:
            self.assertTrue(item, "")
            self.assertTrue(item.get_reception_time(), "")
            self.assertTrue(item.get_location(), "")
            self.assertNotIn(None, item.get_location().__dict__.values(), "")
            self.assertTrue(item.get_weather(), "")
            self.assertNotIn(None, item.get_weather().__dict__.values(), "")
        self.assertTrue(isinstance(o4, list))
        self.assertEqual(2, len(o4), "")
        for item in o4:
            self.assertTrue(item, "")
            self.assertTrue(item.get_reception_time(), "")
            self.assertTrue(item.get_location(), "")
            self.assertNotIn(None, item.get_location().__dict__.values(), "")
            self.assertTrue(item.get_weather(), "")
            self.assertNotIn(None, item.get_weather().__dict__.values(), "")

    def test_find_observations_by_coords(self):
        """
        Test feature: find currently observed weather for locations that are 
        nearby the specified coordinates
        """
        o2 = self.__owm.find_observations_by_coords(-2.15, 57.0)  # Scotland
        self.assertTrue(isinstance(o2, list))
        for item in o2:
            self.assertTrue(item, "")
            self.assertTrue(item.get_reception_time(), "")
            self.assertTrue(item.get_location(), "")
            self.assertNotIn(None, item.get_location().__dict__.values(), "")
            self.assertTrue(item.get_weather(), "")
            self.assertNotIn(None, item.get_weather().__dict__.values(), "")   
        o1 = self.__owm.find_observations_by_coords(-2.15, 57.0, 2)  # Scotland
        self.assertTrue(isinstance(o1, list))
        self.assertEqual(2, len(o1), "")
        for item in o1:
            self.assertTrue(item, "")
            self.assertTrue(item.get_reception_time(), "")
            self.assertTrue(item.get_location(), "")
            self.assertNotIn(None, item.get_location().__dict__.values(), "")
            self.assertTrue(item.get_weather(), "")
            self.assertNotIn(None, item.get_weather().__dict__.values(), "")
        
    def test_three_hours_forecast(self):
        """
        Test feature: get 3 hours forecast for a specific location
        """
        f1 = self.__owm.three_hours_forecast("London,uk")
        f2 = self.__owm.three_hours_forecast('Kiev')
        f3 = self.__owm.three_hours_forecast('QmFoPIlbf')  #Shall be None
        self.assertTrue(f1)
        self.assertFalse(f1.get_reception_time() is None)
        self.assertTrue(f1.get_location())
        self.assertNotIn(None, f1.get_location().__dict__.values())
        for weather in f1:
            self.assertTrue(weather)
            self.assertNotIn(None, weather.__dict__.values())
        self.assertTrue(f2)
        self.assertFalse(f2.get_reception_time() is None)
        self.assertTrue(f2.get_location())
        self.assertNotIn(None, f2.get_location().__dict__.values())
        for weather in f2:
            self.assertTrue(weather)
            self.assertNotIn(None, weather.__dict__.values())
        self.assertFalse(f3)
        
    def test_daily_forecast(self):
        """
        Test feature: get daily forecast for a specific location
        """
        f1 = self.__owm.daily_forecast("London,uk")
        f2 = self.__owm.daily_forecast('Kiev')
        f3 = self.__owm.daily_forecast('QmFoPIlbf')  #Shall be None
        self.assertTrue(f1)
        self.assertFalse(f1.get_reception_time() is None)
        self.assertTrue(f1.get_location())
        self.assertNotIn(None, f1.get_location().__dict__.values())
        for weather in f1:
            self.assertTrue(weather)
            self.assertNotIn(None, weather.__dict__.values())
        self.assertTrue(f2)
        self.assertFalse(f2.get_reception_time() is None)
        self.assertTrue(f2.get_location())
        self.assertNotIn(None, f2.get_location().__dict__.values())
        for weather in f2:
            self.assertTrue(weather)
            self.assertNotIn(None, weather.__dict__.values())
        self.assertFalse(f3)
        
if __name__ == "__main__":
    unittest.main()
    
