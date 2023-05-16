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
    # radius = StringField(
    #     'Search Radius',
    #     validators=[DataRequired()]
    # )

myLocation = []
myLoc = ""
def setLocation(location):
    myLocation.append(f"{location}")
    myLoc = (f"{location}")



@app.route('/', methods=('GET','POST'))
def index():
    myForm = Location()
    if myForm.validate_on_submit():
        print("validated")
        print(f"myForm Location data: {myForm.location.data}")
        setLocation(myForm.location.data)
        print(f"My Location: {myLocation}")
        print(f"MyLoc: {myLoc}")
        return redirect('/location')
    return render_template('index.html', form=myForm)

@app.route('/location', methods=('GET','POST'))
def location():
    return render_template('location.html', location=myLocation)



@app.route('/navbar', methods=('GET','POST'))
def navbar():
    myForm = Location()
    if myForm.validate_on_submit():
        print("validated")
    return render_template('navbar.html', form=myForm)

if __name__ == '__main__':
    app.run(debug=True)   

