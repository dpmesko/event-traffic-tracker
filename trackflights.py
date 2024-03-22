import requests
import json
import datetime
import time

# requires OAUTH setup
def getAirportStats(icao):
    response = requests.get("https://api.ivao.aero/v2/airports/" + icao + "/stats")
    data = response.json()

    if response.status_code != 200:
        print("error retrieving data")
        print(data)
        return;

    print(data)


#getAirportStats('KJFK')

def getPilotsAtICAOs(dep = [], arr = []):
    response = requests.get("https://api.ivao.aero/v2/tracker/whazzup")
    data = response.json()

    if response.status_code != 200:
        print("error retrieving data")
        print(response.status_code)
        return;

   
    matchingPilots = []
    for elem in data['clients']['pilots']:
        if elem['flightPlan'] == None:
            continue

        if elem['flightPlan']['departureId'] in dep:
            matchingPilots.append(elem)
        elif elem['flightPlan']['arrivalId'] in arr:
            matchingPilots.append(elem)
    
    return matchingPilots


def dumpFlights(flights, startTime):
    print('\nWRITING FLIGHT LOG FILE...')
    currTime = datetime.datetime.utcnow()
    filePath = 'FLIGHTLOG' + currTime.strftime('%f') + '.txt'
    f = open(filePath, 'at')
    
    f.write('FLIGHT LOG RECORDED FROM ' + startTime.strftime('%c') + ' TO ' + currTime.strftime('%c'))
    f.write('\nDEPARTURE ICAOs: ')
    f.write('\nARRIVAL ICAOs: ')
    f.write('\nNUM FLIGHTS: ' + str(len(flights)))
    f.write('\n\n\n')

    for flight in flights.values():
        f.write(str(flight))
        f.write('\n\n')


    f.close()
    print('DONE, CHECK ' + filePath)


def mainLoop():
    flights = {}
    startTime = datetime.datetime.utcnow()
    try:
      while True:
        print('fetching new flights')
        pilots = getPilotsAtICAOs(['KJFK'])
        print('found ' + str(len(pilots)) + ' matching flights')

        for pilot in pilots:
            if pilot['id'] in flights:
                continue # skip flights we already logged
            else:
                flights[pilot['id']] = pilot

        print('sleeping...')
        time.sleep(15)
    except KeyboardInterrupt:
        print('\n\nSHUTTING DOWN')
        dumpFlights(flights, startTime);
        print('DONE, CYA')


mainLoop()
