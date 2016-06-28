from flask import Flask, render_template, jsonify, request
import time
import logging
import sys
import requests
import threading
import Citibike


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

    global station_information
    global station_status

    station_information = CitibikeAPICaller.getStationInfo()[0]
    station_status = CitibikeAPICaller.getStationStatus()[0]
    print("---> Data is Fresh as of: ", str(CitibikeAPICaller.getStationStatus()[1]))

    # Process data received from Citibike API
    station_data_list = Citibike.process_list(station_status, station_information, a_lat, a_lon)
    final = Citibike.create_final_list(station_data_list, pSize=partySize, statReq=stationReq)
    return jsonify(result=final)


class APICall(object):
    def __init__(self, interval=30):
        self.interval = interval
        self.station_information = {}
        self.station_status = {}
        self.t1 = time.asctime()
        self.t2 = time.asctime()

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        while True:
            time.sleep(self.interval)

            self.station_status = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json').json()['data']['stations']
            self.station_information = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json').json()['data']['stations']
            self.t1 = time.asctime()
            self.t2 = time.asctime()
            print('Arrival Of Fresh Data --->', "|", time.asctime())

    def getStationStatus(self):
        return self.station_status, self.t1

    def getStationInfo(self):
        return self.station_information, self.t2


CitibikeAPICaller = APICall(interval=30)

if __name__ == "__main__":
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)

    app.run()



