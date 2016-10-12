# Contains functions related to the processing of location coordinates and chatbot messages
# This is a module that is supplementary to app.py

import math, threading, time, requests, googlemaps, os, json


class APICall(object):
    # Daemon process that continuously calls the Citibike API in n second increments
    def __init__(self, interval=30):
        self.interval = interval
        self.station_information = {}
        self.station_status = {}
        self.t1 = time.asctime()

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        while True:
            self.station_status = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json').json()['data']['stations']
            self.station_information = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json').json()['data']['stations']
            self.t1 = time.asctime()
            print('Arrival Of Fresh Data --->', "|", time.asctime())
            time.sleep(self.interval)

    def getStationStatus(self):
        return self.station_status, self.t1

    def getStationInfo(self):
        return self.station_information, self.t1



def createFinalList(statData, pSize=1, statReq=5):
    # Create a tuple that contains a list of n stations that contain open bikes & n stations that contain open docks
    bikeList = []
    DockList = []

    # Collect N closest stations with available bikes >= party size
    for station in statData:
        if len(bikeList) == statReq:
            break
        if station['num_bikes_available'] >= pSize:
            bikeList += [station]

    # Collect N closest stations with available docks >= party size
    for station in statData:
        if len(DockList) == statReq:
            break
        if station['num_docks_available'] >= pSize:
            DockList += [station]

    # returns tuple containing top N closest stations with available bikes & docks that meet constraints
    return bikeList, DockList


def processList(stationStatus, stationInfo, _alat, _alon):
    # Sorts the list of stations based on distance to the user's inputted location
    statDataList = []

    statData = {stationInfo[i]['station_id']: stationInfo[i] for i in range(0, len(stationInfo))}
    dictStatInfo = {stationStatus[i]['station_id']: stationStatus[i] for i in range(0, len(stationStatus))}

    for key in statData.keys():
        # Transfers num_bikes & num_docks from station_info to station_data
        statData[key]['num_bikes_available'] = dictStatInfo[key]['num_bikes_available']
        statData[key]['num_docks_available'] = dictStatInfo[key]['num_docks_available']

        # Calculate vector between your location & citibike station
        b_lat = statData[key]['lat']
        b_lon = statData[key]['lon']
        statData[key]['vector'] = (b_lat - _alat, b_lon - _alon)

        # Calculate vector magnitude
        statData[key]['magnitude'] = math.sqrt(statData[key]['vector'][0] ** 2 + statData[key]['vector'][1] ** 2)
        statDataList += [statData[key]]

    return sorted(statDataList, key=lambda k: k['magnitude'], reverse=False)


def validLocation(lat, lon):
    # Checks whether requested location is within 75 miles of New York City
    lat_nyc = 40.712700
    lon_nyc = -74.005900
    if (math.sqrt((lat-lat_nyc)**2 + (lon-lon_nyc)**2))*110 >75:
        return False
    else:
        return True


def ChatbotStations(final, address):
    # Creates output messages for Chatbot

    sb = "Showing results for " + address + "\n\nBikes\n"
    for item in final[0]:
        sb += str(item["name"] + ": " + str(item["num_bikes_available"]) + " bikes\n")

    sd = "Docks\n"
    for item in final[1]:
        sd+= str(item["name"] + ": " + str(item["num_docks_available"]) + " docks\n")

    sd+= "\nFor map view visit closestcitibike.com"
    return sb, sd



## Chatbot Message Processing Functions
def processMessage(message):
    # Processes all incoming messages from facebook. Uses a function dispatcher dictionary for.. polymorphism

    # Invalid location string message
    invalid = "Send us your location or enter a location name"

    # Dispatcher dictionary containing message type evaluation & processing functions
    dispatcher = {textMessage: processText, mapMessage: processMap}

    # Checks if message matches a known type. If so, processes message with corresponding function
    for key in dispatcher.keys():
        if key(message):
            return dispatcher[key](message)
    return [invalid]


def textMessage(m):
    # Checks if a sent message is a Text-type message. Returns True if text message, False otherwise
    return "text" in m["message"].keys()


def mapMessage(m):
    # Checks if a sent message is a Map-type message. Returns True if map message, False otherwise
    if "attachments" in m["message"].keys():
        if "payload" in m["message"]["attachments"][0].keys() and m["message"]["attachments"][0]["payload"]:
            if "coordinates" in m["message"]["attachments"][0]["payload"].keys():
                return True
    return False


def processText(m):
    # Processes a Text-Type message and returns an appropriate response

    specify = "Be more specific or add 'New York' to your location"
    geocode_results = gmaps.geocode(m["message"]["text"])

    if len(geocode_results) > 0:
        a_lat = geocode_results[0]['geometry']['location']['lat']
        a_lon = geocode_results[0]['geometry']['location']['lng']
        fAddress = geocode_results[0]["formatted_address"]

        if validLocation(a_lat, a_lon):
            final = processCoords(a_lat, a_lon, stationReq_=3, partySize_=1)
            return [ChatbotStations(final, fAddress)[0], ChatbotStations(final, fAddress)[1]]
        else:
            return [specify]
    else:
        return [specify]


def processMap(m):
    # Processes a Map-Type message and returns an appropriate response based on location validity
    a_lat = m["message"]["attachments"][0]["payload"]["coordinates"]["lat"]
    a_lon = m["message"]["attachments"][0]["payload"]["coordinates"]["long"]

    final = processCoords(a_lat, a_lon, stationReq_=3, partySize_=1)

    fAddress = gmaps.reverse_geocode((a_lat, a_lon))[0]["formatted_address"]
    return [ChatbotStations(final, fAddress)[0], ChatbotStations(final, fAddress)[1]]


def processCoords(lat, lon, stationReq_, partySize_):
    # Returns a list of valid stations sorted by distance from the user

    # Print the inputted latitude and longitude to console
    print("Lat: " + str(lat))
    print("Lon: " + str(lon))

    # Call the Citibike API and get the latest station data
    station_information = APICaller.getStationInfo()[0]
    station_status = APICaller.getStationStatus()[0]

    print("---> Data Used for Calculations is Fresh as of: ", str(APICaller.getStationStatus()[1]))

    # Process data received from Citibike API
    station_data_list = processList(station_status, station_information, lat, lon)
    final = createFinalList(station_data_list, pSize=partySize_, statReq=stationReq_)

    return final

def sendMessage(recipientID, messageText):
    # Packages and sends message to facebook graph API

    print("sending message to {recipient}: {text}".format(recipient=recipientID, text=messageText))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipientID
        },
        "message": {
            "text": messageText
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

def main():
    # Define Global Variables
    global APICaller
    APICaller = APICall(interval=30)

    global gmaps
    gmaps = googlemaps.Client(key='AIzaSyCULBWkM7EHcIiQkOqisULz1AswwHkxl_U')
