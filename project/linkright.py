# import time
#
# import requests
#
# import keys
# import json
#
# apiKey = keys.GEOAPIFY_SECRET_API_KEY
# timeout = 1
# maxAttempt = 10
#
#
# def getLocations (locations):
#     url = "https://api.goeapify.com/v1/batch/geocode/search?apiKey=" + apiKey
#     response = requests.post(url, json=locations)
#     result = response.json()
#
#     status = response.status_code
#     if (status != 202):
#         print('Failed to create a job. Check if the input data is correct.')
#         return
#     jobId = result['id']
#     getResultsUrl = url + '&id=' + jobId
#
#     time.sleep(timeout)
#     result = getLocationJobs (getResutlsUrl, 0)
#     if result:
#         print(result)
#         print('You can also get results by the URL - ' + getResultsUrl)
#     else:
#         print('You exceeded the maximum number of attempts. Try to get results later.')
#
#
# def getLocationJobs(url, attemptCount):
#     response = requests.get(url)
#     result = response.json()
#     status = response.status_code
#     if status == 200:
#         print('The job was successful. Here are the results: ')
#         return result
#     elif attemptCount > maxAttempt:
#         return
#     elif status == 202:
#         print('The job is pending...')
#         time.sleep(timeout)
#         return getLocationJobs(url, attemptCount + 1)
#
#
# data = [input('Please enter address 1: \n'), input('Please enter address 2: \n'), input('Please enter address 3: \n')]
# getLocations(data)



import requests

import keys

# Replace YOUR_API_KEY with your actual API key. Sign up and get an API key on https://www.geoapify.com/
API_KEY = keys.GEOAPIFY_SECRET_API_KEY

# Define the address to geocode
address = "1600 Amphitheatre Parkway, Mountain View, CA"

# Build the API URL
url = f"https://api.geoapify.com/v1/geocode/search?text={address}&limit=1&apiKey={API_KEY}"

# Send the API request and get the response
response = requests.get(url)

# Check the response status code
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()

    # Extract the first result from the data
    result = data["features"][0]

    # Extract the latitude and longitude of the result
    latitude = result["geometry"]["coordinates"][1]
    longitude = result["geometry"]["coordinates"][0]

    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print(f"Request failed with status code {response.status_code}")


from requests.structures import CaseInsensitiveDict

url = "https://api.geoapify.com/v1/routing?waypoints=50.96209827745463%2C4.414458883409225%7C50.429137079078345%2C5.00088081232559&mode=drive&apiKey=" + API_KEY

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

resp = requests.get(url, headers=headers)

print(resp.status_code)

def get_location():
    current_location = input(ask user for current location in address form)
    from_waypoint = use geoapify api to geocode location
    return from_waypoint

def get_stop(from_waypoint)
    station_dictionary = { 'station1': [lat1, long1], 'station2': [lat2, long2]...}
    radius = 1.0 mile
    nearby_station_list = find stations within radius
    return nearby_station_list

def get_directions():
    api_key = keys.GEOAPIFY_SECRET_API_KEY
    from_waypoint = get_location()
    to_waypoint_list = get_stop(from_waypoint)
    for item in to_waypoint_list:
        url = 'https://api.geoapify.com/v1/routing?waypoints=?{}|{}&mode=walk&apiKey={}'.format(from_waypoint, to_waypoint_list[item], api_key)





















