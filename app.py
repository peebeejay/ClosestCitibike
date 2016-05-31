from flask import Flask, render_template, jsonify, request
import pprint
import requests
import jinja2
import math


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('test.html')


@app.route('/citibike')
def citibike():
    a_lat = 40.719040799999995
    a_lon = -73.9827466
    bike_req = 3
    dock_req = 0


    def create_final_list():
        final_list = []
        c = 0

        if bike_req > 0:
            for station in station_data_list:
                if c == bike_req:
                    break
                if station['num_bikes_available'] >= bike_req:
                    final_list += [station]
                    c += 1
        elif dock_req > 0:
            for station in station_data_list:
                if c == dock_req:
                    break
                if station['num_bikes_available'] >= dock_req:
                    final_list += [station]
                    c += 1
        return final_list


    def process_list(_station_status, _station_information, _a_lat, _a_lon):
        _station_data_list = []

        station_data = {_station_information[i]['station_id']: _station_information[i] for i in range(0, len(_station_information))}
        dict_station_information = {_station_status[i]['station_id']: _station_status[i] for i in range(0, len(_station_status))}

        for key in station_data.keys():
            # Transfers num_bikes & num_docks from station_info to station_data
            station_data[key]['num_bikes_available'] = dict_station_information[key]['num_bikes_available']
            station_data[key]['num_docks_available'] = dict_station_information[key]['num_docks_available']

            # Calculate vector between your location & citibike station
            b_lat = station_data[key]['lat']
            b_lon = station_data[key]['lon']
            station_data[key]['vector'] = (b_lat - _a_lat, b_lon - _a_lon)

            # Calculate magnitude
            station_data[key]['magnitude'] = math.sqrt(station_data[key]['vector'][0]**2 + station_data[key]['vector'][1]**2)
            _station_data_list += [station_data[key]]

        return sorted(_station_data_list, key=lambda k: k['magnitude'], reverse=False)


    def print_station_data_all(_station_data_list):
        print("\n")
        for station in _station_data_list:
            print(station['magnitude'], station['name'], 'BA:', station['num_bikes_available'], 'DA:', station['num_docks_available'])


    def print_station_data_final(_final):
        # Print list of closest stations that meets requirements
        for x, station in enumerate(_final):
            print(x, station['magnitude'], station['name'],  'BA:', station['num_bikes_available'], 'DA:', station['num_docks_available'])


    # Retrieve station data from Citibike API
    station_status = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json').json()['data']['stations']
    station_information = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json').json()['data']['stations']

    # Process data received from Citibike API
    station_data_list = process_list(station_status, station_information, a_lat, a_lon)

    # Create final list of stations based on constraints: bike_req OR dock_req
    final = create_final_list()

    print_station_data_final(final)
    print(type(final))
    print(len(final))


    return render_template('citibike.html', title = "Jinja2 Template Test", station_list=final)
    #return render_template('base.html')


@app.route('/geo')
def geo():
    return render_template('geolocation.html')


@app.route("/receive_coord", methods=['POST'])
def receive_coord():
    lat = request.json['lat']
    lon = request.json['lon']

    print("Coordinates:", lat, ", ", lon)
    return jsonify(result=lat+lon)

'''@app.route("/add_numbers")
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print(a, b)
    return jsonify(result=a+b)
'''


if __name__ == '__main__':
    app.run()
