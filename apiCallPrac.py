from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests, json
from pprint import pprint

def printInfo(myStation, count):
    pprint(f"Station {count + 1}: {myStation['station_name']}")
    pprint(f"    Distance: {shortenDecimal(str(myStation['distance']))} mi ({shortenDecimal(str(myStation['distance_km']))} km)")
    pprint(f"    Address: {myStation['street_address']}, {myStation['city']} {myStation['state']} ({myStation['zip']})")
    pprint(f"    Number: {myStation['station_phone']}")

def shortenDecimal(myString):
    miles = ''
    for i in range(0, len(myString)):
        miles += myString[i]
        if (myString[i + 1]) == '.':
            miles += myString[i + 1]
            miles += myString[i + 2]
            return miles
    return miles


url = 'https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?'

payload = {
    'api_key' : 'nt85Bjlno2VSkWDsjD1HbbgCTlenN7QQJ6vKZWI4',
    'location' : 'Marina+CA',
    'fuel_type' : 'ELEC',
    'limit' : '4'
}

response = (requests.get(url, payload))

try:
    myRequest = requests.get(url, payload)
    data = myRequest.json()

    ################# Print tests
    # pprint(data) #prints all data
    # pprint(data['fuel_stations']) # returns all information relating to fuel stations in this fuel station
    # pprint(data['fuel_stations'][0]['station_name']) # returns values in nested key 'station_name'
    # pprint(data['fuel_stations'][0]['street_address'])
    # pprint(data['fuel_stations'][0]['city'])
    # pprint(data['fuel_stations'][0]['state'])
    # pprint(data['fuel_stations'][0]['zip'])

    #Below: Stores a portion of the "dictionary" to reduce the amount passed in to print parameter
    #myStation = data['fuel_stations'][0] 
    
    #pprint(myStation['station_phone'])
    #pprint(f"Address: {myStation['street_address']}, {myStation['city']} {myStation['state']} ({myStation['zip']})")
    #pprint(f"Distance from Address: {myStation['distance']} mi ({myStation['distance_km']} km)") # this prints with several trailing decimals
    ################### getting counter of stations returned, which may be less than 'limit' parameter
    print("\n\nBeginning loop:")
    for i in range(0, len(data['fuel_stations'])):
        myStation = data['fuel_stations'][i]
        printInfo(myStation, i)
        
    ###################### 

except:
    print('Request failed')



# if response.status_code == 200:
#     data = response.json()
# else:
#     print('Request failed')

# latitude
# longitude
# date_last_confirmed
# 
# ev_pricing
# ev_renewable_source
# ev_network (name of ev brand)
#
# access_days_time
# cards_accepted
#

### Attributes of stations
# fuel_type_code (type of fuel)
# station_name
# street_address
# city
# state
# zip
#
# station_phone
# station_code (current availability)
