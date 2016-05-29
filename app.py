from flask import Flask
import pprint
import requests


app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/citibike')
def citibike():
    r = requests.get('https://gbfs.citibikenyc.com/gbfs/gbfs.json')
    d = r.json()
    list_keys = d.keys()
    print(type(d['data']))
    print(d['data']['en']['feeds'][0])
    return pprint.pformat(d, indent=4)

@app.route('geo')
def geo():
	return render_template('geolocation.html')



if __name__ == '__main__':
    app.run()
