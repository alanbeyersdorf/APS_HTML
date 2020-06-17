import folium
import pandas
from geopy.geocoders import Nominatim
import time
import datetime

### Importing Postal Data CSV file and creating variables for date and locations ###
data = pandas.read_csv("Historic Postal Data - Incoming.csv", engine='python')
date = list(data["Date"])
loc = list(data["Location"])

### Testing to make sure CSV can be read by python/is iterable and find date
if any("5/25/1748" in s for s in date):
    print("true")

### Testing to make sure python can find number of New York and specific date iterations###
newyork_total = loc.count("New York")
print("Total letters from New York: " + str(newyork_total))
date_1748 = date.count("5/25/1748")
print("Total letters recieve in 1748: " + str(date_1748))

### ***CURRENTLY NOT WORKING*** ###
### Testing to see if newyork_total can be cross referenced with date_1748
### in order to show number of letters coming only from New York on 5/25/1748

### Could require function using "while"?

### Error below code


### newyork_1748 = [s for s in newyork_total if date_1748 in s]
### print(newyork_1748)
###
### Alan-Beyersdorfs-Mac-mini:APS_HTML abeyers$ python3 postal_incoming_map.py
### true
### Total letters from New York: 4340
### Total letters recieve in 1748: 138
### Traceback (most recent call last):
###   File "postal_incoming_map.py", line 25, in <module>
###     newyork_1748 = [s for s in newyork_total if date_1748 in s]
### TypeError: 'int' object is not iterable

### ***Resumes working code below*** ###

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
