from lib.scraping.wesleying import wesleying
from lib.scraping.wesleyanEvents import wesleyanEvents
from lib.scraping.wesleyanMenus import usdanMenus
from lib.scraping.filmSeries import film_series
from lib.db import db

SCRAPE_WESLEYING = True
SCRAPE_WESLEYAN_EVENTS = True
SCRAPE_USDAN = True
SCRAPE_STATIC_MENUS = True
SCRAPE_FILM_SERIES = True

def initialize():
	clear_all_sources()
	scrape_all_sources()
	populate_static_menus()

def scrape_all_sources():
	"""
	Calls all of the scraping methods from all 
	of the scraping sources imported above.
	TODO: Multi-threading
	"""
	print "SCRAPER: Scraping all sources"
	print "SCRAPER: Scraping Wesleying"
	result1 = scrape_wesleying()
	print "SCRAPER: Scraping Wesleyan Events"
	result2 = scrape_wesleyan_events()
	print "SCRAPER: Scraping Usdan Menus"
	result3 = scrape_usdan_menus()
	print "SCRAPER: Scraping Film Series"
	result4 = scrape_film_series()
	if not result1 and result2 and result3 and result4:
		print "SCRAPER: ERROR, UNABLE TO SCRAPE ALL SOURCES"
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

def clear_wesleyan_events():
	if not db.remove_events_by_source("Wesleyan Events"):
		print "UNABLE TO CLEAR WESLEYAN EVENTS"
		return False
	return True

def scrape_wesleying():
	# scrape Wesleying
	if not SCRAPE_WESLEYING:
		return True
	wesleying_results = wesleying.scrape_wesleying()
	#add to db
	for res in wesleying_results:
		add_result = db.add_event(res)
		if not add_result:
			print "AHH COULND'T ADD"
	return True

def scrape_wesleyan_events():
	# scrape Wesleyan Events
	if not SCRAPE_WESLEYAN_EVENTS:
		return True

	wesleyan_events_results = wesleyanEvents.scrape_wesleyan_events()
	#add to db
	for res in wesleyan_events_results:
		add_result = db.add_event(res)
		if not add_result:
			print "AHH COULND'T ADD"
	return True

def scrape_usdan_menus():
	# scrape Wesleyan Menus
	if not SCRAPE_USDAN:
		return True
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

def populate_static_menus():
	try:
		db.populate_static_menus()
		return True
	except:
		return False
		
def scrape_film_series():
	if not SCRAPE_FILM_SERIES:
		return True
	film_series_results = film_series.scrape_film_series()
	if not film_series_results:
		print "No film series results"
		return False
	for item in film_series_results:
		result = db.add_film_event(item)
		if not result:
			print item,"failed to add to db"
	return True

def remove_all_films():
	if not db.remove_all_films():
		print "UNABLE TO CLEAR FILM SERIES"
		return False
	return True
# scrape WesMaps

# scrape Wesleyan Hours
