import keys     #keys.ONEBUSAWAY_SECRET_API_KEY; keys.GEOAPIFY_SECRET_API_KEY

from flask import Flask, render_template, request

import linkright

app = Flask(__name__)


@app.route('/')
def input():
    return render_template('input.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        current_location = request.form['curr_location_input']
        direction = request.form['drop_down']
        radius = request.form['radius_input']
        nearby_lrstops = linkright.next_train(direction, radius)
        for station in nearby_lrstops:
            station_key = station
            dist_to_station = nearby_lrstops[0]
            time_to_station = nearby_lrstops[1]
            next_trains = [nearby_lrstops[2], nearby_lrstops[3], nearby_lrstops[4]]
        return render_template('results.html', current_location=current_location, station_key=station_key, dist_to_station=dist_to_station, time_to_station=time_to_station, next_trains=next_trains)
    else:
        return 'Error: was expecting a POST request', 400





