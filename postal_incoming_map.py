import folium
import pandas
from geopy.geocoders import Nominatim
import time
import datetime

### Importing Postal Data CSV file and creating variables for date and locations ###
data = pandas.read_csv("Historic Postal Data - Incoming.csv", engine='python')
date = list(data["Date"])
loc = list(data["Location"])

data['Date'] = data['Date'].str[0:10]
data['Date'] = pandas.to_datetime(data['Date'],errors='coerce')
data.groupby(['Date','Location'])['Page URL'].count()




def return_letters(date,location):
    """
    date: str input of date
    location: str input of location
    returns number of letters for input date and locations
    """

    new_df=data[(data['Date']==date)&(data['Location']==location)]
    return new_df.groupby(['Date','Location'])['Page URL'].count()

print("New York letters on May 25th in 1748 " + str(return_letters('1748-05-25','New York')))

### Converts city name ot GPS coordinates
locator = Nominatim(user_agent="myGeocoder")
newyork_location = locator.geocode("New York")

### Creates folium map with New York Coordinates
postal_map = folium.Map(
    location=(newyork_location.latitude, newyork_location.longitude),
    tiles='cartodbpositron'
)

def return_coordinates(loc):
    geo_loc=locator.geocode(loc)
    geo_loc=(geo_loc.latitude, geo_loc.longitude)
    return geo_loc

print(return_coordinates("Boston"))

### Creates folium feature group for New York letters. Will later include all cities
'''
fgall = folium.FeatureGroup(name="newyork_letters")


fgall.add_child(folium.CircleMarker(location =[newyork_location.latitude,
                                                newyork_location.longitude],
                                    color = 'black',
                                    popup = "Letters: " + str(return_letters('1748-05-25','New York'))))
'''

fgall = folium.FeatureGroup(name="all letters")
fg_5_25_1748 = folium.FeatureGroup(name= "Letters in 5/25/1748")

for da, lo in zip(date, loc):
    if da == "5/25/1748":
        '''
        fgall.add_child(folium.CircleMarker(location=return_coordinates(lo),
                                        popup = "Letters: " + str(return_letters(da, lo)),
                                        color = 'black'))
        '''
        fg_5_25_1748.add_child(folium.CircleMarker(location=return_coordinates(lo),
                                        popup = "Letters: " + str(return_letters(da, lo)),
                                        color = 'black'))



### Adds current feature groups to map and creates HTML map file

postal_map.add_child(fgall)
postal_map.add_child(fg_5_25_1748)

postal_map.add_child(folium.LayerControl())

postal_map.save("Historic_Philadelphia_Incoming_Post.html")
