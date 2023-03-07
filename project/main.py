import urllib.parse, urllib.request, urllib.error, json
import requests
from requests.structures import CaseInsensitiveDict
import pprint

import keys

# from_waypoint = input()             #get current location--put into lat/lon
# to_waypoint = 'some latlong'        #get stations within 1 mile radius
# waypoints_list = [from_waypoint]
#
# route_args = {'waypoints': waypoints_list, 'mode': 'walk', 'apiKey': keys.GEOAPIFY_SECRET_API_KEY}
# route_paramstr = urllib.parse.urlencode(route_args)
# route_baseurl = "https://api.geoapify.com/v1/routing?"


current_location = input("Enter your current address")
geocode_args = {'text': current_location, 'apiKey': keys.GEOAPIFY_SECRET_API_KEY}
geocode_paramstr = urllib.parse.urlencode(geocode_args)
geocode_baseurl = 'https://api.geoapify.com/v1/geocode/search?'
geocode_curr_loc = geocode_baseurl + '&' +geocode_paramstr
with urllib.request.urlopen(geocode_curr_loc) as response:
    geocode_curr_loc_str = response.read().decode()

geocode_data = json.loads(geocode_curr_loc_str)
pprint.pprint(geocode_data)
from_waypoint = geocode_data['features'][0]['geometry']['coordinates']
print(from_waypoint)
print(type(from_waypoint))

#lat, long, stop id
lr_stops = {'Northgate': [47.701976, -122.328388, 29_2192], 'Roosevelt Station': [47.676594, -122.315985, 990003],
            'U District Station': [47.660312, -122.314131, 1_990001], 'University of Washington Station': [47.649704, -122.303772, 99604], 'Capitol Hill Station': [47.619591, -122.320214, 99610],
            'Westlake Station': [47.611597, -122.336666, 1108], 'University Street Station': [47.607746, -122.335960, 455], 'Pioneer Square Station': [47.602669, -122.331318, 40_532],
            'International District/Chinatown Station': [47.598055, -122.328019, 623], 'Stadium Station': [47.592047, -122.327171, 99101], 'SODO Station': [47.580271, -122.327393, 99111],
            'Beacon Hill Station': [47.579401, -122.311340, 99121], "Mount Baker Station": [47.576716, -122.297802, 55949], 'Columbia City Station': [47.559616, -122.292618, 56039],
            'Othello Station': [47.538006, -122.281574, 56159], 'Rainier Beach Station': [47.522610, -122.279335, 56173], 'Tukwila International Boulevard Station': [47.464098, -122.288201, 99900],
            'Sea Tac/Airport Station': [47.445011, -122.296860, 99904], 'Angle Lake Station': [47.422638, -122.297787, 99913]}
stop_id = []    #how do I pull the correct stop id???
oba_args = {'apiKey': keys.ONEBUSAWAY_SECRET_API_KEY}
oba_paramstr = urllib.parse.urlencode(oba_args)
oba_baseurl = 'http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/'
oba_ardep = oba_baseurl + stop_id + oba_paramstr