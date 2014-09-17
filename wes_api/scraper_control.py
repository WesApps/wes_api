from lib.scraping.wesleying import wesleying
from lib.scraping.wesleyanEvents import wesleyanEvents
from lib.db import db

SCRAPE_WESLEYING = False
SCRAPE_WESLEYAN_EVENTS = True



def scrape_all_sources():
	"""
	Calls all of the scraping methods from all 
	of the scraping sources imported above.
	TODO: Multi-threading
	"""
	# scrape Wesleying
	if SCRAPE_WESLEYING:
		wesleying_results = wesleying.scrape_wesleying()
		#add to db
		for res in wesleying_results:
			add_result = db.add_event(res)
			if not add_result:
				print "AHH COULND'T ADD"

	# scrape Wesleyan Events
	if SCRAPE_WESLEYAN_EVENTS:
		wesleyan_events_results = wesleyanEvents.scrape_wesleyan_events()
		#add to db
		for res in wesleyan_events_results:
			add_result = db.add_event(res)
			if not add_result:
				print "AHH COULND'T ADD"
		return True

	# scrape WesMaps

	# scrape Wesleyan Hours

	# scrape Wesleyan Menus