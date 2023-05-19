from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
import requests, json
from pprint import pprint

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# NearestStationAPI implemented by Arturo
# Google Map API implemented by Christian
# CSS and images implemented by David

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fuel_Finder_205'
bootstrap = Bootstrap(app)

class Location(FlaskForm):
    location = StringField(
        'Input Address',
        validators=[DataRequired()]
    )

## NearestStations API Setup ##
url = 'https://developer.nrel.gov/api/alt-fuel-stations/v1/nearest.json?'

payload = {
    'api_key' : 'nt85Bjlno2VSkWDsjD1HbbgCTlenN7QQJ6vKZWI4',
    'location' : 'Marina+CA', # placeholder value the user can reassign
    'fuel_type' : 'ELEC',
    'limit' : '1'
}

#The GetNearestStation function takes in a location as a string, then sets that as the location in our payload.
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


# The SetStationInfo function takes in the data of a station, and 
# reassigns a global dictionary with specific info from the given station, such as it's name, phone, address, and distance from the given address.
def SetStationInfo(myStation):
    global stationInfo
    global mapAddress

    stationInfo = dict(
        name=str(myStation['station_name']),
        phone=str(myStation['station_phone']),
        address=(f"{myStation['street_address']}, {myStation['city']} {myStation['state']} ({myStation['zip']})"),
        distance=(f"{myStation['distance']} mi ({myStation['distance_km']} km)")
    )

    mapAddress1 = str(myStation['street_address'] + ", " + myStation['city'] + " " + myStation['state'] + " (" + myStation['zip'] + ")")
    mapAddress = mapAddress1.replace(" ", "+")
    pprint(stationInfo)
    pprint(mapAddress)

##############

@app.route('/', methods=('GET','POST'))
def index():
    myForm = Location()
    if myForm.validate_on_submit():
        myStation = GetNearestStation(myForm.location.data)
        SetStationInfo(myStation)
        
        return redirect('/location')
    return render_template('index.html', form=myForm)

@app.route('/location', methods=('GET','POST'))
def location():
    pprint(stationInfo)
    return render_template('location.html', myStation=stationInfo, mapAddress = mapAddress)

if __name__ == '__main__':
    app.run(debug=True)   
