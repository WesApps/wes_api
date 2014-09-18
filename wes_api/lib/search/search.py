from pymongo import MongoClient

client = MongoClient() 
db = client.wes_api

"""
EVENTS SEARCH
"""
def get_all_events(numEvents):
	"""
	Returns numEvents MAX latest events from the DB
	"""
	results = db.events.find()
	if results.count() == 0:
		print "Found no events, panic"
		return None
	sorted_results = results.sort('time')
	

	if numEvents < sorted_results.count():
		return list(sorted_results[0:numEvents])
	else:
		return list(sorted_results)

def get_wesleying_events(numEvents):
	
	pass

def get_wesleyanEvents_events(numEvents):
	print "NOt YEt IMPLEMEntEd"
	pass


"""
MENUS SEARCH
"""
# def get_menus_all(numResults):
