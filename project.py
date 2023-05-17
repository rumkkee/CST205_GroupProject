from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
import requests, json
from pprint import pprint

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fuel_Finder_205'
bootstrap = Bootstrap(app)

class Location(FlaskForm):
    location = StringField(
        'Input Address',
        validators=[DataRequired()]
    )

# stationInfo will store a dictionary with the name, address, and phone number of the nearest fuel station.
stationInfo = {}

## NearestStations API Setup ##

url = 'https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?'

payload = {
    'api_key' : 'nt85Bjlno2VSkWDsjD1HbbgCTlenN7QQJ6vKZWI4',
    'location' : 'Marina+CA', # placeholder value the user can reassign
    'fuel_type' : 'ELEC',
    'limit' : '1'
}

#This functionTakes in a location as a string, then sets that as the location in our payload.
#It also calls the API with this redefined payload, and returns the requested data.
def GetNearestStation(location):
    payload['location'] = location
    response = (requests.get(url, payload))
    try:
        myRequest = requests.get(url, payload)
        data = myRequest.json()
        myStation = data['fuel_stations'][0] 
        print(myStation)
        return myStation
    except:
        print('Request failed')

# This function takes in the data of a station, and 
# reassigns a dictionary containing that same relevant data. Returns that dictionary
def SetStationInfo(myStation):
    global stationInfo
    stationInfo = dict(
        name = str(myStation['station_name']),
        phone = str(myStation['station_phone']),
        address = (f"{myStation['street_address']}, {myStation['city']} {myStation['state']} ({myStation['zip']})"),
        distance = (f"{myStation['distance']} mi ({myStation['distance_km']} km)")
    )
    #print(stationInfo)
    return myStation

##############

@app.route('/', methods=('GET','POST'))
def index():
    myForm = Location()
    if myForm.validate_on_submit():
        myStation = GetNearestStation(myForm.location.data)
        stationInfo = SetStationInfo(myStation)
        return redirect('/location')
    return render_template('index.html', form=myForm)

@app.route('/location', methods=('GET','POST'))
def location():
    # myStation is the alternative that doesn't currently work. myStation's goal is to only use one dictionary,
    # rather than append to a list of dictionaries like "totalStations" does 
    return render_template('location.html', totalStations=totalStations, station=stationInfo)

if __name__ == '__main__':
    app.run(debug=True)   
