from lib.scraping.wesleying import wesleying
from lib.scraping.wesleyanEvents import wesleyanEvents
from lib.scraping.wesleyanMenus import usdanMenus
from lib.db import db

SCRAPE_WESLEYING = True
SCRAPE_WESLEYAN_EVENTS = True
SCRAPE_USDAN = True
SCRAPE_STATIC_MENUS = True
SCRAPE_FILM_SERIES = True

def scrape_all_sources():
	"""
	Calls all of the scraping methods from all 
	of the scraping sources imported above.
	TODO: Multi-threading
	"""
	result1 = scrape_wesleying()
	result2 = scrape_wesleyan_events()
	result3 = scrape_usdan_menus()
	result4 = scrape_film_series()
	if not result1 and result2 and result3:
		print "UNABLE TO SCRAPE ALL SOURCE"
		return False
	return True

def clear_all_sources():
	"""
	Drop.
	"""
	result1 = db.remove_all_events()
	result2 = db.remove_all_menus()
	result3 = db.remove_all_films()
	if not result1 and result2 and result3:
		print "UNABLE TO CLEAR ALL SOURCES"
		return False
	return True

def clear_wesleying():
	if not db.remove_events_by_source("Wesleying"):
		print "UNABLE TO CLEAR WESLEYING"
		return False
	return True

def clear_wesleying():
	if not db.remove_events_by_source("Wesleyan Events"):
		print "UNABLE TO CLEAR WESLEYAN EVENTS"
		return False
	return True

def scrape_wesleying():
	# scrape Wesleying
	if SCRAPE_WESLEYING:
		wesleying_results = wesleying.scrape_wesleying()
		#add to db
		for res in wesleying_results:
			add_result = db.add_event(res)
			if not add_result:
				print "AHH COULND'T ADD"
		return True
	return True

def scrape_wesleyan_events():
	# scrape Wesleyan Events
	if SCRAPE_WESLEYAN_EVENTS:
		wesleyan_events_results = wesleyanEvents.scrape_wesleyan_events()
		#add to db
		for res in wesleyan_events_results:
			add_result = db.add_event(res)
			if not add_result:
				print "AHH COULND'T ADD"
		return True
	return True

def scrape_usdan_menus():
	# scrape Wesleyan Menus
	if SCRAPE_USDAN:
		usdan_results = usdanMenus.fetch_all()
		usdan_items = usdan_results.get('Usdan')
		if not usdan_items:
			print "No usdan items from fetch"
			return False
		for item in usdan_items:
			result = db.add_usdan_day(item)
			if not result:
				print item,"failed to add to db"
		return True
	return True

def populate_static_menus():
	db.populate_static_menus()

	# scrape WesMaps

	# scrape Wesleyan Hours
