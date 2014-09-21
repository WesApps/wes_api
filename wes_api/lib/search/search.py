import pymongo
import datetime

MongoClient = pymongo.MongoClient

client = MongoClient() 
db = client.wes_api
events = db.events
usdan_menus = db.usdan_menus
summerfields_menu = db.summerfields_menu
late_night_menu = db.late_night_menu

"""
EVENTS SEARCH
"""

def limit_results(numResults,results):
	"""
	Limits results to numResults
	"""
	if numResults < results.count():
		return list(results[0:numResults])
	else:
		return list(results)

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
	return limit_results(numEvents,sorted_results)
	

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
	usdan = get_usdan(numResults)
	summerfields = get_summerfields_menu()
	late_night = get_late_night_menu()
	return {"usdan":usdan,
			"summerfields":summerfields,
			"late_night":late_night}

def get_menus_today():
	now = datetime.datetime.today()
	start_today = datetime.datetime(now.year,now.month,now.day)
	usdan = get_usdan(1,start_today) 

	summerfields = get_summerfields_menu()
	late_night = get_late_night_menu()
	return {"usdan":usdan,
			"summerfields":summerfields,
			"late_night":late_night}

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

	return limit_results(numResults,sorted_results)

def get_summerfields_menu():
	return get_static_menu(summerfields_menu)

def get_late_night_menu():
	return get_static_menu(late_night_menu)

def get_static_menu(target_db):
	"""
	Not worried about time here since these menus
	don't change on a daily basis.
	"""
	results = target_db.find()
	if results.count() == 0:
		print "Found no static meals"
		return None
	return list(results)