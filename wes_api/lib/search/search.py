import pymongo
import datetime

MongoClient = pymongo.MongoClient

client = MongoClient() 
db = client.wes_api
events = db.events
usdan_menus = db.usdan_menus

"""
EVENTS SEARCH
"""
def get_events(numEvents,source=None):
	"""
	Returns numEvents MAX latest events from the DB
	"""
	if source:
		results = db.events.find({'source':source})
	else:
		results = db.events.find()
	if results.count() == 0:
		print "Found no events"
		return None
	sorted_results = results.sort('time',pymongo.DESCENDING)

	if numEvents < sorted_results.count():
		return list(sorted_results[0:numEvents])
	else:
		return list(sorted_results)

def search_events(numResults,title_query,location_query,
					time_from,time_until,category_query,source):
	"""
	To minimize search space, search hierarchically.
	Order of search:
		-source
		-category_query
		-time_from AND time_until
		-location_query
		-title_query
	Then restrict results to numResults.
	"""
	print "Not yet implemented. Will be slightly painful."
	pass

"""
MENUS SEARCH
"""
def get_menus_all(numResults):
	return get_usdan(numResults)

def get_menus_today():
	now = datetime.datetime.today()
	start_today = datetime.datetime(now.year,now.month,now.day)
	return get_usdan(1,start_today,start_today)


def get_usdan(numResults,time_from=None,time_until=None):
	# grab time_from to present
	if time_from and not time_until:
		usdan_results=usdan_menus.find({"time":{"$gte":time_from}})
	
	# grab from beginning to time_until
	elif not time_from and time_until:
		usdan_results=usdan_menus.find({"time":{"$lte":time_until}})

	# grab time_from to time_until
	elif time_from and time_until:
		usdan_results=usdan_menus.find({"time":{"$lte":time_until,"$gte":time_from}})

	# grab all
	else:
		usdan_results = usdan_menus.find()
	if usdan_results.count() == 0:
		print "Found no usdan meals"
		return None
	sorted_results = usdan_results.sort('time',pymongo.DESCENDING)

	if numResults < sorted_results.count():
		return list(sorted_results[0:numResults])
	else:
		return list(sorted_results)