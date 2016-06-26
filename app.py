from flask import Flask, render_template, jsonify, request
import Citibike
#import requests
import unirest
import time

app = Flask(__name__)

def callback_station_status(response):
      response.code # The HTTP status code
      response.headers # The HTTP headers
      response.body # The parsed response
      response.raw_body # The unparsed response
      print "in callback:", time.time() - t1
      global station_status
      station_status = response.body['data']['stations']
  

def callback_station_information(response):
      response.code # The HTTP status code
      response.headers # The HTTP headers
      response.body # The parsed response
      response.raw_body # The unparsed response
      print "in callback2: ", time.time() - t1
      global station_information
      station_information = response.body['data']['stations']
  
@app.route('/')
def citibike():
    print "Citibike Method before unirest", time.time() - t1
    thread = unirest.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json', headers={ "Accept": "application/json" }, callback=callback_station_status)
    thread = unirest.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json', headers={ "Accept": "application/json" }, callback=callback_station_information)
    print "Citibike Method after unirest", time.time() - t1


    return render_template('citibike.html')


@app.route("/receive_coord")
def receive_coord():
    a_lat = request.args.get('lat', 0, type=float)
    a_lon = request.args.get('lon', 0, type=float)
    print "Coordinates:", a_lat, ", ", a_lon
    partySize = 2
    stationReq = 5
    print "Receive coord", time.time() - t1

    # Retrieve station data from Citibike API
    # station_status = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json').json()['data']['stations']
    # station_information = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json').json()['data']['stations']

    # Process data received from Citibike API
    station_data_list = Citibike.process_list(station_status, station_information, a_lat, a_lon)

    # Create final list of stations based on constraints: bike_req OR dock_req
    # *** Add logic here - Section needs work ***
    final = Citibike.create_final_list(station_data_list, pSize=partySize, statReq=stationReq)

    #Citibike.print_station_data_final(final)

    return jsonify(result=final)


if __name__ == '__main__':
    global t1
    t1 = time.time()
    global station_status
    global station_information
    app.run()
