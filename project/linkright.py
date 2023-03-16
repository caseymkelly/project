import urllib.request, urllib.parse, urllib.error
import json
import requests
import pprint
import datetime
import keys
from math import floor

#Pioneer Square station stop ID NOT working   #lr_stops: { 'station' : [ lon, lat, NB stop, SB stop]
lr_stops = {'Northgate Station': [47.701976, -122.328388, '1_990006', '1_990005'], 'Roosevelt Station': [47.676594, -122.315985, '1_990004', '1_990003'],
            'U District Station': [47.660312, -122.314131, '1_990002', '1_990001'], 'University of Washington Station': [47.649704, -122.303772, '1_99605', '1_99604'], 'Capitol Hill Station': [47.619591, -122.320214, '1_99603', '1_99610'],
            'Westlake Station': [47.611597, -122.336666, '1_1121', '1_1108'], 'University Street Station': [47.607746, -122.335960, '1_565', '1_455'], 'Pioneer Square Station': [47.602669, -122.331318,  '1_532', '1_501'],
            'International District/Chinatown Station': [47.598055, -122.328019, '1_621', '1_623'], 'Stadium Station': [47.592047, -122.327171, '1_99260', '1_99101'], 'SODO Station': [47.580271, -122.327393, '1_99256', '1_99111'],
            'Beacon Hill Station': [47.579401, -122.311340, '1_99240', '1_99121'], "Mount Baker Station": [47.576716, -122.297802, '1_55860', '1_55949'], 'Columbia City Station': [47.559616, -122.292618, '1_55778', '1_56039'],
            'Othello Station': [47.538006, -122.281574, '1_55656', '1_56159'], 'Rainier Beach Station': [47.522610, -122.279335, '1_55578', '1_56173'], 'Tukwila International Boulevard Station': [47.464098, -122.288201, '1_99905', '1_99900'],
            'Sea Tac/Airport Station': [47.445011, -122.296860, '1_99903', '1_99904'], 'Angle Lake Station': [47.422638, -122.297787, '1_99914', '1_99913']}


##RETURN LAT AND LONG LIST FOR CURRENT LOCATION (INPUT)##
def geocode_current_location(current_location):
    geocode_args = {'text': current_location, 'apiKey': keys.GEOAPIFY_SECRET_API_KEY}
    geocode_paramstr = urllib.parse.urlencode(geocode_args)
    geocode_baseurl = 'https://api.geoapify.com/v1/geocode/search?'
    geocode_curr_loc = geocode_baseurl + '&' + geocode_paramstr

    with urllib.request.urlopen(geocode_curr_loc) as response:
        geocode_curr_loc_str = response.read().decode()
    geocode_data = json.loads(geocode_curr_loc_str)
    from_waypoint = geocode_data['features'][0]['geometry']['coordinates']
    return from_waypoint


#FINDS STATIONS WITHIN RADIUS, RETURNS Dict OF NEARBY STATIONS {stop name: dist (mi), time to dist (min)}


def get_time_dist_to_lrstops(lr_stops, radius, current_location):
    current_location = geocode_current_location(current_location)
    nearby_lrstops = {}

    for station in lr_stops:
        geomatrix_args = {'mode': 'walk',  ##call once for each station
                          'sources': [{'location': current_location}],
                          'targets': [{'location': [lr_stops[station][1], lr_stops[station][0]]}],
                          'type': 'short'
                          }
        headers = {'Content-Type': 'application/json'}
        geomatrix_baseurl = 'https://api.geoapify.com/v1/routematrix?apiKey=' + keys.GEOAPIFY_SECRET_API_KEY

        try:
            loc_data = requests.post(geomatrix_baseurl, headers=headers, data=json.dumps(geomatrix_args))
            data = loc_data.json()
            #print('Distance to ', station, ': ', round((data['sources_to_targets'][0][0]['distance']/1609), 2), 'mi')
            #print('Time to ', station, ': ', floor(data['sources_to_targets'][0][0]['time']/60), 'min')
        except requests.exceptions.HTTPError as e:
            print(e.response.text)

        dist_mi = round((data['sources_to_targets'][0][0]['distance']/1609), 2)
        time_min = floor(data['sources_to_targets'][0][0]['time']/60)

        if dist_mi <= radius:
            nearby_lrstops[station] = [dist_mi, time_min]
    return nearby_lrstops


def next_train(direction, radius, current_location):
    nearby_lrstops = get_time_dist_to_lrstops(lr_stops, radius, current_location)

    for station in nearby_lrstops:
        # baseurl = 'http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/'
        # oba_args = {'key': keys.ONEBUSAWAY_SECRET_API_KEY, ''}
        if direction == 'North':
            with urllib.request.urlopen('http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/' + str(lr_stops[station][2]) + '.json?key=' + keys.ONEBUSAWAY_SECRET_API_KEY) as response:
                oba_ardep_str = response.read().decode()
            oba_ardep_data = json.loads(oba_ardep_str)
            time_current = oba_ardep_data['currentTime'] / 1000.0
            count = 0
            while count < 3:
                time_arrival = oba_ardep_data['data']['entry']['arrivalsAndDepartures'][count][
                                   'scheduledArrivalTime'] / 1000.0
                time_diff = time_arrival - time_current
                time_diff_min = floor(time_diff / 60)
                nearby_lrstops[station].append(time_diff_min)
                count += 1
        else:
            with urllib.request.urlopen('http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/' + str(lr_stops[station][3]) + '.json?key=' + keys.ONEBUSAWAY_SECRET_API_KEY) as response:
                oba_ardep_str = response.read().decode()
            oba_ardep_data = json.loads(oba_ardep_str)
            time_current = oba_ardep_data['currentTime'] / 1000.0
            count = 0
            while count < 3:                                                                              #only getting info for the next 3 trains
                time_arrival = oba_ardep_data['data']['entry']['arrivalsAndDepartures'][count][
                                   'scheduledArrivalTime'] / 1000.0
                time_diff = time_arrival - time_current
                time_diff_min = floor(time_diff / 60)
                nearby_lrstops[station].append(time_diff_min)
                count += 1
    return nearby_lrstops










