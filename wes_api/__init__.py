from flask import Flask, request, render_template
from lib.scraping.wesleying import wesleying
from api import api
import scraper_control
import json
import os

app = Flask(__name__)

app.register_blueprint(api,url_prefix='/api')


#TODO: Create playground to do basic api calls and see data
# and display the exact API call used
@app.route('/')
def index():
	print os.listdir('wes_api/templates')
	return render_template('index.html')

@app.route('/update')
def update():
	return json.dumps({"Success?":scraper_control.scrape_all_sources()})

@app.route('/clearAll')
def clearAll():
	return json.dumps({"Cleared?":scraper_control.clear_all_sources()})