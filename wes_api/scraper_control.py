from lib.scraping.wesleying import wesleying
from lib.scraping.wesleyanEvents import wesleyanEvents
from lib.scraping.wesleyanMenus import usdanMenus
from lib.db import db

SCRAPE_WESLEYING = True
SCRAPE_WESLEYAN_EVENTS = True
SCRAPE_USDAN = True

def scrape_all_sources():
	"""
	Calls all of the scraping methods from all 
	of the scraping sources imported above.
	TODO: Multi-threading
	"""
	scrape_wesleying()
	scrape_wesleyan_events()
	scrape_usdan_menus()

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
	return False

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
	return False

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





	# scrape WesMaps

	# scrape Wesleyan Hours
