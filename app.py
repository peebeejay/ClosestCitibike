from flask import Flask, render_template, jsonify, request
from Citibike import APICall, process_list, create_final_list
import logging, sys, os, json, requests




app = Flask(__name__)


@app.route('/')
def citibike():
    return render_template('citibike.html')


@app.route("/receive_coord")
def receive_coord():
    a_lat = request.args.get('lat', 0, type=float)
    a_lon = request.args.get('lon', 0, type=float)
    print("Coordinates:", a_lat, ", ", a_lon)
    partySize = 1
    stationReq = 5

    # Call the Citibike API and get the latest station data
    station_information = CitibikeAPICaller.getStationInfo()[0]
    station_status = CitibikeAPICaller.getStationStatus()[0]
    print("---> Data is Fresh as of: ", str(CitibikeAPICaller.getStationStatus()[1]))

    # Process data received from Citibike API
    station_data_list = process_list(station_status, station_information, a_lat, a_lon)
    final = create_final_list(station_data_list, pSize=partySize, statReq=stationReq)
    return jsonify(result=final)


CitibikeAPICaller = APICall(interval=30)

if __name__ == "__main__":
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    app.run()
