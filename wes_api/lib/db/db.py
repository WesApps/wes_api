from pymongo import MongoClient
import logging
import datetime

path = "db.log"
# path = "weshappening.log"
# logging.basicConfig(filename=path, level=logging.DEBUG,
                        # format="%(asctime)s: %(message)s")
client = MongoClient()
db = client.wes_api
events = db.events
usdan_menus = db.usdan_menus

"""
EVENT DB METHODS
"""
def add_event(event):
	"""
	Upserts the event. Returns False if unable to upsert.
	Uses 'name' of event as unique ID
	"""
	#ensure event['name'] exists
	name = event.get('name')
	if not name:
		print 'Unable to upsert event, no name',event
		return False
	try:
		events.update({'name':name},event,True)
		return True
	except:
		print 'Unable to upsert event, can\'t add to db',event

def remove_event_by_name(eventName):
	"""
	Removes one instance of the event with 'name' == 'eventName'
	if it exists, otherwise do nothing.
	"""
	try:
		events.remove({'name':eventName})
		return True
	except:
		print 'Unable to remove event',eventName
		return False

def remove_all_events():
	"""
	Removes all events from the DB
	"""
	try:
		events.drop()
		print 'Dropped events DB'
		return True
	except:
		print 'Unable to drop events DB'
		return False


"""
MENU DB METHODS
"""
def flatten_meal_item(meal_item):
	"""
	Input: <meal_items> is in the form:
		[
			[category,title,extra],
			...
		]
	Output: dictionaries, each one containing
		a list of items w/extra text that fall into the 
		category.
		
		{'stockpot':[
						{
							'title':'oatmeal',
							'extra':'decent'
						},...
					]
		},
		{'classics'
		}
	"""
	categories = {}
	for meal in meal_item:
		meal_category = meal[0]
		meal_data = {'title':meal[1],'extra':meal[2]}
		if meal_category not in categories:
			categories[meal_category] = [meal_data]
		else:
			categories[meal_category].append(meal_data)
	return categories

def add_usdan_day(day_item):
	"""
	Unique ID for each day item is the time attr.
	Assumes a day_item is in the form:
	{
		'time': <time>,
		'breakfast':<meal_items>,
		'lunch':<meal_items>,
		'dinner':<meal_items>,
		'brunch'...
	}y

	where <meal_items> is in the form:
	[
		[category,title,extra],
		...
	]
	"""
	try:
		raw_day_time = day_item['time']
		day_time = datetime.datetime.strptime(raw_day_time,'%a, %d %b %Y')
		
		# if we already have the item, can stop.
		print usdan_menus.find({'time':day_time}).count()
		if usdan_menus.find({'time':day_time}).count() != 0:
			return True

		processed_meals = {}
		meals = ['breakfast','lunch','dinner','brunch']
		for meal in meals:
			raw_meal = day_item.get(meal)
			if raw_meal:
				dict_meal = flatten_meal_item(raw_meal)
				processed_meals[meal] = dict_meal

		processed_day_item = {
			"time":day_time,
			"breakfast":processed_meals.get('breakfast'),
			"lunch":processed_meals.get('lunch'),
			"dinner":processed_meals.get('dinner')
		}
		usdan_menus.insert(processed_day_item)
		return True
	except:
		print "Unable to add usdan day,",day_item
		return False