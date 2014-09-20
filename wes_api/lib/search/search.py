import pymongo
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
	print "Not yet implemented. Will be slightly painful."
	pass

"""
MENUS SEARCH
"""
def get_menus_all(numResults):
	return get_usdan(numResults)



def get_usdan(numResults,time_from=None,time_until=None):
	usdan_results = usdan_menus.find()
	if usdan_results.count() == 0:
		print "Found no usdan meals"
		return None
	sorted_results = usdan_results.sort('time',pymongo.DESCENDING)

	if numResults < sorted_results.count():
		return list(sorted_results[0:numResults])
	else:
		return list(sorted_results)