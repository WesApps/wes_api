from flask import Flask, request
from lib.scraping.wesleying import wesleying
from api import api
import scraper_control
import json

app = Flask(__name__)

app.register_blueprint(api,url_prefix='/api')


#TODO: Create playground to do basic api calls and see data
# and display the exact API call used
@app.route('/')
def index():
    return "Welcome to the Wesleyan API. Get your info here."

@app.route('/update')
def update():
	return json.dumps({"Success?":scraper_control.scrape_all_sources()})

@app.route('/clearAll')
def clearAll():
	return json.dumps({"Cleared?":scraper_control.clear_all_sources()})