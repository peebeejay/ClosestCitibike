from flask import Flask, render_template, jsonify, request
import Citibike
import requests

app = Flask(__name__)


@app.route('/')
def citibike():
    return render_template('citibike.html')


@app.route("/receive_coord")
def receive_coord():
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

if __name__ == '__main__':
    app.run()
