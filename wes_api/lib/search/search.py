import pymongo
import datetime

MongoClient = pymongo.MongoClient

client = MongoClient() 
db = client.wes_api
events = db.events
usdan_menus = db.usdan_menus
summerfields_menu = db.summerfields_menu
late_night_menu = db.late_night_menu
film_series = db.film_series

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
	
def get_events_today():
	now = datetime.datetime.today()
	today = datetime.datetime(now.year,now.month,now.day)
	tomorrow = today + datetime.timedelta(days=1)
	search_results = events.find({"time":{"$gte":today,"$lt":tomorrow}})
	if search_results.count() == 0:
		print "Found no events for today."
		return None
	return list(search_results)

def search_events(numResults,title_query,location_query,
					time_from,time_until,category_query,source):
	"""
	To minimize total search space, search hierarchically.
	This will do only exact matches. Since the amount of event
	data (for now) is relatively small, people can just
	do whatever more-serious searching they want on the 
	front end once they have the data.
	Order of search:
		-source
		-category_query
		-time_from and time_until
		-location_query
		-title_query
	Then restrict results to numResults.
	"""
	# Source Filter
	if source:
		search_results = db.events.find({'source':source})
	else:
		search_results = db.events.find()
	if not search_results:
		print "NO events found in search events"
		return None

	# Category Filter
	if category_query:
		lower_cat = category_query.lower()
		search_results_2 = [i if i['category'].lower() == lower_cat for i in search_results]
	else:
		search_results_2 = search_results

	# Time Filter
	if time_from and not time_until:
		search_results_3 = [i if i['time'] >= time_from for i in search_results_2]
	
	# grab from beginning to time_until
	elif not time_from and time_until:
		search_results_3 = [i if i['time'] <= time_until for i in search_results_2]

	# grab time_from to time_until
	elif time_from and time_until:
		search_results_3 = [i if i['time'] <= time_from and i['time'] <= time_until for i in search_results_2]

	else:
		search_results_3 = search_results_2

	# Location Filter
	if location_query:
		lower_loc = location_query.lower()
		search_results_4 = [i if i['location'].lower() == lower_loc for i in search_results_3]
	else:
		search_results_4 = search_results


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
	today = datetime.datetime(now.year,now.month,now.day)
	tomorrow = today + datetime.timedelta(days=1)
	usdan = get_usdan(1,today,tomorrow) 

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
		usdan_results=usdan_menus.find({"time":{"$lt":time_until,"$gte":time_from}})

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

"""
FILM SERIES SEARCH
"""
def get_film_series_all():
	search_results = film_series.find()
	if search_results.count() == 0:
		print "Found no film series at all...?"
		return None
	return list(search_results)

def get_film_series_today():
	now = datetime.datetime.today()
	today = datetime.datetime(now.year,now.month,now.day)
	tomorrow = today + datetime.timedelta(days=1)
	search_results = film_series.find({"time":{"$gte":today,"$lt":tomorrow}})
	if search_results.count() == 0:
		print "Found no film for today."
		return None
	return list(search_results)
