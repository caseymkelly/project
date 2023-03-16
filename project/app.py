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
        radius = float(request.form['radius_input'])
        nearby_lrstops = linkright.next_train(direction, radius, current_location)
        station_count = len(nearby_lrstops)
        # for station_key, stop_info in nearby_lrstops.items():
        #     dist_to_station = stop_info[0]
        #     time_to_station = stop_info[1]
        #     next_trains = [stop_info[2], stop_info[3], stop_info[4]]
        return render_template('results.html', current_location=current_location, nearby_lrstops=nearby_lrstops, radius=radius, station_count=station_count)
    else:
        return 'Error: was expecting a POST request', 400


app.run(debug=True)


#station_key=station_key, dist_to_station=dist_to_station, time_to_station=time_to_station, next_trains=next_trains