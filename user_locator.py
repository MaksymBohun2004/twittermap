import os

import folium
import geopy
from functools import lru_cache
from geopy import Nominatim
import random


@lru_cache()
def locate(location):
    """
    Gets the name of a city and returns its coordinates
    """
    geolocator = Nominatim(user_agent="Movie_Map")
    location = geolocator.geocode(location)
    location = (location.latitude, location.longitude)
    return location


def put_on_map(dct):
    """
    Puts a Marker of user coordinates on the map,
    puts markers of movies and connect user with
    locations with lines that specify the distance between
    those two objects
    """
    os.remove('templates/friends_map.html')
    my_map = folium.Map(zoom_start=10)
    fg = folium.FeatureGroup(name="Users")
    colors = ['darkpurple', 'cadetblue', 'darkred', 'green', 'lightgray', 'darkgreen',
              'pink', 'purple', 'beige', 'lightgreen', 'red', 'darkblue', 'lightblue',
              'gray', 'blue', 'white', 'orange', 'black', 'lightred']
    for location in dct:
        for movie in dct[location]:
            fg.add_child(folium.Marker(location=[location[0]
                                                 - 0.001 * random.uniform(-20, 20),
                                                 location[1] + 0.001 * random.uniform(-20, 20)],
                                       popup=movie,
                                       icon=folium.Icon(color=random.choice(colors))))
    my_map.add_child(fg)
    my_map.add_child(folium.LayerControl())
    my_map.save(outfile='templates/friends_map.html')
