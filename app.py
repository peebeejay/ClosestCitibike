from flask import Flask, render_template, jsonify, request
import Citibike
import pprint
import requests
import jinja2
import math


app = Flask(__name__)

@app.route('/unused')
def hello_world():
    return render_template('test.html')


@app.route('/citibike_unused')
def citibike():
    # Variables defined below will eventually be entered by the user
    #   a_lat, a_lon : User's geolocation (latitude, longitude) -> Could package as tuple instead
    #   partySize : Size of the user's party; default value -> 3
    #   stationReq : Amount of stations requested by the user; default value -> 3

    a_lat = 40.719040799999995
    a_lon = -73.9827466
    partySize = 1
    stationReq = 3


    # Retrieve station data from Citibike API
    station_status = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json').json()['data']['stations']
    station_information = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json').json()['data']['stations']

    # Process data received from Citibike API
    station_data_list = Citibike.process_list(station_status, station_information, a_lat, a_lon)


    # Create final list of stations based on constraints: bike_req OR dock_req
    # *** Add logic here - Section needs work ***
    final = Citibike.create_final_list(station_data_list, _partySize=partySize, _stationReq=stationReq)

    Citibike.print_station_data_final(final)

    print(type(final))
    print(len(final))

    return render_template('citibike.html', title="Jinja2 Template Test", station_list=final[0])


@app.route('/')
def geo():
    return render_template('citibike.html')


@app.route("/receive_coord")
def receive_coord():

    # lat = request.json['lat']
    # lon = request.json['lon']
    # lat = request.args.get('lat', 0, type=float)
    # lon = request.args.get('lon', 0, type=float)
    #
    # print("Coordinates:", lat, ", ", lon)
    # return jsonify(result=lat+lon)


    a_lat = request.args.get('lat', 0, type=float)
    a_lon = request.args.get('lon', 0, type=float)
    print("Coordinates:", a_lat, ", ", a_lon)
    partySize = 2
    stationReq = 5

    # Retrieve station data from Citibike API
    station_status = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json').json()['data']['stations']
    station_information = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json').json()['data']['stations']

    # Process data received from Citibike API
    station_data_list = Citibike.process_list(station_status, station_information, a_lat, a_lon)

    # Create final list of stations based on constraints: bike_req OR dock_req
    # *** Add logic here - Section needs work ***
    final = Citibike.create_final_list(station_data_list, _partySize=partySize, _stationReq=stationReq)

    Citibike.print_station_data_final(final)

    return jsonify(result=final)



@app.route("/add_numbers")
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print(a, b)
    return jsonify(result=a+b)



if __name__ == '__main__':
    app.run()
