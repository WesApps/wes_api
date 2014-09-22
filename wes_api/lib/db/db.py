from pymongo import MongoClient
import datetime
import csv

client = MongoClient()
db = client.wes_api
events = db.events
usdan_menus = db.usdan_menus
late_night_menu = db.late_night_menu
summerfields_menu = db.summerfields_menu
film_series = db.film_series

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
		return False

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

def remove_events_by_source(sourceName):
	"""
	Removes all event documets with source == sourceName
	"""
	try:
		events.remove({'source':sourceName})
		return True
	except:
		print 'Unable to remove events from source',sourceName
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
def populate_static_menus():
	try:
		print "Populating static menus"
		populate_static_menu("static/summerfields_menu.csv",summerfields_menu)
		populate_static_menu("static/late_night.csv",late_night_menu)
		return True
	except:
		print "Populating static menus failed"
		return False

def populate_static_menu(csv_file,target_db):
	"""
	csv_file is a string.
	Reads from late_night.csv and summerfields_menu.csv
	and adds them to db.late_night_menu and db.summerfields_menu
	"""
	reader = csv.DictReader(file(csv_file))
	
	for line in reader:
		title = line.get('item')
		item_filter = line.get('filter')
		description = line.get('description')
		price = line.get('price')
		obj = {
				"title":title,
				"filter":item_filter,
				"description":description,
				"price":price
			}
		#if it does not exist, insert it.
		if target_db.find(obj).count() == 0:
			target_db.insert(obj)

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
			"dinner":processed_meals.get('dinner'),
			"brunch":processed_meals.get('brunch')
		}
		usdan_menus.insert(processed_day_item)
		return True
	except:
		print "Unable to add usdan day,",day_item
		return False

def remove_all_menus():
	"""
	Removes all events from the DB
	"""
	try:
		usdan_menus.drop()
		summerfields_menu.drop()
		late_night_menu.drop()
		print 'Dropped Menus DB'
		return True
	except:
		print 'Unable to drop menus DB'
		return False


"""
FILM SERIES METHODS
"""
def add_film_event(film_event):
	if film_series.find(film_event).count() == 0:
		print "Have film, done."
		return True
	try:
		film_series.insert(film_event)
		return True
	except:
		print 'Unable to add film event, can\'t add to db',film_event
		return False

def remove_all_films():
	try:
		film_series.drop()
		print 'Dropped Film Series DB'
		return True
	except:
		print 'Unable to drop Film Series DB'
		return False