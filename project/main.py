import urllib.parse, urllib.request, urllib.error, json
from math import floor
from urllib import request

import requests
from requests.structures import CaseInsensitiveDict
import pprint
import datetime
import keys




# from_waypoint = input()             #get current location--put into lat/lon
# to_waypoint = 'some latlong'        #get stations within 1-mile radius
# waypoints_list = [from_waypoint]
#
# route_args = {'waypoints': waypoints_list, 'mode': 'walk', 'apiKey': keys.GEOAPIFY_SECRET_API_KEY}
# route_paramstr = urllib.parse.urlencode(route_args)
# route_baseurl = "https://api.geoapify.com/v1/routing?"

#ALL THIS WORKS!!
def geocode_current_location():                         #returns the lat + long for current location based on user input
    input_location = input("Enter your current address")
    geocode_args = {'text': input_location, 'apiKey': keys.GEOAPIFY_SECRET_API_KEY}
    geocode_paramstr = urllib.parse.urlencode(geocode_args)
    geocode_baseurl = 'https://api.geoapify.com/v1/geocode/search?'
    geocode_curr_loc = geocode_baseurl + '&' + geocode_paramstr
    with urllib.request.urlopen(geocode_curr_loc) as response:
        geocode_curr_loc_str = response.read().decode()

    geocode_data = json.loads(geocode_curr_loc_str)
   # pprint.pprint(geocode_data)
    from_waypoint = geocode_data['features'][0]['geometry']['coordinates']
   # print(from_waypoint)
    #print(type(from_waypoint))
    return from_waypoint


lr_stops = {'Northgate Station': [47.701976, -122.328388, '990005'], 'Roosevelt Station': [47.676594, -122.315985, '990003'],
            'U District Station': [47.660312, -122.314131, '1_990001'], 'University of Washington Station': [47.649704, -122.303772, '99604'], 'Capitol Hill Station': [47.619591, -122.320214, '99610'],
            'Westlake Station': [47.611597, -122.336666, '1108'], 'University Street Station': [47.607746, -122.335960, '455'], 'Pioneer Square Station': [47.602669, -122.331318, '40_532'],
            'International District/Chinatown Station': [47.598055, -122.328019, '623'], 'Stadium Station': [47.592047, -122.327171, '99101'], 'SODO Station': [47.580271, -122.327393, '99111'],
            'Beacon Hill Station': [47.579401, -122.311340, '99121'], "Mount Baker Station": [47.576716, -122.297802, '55949'], 'Columbia City Station': [47.559616, -122.292618, '56039'],
            'Othello Station': [47.538006, -122.281574, '56159'], 'Rainier Beach Station': [47.522610, -122.279335, '56173'], 'Tukwila International Boulevard Station': [47.464098, -122.288201, '99900'],
            'Sea Tac/Airport Station': [47.445011, -122.296860, '99904'], 'Angle Lake Station': [47.422638, -122.297787, '99913']}

#make empty list. use for loop--iterate over each station, calculate distance between curr location + station, if within bounds, add to list, otherwise move on
def get_time_and_dist(lr_stops): #LONG FIRST!!!
    current_location = geocode_current_location()
    geomatrix_args= {'mode': 'walk',                ##call once for each station
                     'sources': [{'location': current_location}],
                     'targets': [{'location': [lr_stops['Northgate Station'][1], lr_stops['Northgate Station'][0]]},
                                 {'location': [lr_stops['Roosevelt Station'][1], lr_stops['Roosevelt Station'][0]]}]
                     }
    print(geomatrix_args)

    Headers = {'Content-Type': 'application/json'}
    geomatrix_baseurl = 'https://api.geoapify.com/v1/routematrix?apiKey=' + keys.GEOAPIFY_SECRET_API_KEY
    try:
        response = requests.post(geomatrix_baseurl, headers=Headers, data=json.dumps(geomatrix_args))
        pprint.pprint(response.json())
    except requests.exceptions.HTTPError as e:
        print(e.response.text)
    #geomatrix_route = geomatrix_baseurl + '?' + Headers + geomatrix_paramstr
    # response = requests.post(geomatrix_baseurl, params= geomatrix_args, headers=Headers)
    # look = json.loads(response)
    # pprint.pprint(look)
    #
    # try:
    #     response = requests.post(geomatrix_baseurl, headers=Headers, data=geomatrix_args)

    # url = "https://api.geoapify.com/v1/routematrix?apiKey=9a43bbe9bdd0494f906028ffe473c835"
    # headers = {"Content-Type": "application/json"}
    # data = '{"mode":"walk", "type": "short", "sources":[{"location":[-122.30806059473039,47.6543466]}],"targets":[{"location":[-122.314049,47.660729]},{"location":[-122.30377035000001,47.6498463]}]}'
    #
    # try:
    #     resp = requests.post(url, headers=headers, data=data)
    #     print('\n\n--------geomatrix---------\n\n')
    #     pprint.pprint(resp.json())
    # except requests.exceptions.HTTPError as e:
    #     print(e.response.text)

    # with urllib.request.urlopen(geomatrix_route) as response:
    #     geomatrix_route_str = response.read().decode()
    #
    # geomatrix_route_data = json.load(geomatrix_route_str)
    # pprint.pprint(geomatrix_route_data)
#
# #lat, long, stop id

# stop_id = lr_stops['Northgate Station'][2]
# oba_args = {'key': keys.ONEBUSAWAY_SECRET_API_KEY}
# oba_paramstr = urllib.parse.urlencode(oba_args)
# oba_baseurl = 'http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/'
# oba_ardep = oba_baseurl + stop_id + '.json' + oba_paramstr

with urllib.request.urlopen('http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/1_990001.json?key=' + keys.ONEBUSAWAY_SECRET_API_KEY) as response:
    oba_ardep_str = response.read().decode()

oba_ardep_data = json.loads(oba_ardep_str)
f = open('oba.json', "w")
f.write(oba_ardep_str)

time_current = oba_ardep_data['currentTime']/1000.0
for index in range(len(oba_ardep_data['data']['entry']['arrivalsAndDepartures'])):
    time_arrival = oba_ardep_data['data']['entry']['arrivalsAndDepartures'][index]['scheduledArrivalTime']/1000.0
    time_diff = time_arrival - time_current
    time_diff_min = floor(time_diff/60)
    #if time_diff is neg, pring message, missed the train.
    print('unix epoch time diff', time_diff, 'Time diff in min:', time_diff_min)
    human_time_current = datetime.datetime.fromtimestamp(time_current).strftime('%Y-%m-%d %H:%M:%S')
    human_time_arrival = datetime.datetime.fromtimestamp(time_arrival).strftime('%Y-%m-%d %H:%M:%S')
    human_time_diff = datetime.datetime.fromtimestamp((time_diff)).strftime('%H: %M: %S')
    print('Current time: ', human_time_current, '\tPredicted time of arrival: ', human_time_arrival, '\tTime diff:', human_time_diff)
f.close()

get_time_and_dist(lr_stops)