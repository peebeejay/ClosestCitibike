import math


def create_final_list(_station_data_list, _partySize=1, _stationReq=3):
    tempBikeList = []
    tempDockList = []

    # Collect 3 closest stations with available bikes >= party size
    for station in _station_data_list:
        if len(tempBikeList) == _stationReq:
            break
        if station['num_bikes_available'] >= _partySize:
            tempBikeList += [station]

    # Collect 3 closest stations with available docks >= party size
    for station in _station_data_list:
        if len(tempDockList) == _stationReq:
            break
        if station['num_docks_available'] >= _partySize:
            tempDockList += [station]

    # returns tuple containing top 3 closest stations with available bikes & docks that meet constraints
    return (tempBikeList, tempDockList)


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


