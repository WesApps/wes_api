from flask import Flask, request
from lib.scraping.wesleying import wesleying
from api import api

app = Flask(__name__)

app.register_blueprint(api,url_prefix='/api')


#TODO: Create playground to do basic api calls and see data
@app.route('/')
def index():
    return "Welcome to the Wesleyan API. Get your info here."