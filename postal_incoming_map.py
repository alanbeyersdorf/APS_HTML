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

### Testing to make sure CSV can be read by python/is iterable and find date
if any("5/25/1748" in s for s in date):
    print("true")

### Testing to make sure python can find number of New York and specific date iterations###
newyork_total = loc.count("New York")
print("Total letters from New York: " + str(newyork_total))
date_1748 = date.count("5/25/1748")
print("Total letters recieve in 1748: " + str(date_1748))



### Converts city name ot GPS coordinates
locator = Nominatim(user_agent="myGeocoder")
newyork_location = locator.geocode("New York")

### Creates folium map with New York Coordinates
postal_map = folium.Map(
    location=(newyork_location.latitude, newyork_location.longitude),
    tiles='cartodbpositron'
)

### Tests and prints counts from various variables
print("Total Letters into Philadelphia Post Office: " + str(len(loc)))
print("Letters from New York: " + str(loc.count('New York')))
print(loc.count('Boston'))
print("Latitude = {}, Longitude = {}".format(newyork_location.latitude, newyork_location.longitude))

### Creates folium feature group for New York letters. Will later include all cities
fgall = folium.FeatureGroup(name="newyork_letters")

fgall.add_child(folium.CircleMarker(location =[newyork_location.latitude, newyork_location.longitude],
                                  color = 'black'))

### Adds current feature groups to map and creates HTML map file

postal_map.add_child(fgall)

postal_map.save("Historic_Philadelphia_Incoming_Post.html")
