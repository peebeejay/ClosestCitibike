import math


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


