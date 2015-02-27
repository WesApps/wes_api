from flask import Flask, render_template
from api import api
import scraper_control
import json
import os

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def index():
    print os.listdir('templates')
    return render_template('index.html')


@app.route('/home')
def home():
    print os.listdir('templates')
    return render_template('index.html')


@app.route('/sandbox')
def sandbox_route():
    print os.listdir('templates')
    return render_template('sandbox.html')


@app.route('/documentation')
def documentation():
    print os.listdir('templates')
    return render_template('documentation.html')


@app.route('/about')
def about():
    print os.listdir('templates')
    return render_template('about.html')


# @app.route('/update')
# def update():
#     return json.dumps({"Success?": scraper_control.scrape_all_sources()})


# @app.route('/clearAll')
# def clearAll():
#     return json.dumps({"Cleared?": scraper_control.clear_all_sources()})

@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response

if __name__ == '__main__':
    app.run(debug=True)
