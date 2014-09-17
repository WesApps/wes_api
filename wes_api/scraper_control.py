from lib.scraping.wesleying import wesleying
from lib.db import db

def scrape_all_sources():
	"""
	Calls all of the scraping methods from all 
	of the scraping sources imported above.
	TODO: Multi-threading
	"""
	# scrape Wesleying
	wesleying_results = wesleying.scrape_wesleying()
	#add to db
	for res in wesleying_results:
		add_result = db.add_event(res)
		if not add_result:
			print "AHH COULND'T ADD"
	return True

	# scrape Wesleyan Events
	# wesleyanEvents.scrape_wesleyanEvents()

	# scrape WesMaps

	# scrape Wesleyan Hours

	# scrape Wesleyan Menus