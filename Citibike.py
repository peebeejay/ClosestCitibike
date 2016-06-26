import math, threading, time
import app
import unirest


def create_final_list(statData, pSize=1, statReq=3):
    bikeList = []
    DockList = []

    # Collect 3 closest stations with available bikes >= party size
    for station in statData:
        if len(bikeList) == statReq:
            break
        if station['num_bikes_available'] >= pSize:
            bikeList += [station]

    # Collect 3 closest stations with available docks >= party size
    for station in statData:
        if len(DockList) == statReq:
            break
        if station['num_docks_available'] >= pSize:
            DockList += [station]

    # returns tuple containing top 3 closest stations with available bikes & docks that meet constraints
    return (bikeList, DockList)


def process_list(stationStatus, stationInfo, _alat, _alon):
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


def print_station_data_all(_station_data_list):
    print("\n")
    for station in _station_data_list:
        print(station['magnitude'], station['name'], 'BA:', station['num_bikes_available'], 'DA:', station['num_docks_available'])


def print_station_data_final(_final):
    """Print list of closest stations that meets requirements"""

    for station_list in _final:
        for x, station in enumerate(station_list):
            print((x+1), station['magnitude'], station['name'],  'BA:', station['num_bikes_available'], 'DA:', station['num_docks_available'])





class APICall(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval


        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            thread = unirest.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json', headers={ "Accept": "application/json" }, callback=self.callback_station_status)
            thread = unirest.get('https://gbfs.citibikenyc.com/gbfs/en/station_information.json', headers={ "Accept": "application/json" }, callback=self.callback_station_information)
            app.station_information = "success" # This is temporary obviously
            print('Doing something important in the background')
            time.sleep(self.interval)

    def getStationStatus(self):
        # potential to use time.asctime() to create time stamp for tracking purposes
        return (self.station_status, time.time())

    def getStationInfo(self):
        # potential to use time.asctime() to create time stamp for tracking purposes
        return (self.station_information, time.time())


    def callback_station_status(self, response):
        response.code # The HTTP status code
        response.headers # The HTTP headers
        response.body # The parsed response
        response.raw_body # The unparsed response
        print "in callback1", str(time.time())
        # station_status
        self.station_status = response.body['data']['stations']


    def callback_station_information(self, response):
        response.code # The HTTP status code
        response.headers # The HTTP headers
        response.body # The parsed response
        response.raw_body # The unparsed response
        print "in callback2", str(time.time())
        # station_information
        self.station_information = response.body['data']['stations']


# example = ThreadingExample()
# time.sleep(3)
# print('Checkpoint')
# time.sleep(2)
# print('Bye')
