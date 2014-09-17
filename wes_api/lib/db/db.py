from pymongo import MongoClient
import logging
import lib

path = "db.log"
# path = "weshappening.log"
logging.basicConfig(filename=path, level=logging.DEBUG,
                        format="%(asctime)s: %(message)s")
client = MongoClient()
db = client.wes_api

def addEvent(event):
	"""
	Upserts the event. Returns False if unable to upsert.
	Uses 'name' of event as unique ID
	"""
	#ensure event['name'] exists
	name = event.get('name')
	if not name:
		logging.debug('Unable to upsert event, no name',event)
		return False
	try:
		db.events.update({'name':name},event,True)
		return True
	except:
		logging.debug('Unable to upsert event, can\'t add to db',event)

def removeEventByName(eventName):
	"""
	Removes one instance of the event with 'name' == 'eventName'
	if it exists, otherwise do nothing.
	"""
	try:
		db.events.remove({'name':eventName})
		return True
	except:
		logging.debug('Unable to remove event',eventName)
		return False

def removeAllEvents():
	"""
	Removes all events from the DB
	"""
	try:
		db.events.drop()
		logging.debug('Dropped events DB')
		return True
	except:
		logging.debug('Unable to drop events DB')
		return False

