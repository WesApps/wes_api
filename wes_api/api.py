from lib.search import search
from flask import Blueprint

api = Blueprint('api',__name__,template_folder='templates')

## Events
def get_all_events():
	"""
	Returns all events in the db
	"""
	pass