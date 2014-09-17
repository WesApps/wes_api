from pymongo import MongoClient
# import logging

# path = "db.log"
# logging.basicConfig(filename="db.log", level=logging.DEBUG,
                        # format="%(asctime)s: %(message)s")
# logging.debug("Asd")
client = MongoClient() 
db = client.wes_api

def get_events(numEvents):
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

