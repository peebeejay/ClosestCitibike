from flask import Flask
from flask import render_template
import pprint
import requests
import jinja2


app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/citibike')
def citibike():
    r = requests.get('https://gbfs.citibikenyc.com/gbfs/gbfs.json')
    d = r.json()
    list_keys = d.keys()
    return pprint.pformat(d, indent=4)


@app.route('/geo')
def geo():
    #return "Geo"
    return render_template('geolocation.html')

if __name__ == '__main__':
    app.run()
