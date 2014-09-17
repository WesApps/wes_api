from lib.scraping.wesleying import wesleying

def scrape_all_sources():
	"""
	Calls all of the scraping methods from all 
	of the scraping sources imported above.
	TODO: Multi-threading
	"""
	# scrape Wesleying
	wesleying.scrape_wesleying()

	# scrape Wesleyan Events
	# wesleyanEvents.scrape_wesleyanEvents()

	# scrape WesMaps

	# scrape Wesleyan Hours

	# scrape Wesleyan Menus