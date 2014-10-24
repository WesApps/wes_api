from lib.scraping.wesleying import wesleying
from lib.scraping.wesleyanEvents import wesleyanEvents
from lib.scraping.wesleyanMenus import usdanMenus
from lib.scraping.filmSeries import film_series
from lib.db import db
import time
import datetime

SCRAPE_WESLEYING = True
SCRAPE_WESLEYAN_EVENTS = True
SCRAPE_USDAN = True
SCRAPE_STATIC_MENUS = True
SCRAPE_FILM_SERIES = True
SCRAPE_STATIC_DIRECTORY = True


# For now, everything will be scraped every 10 minutes.
# TODO: Implement smarter timing system so that things
# like events are scraped often, menus scraped daily,
# and film series, wesmaps, hours, etc. scraped only
# once a day or week or even only on specific days or
# times.
SLEEP_TIME = 600


def initialize():
    clear_all_sources()
    populate_static_menus()
    populate_static_directory()
    scrape_all_sources(continuous=False)


"""
events = db.events
usdan_menus = db.usdan_menus
late_night_menu = db.late_night_menu
summerfields_menu = db.summerfields_menu
film_series = db.film_series
"""


def scrape_all_sources(continuous=True):
    """
    Calls all of the scraping methods from all 
    of the scraping sources imported above.
    TODO: Multi-threading
    """
    proceed = True
    while proceed:
        print "SCRAPER: Scraping all sources"
        print "SCRAPER: Scraping Wesleying"
        result1 = scrape_wesleying()
        print "SCRAPER: Scraping Wesleyan Events"
        result2 = scrape_wesleyan_events()
        events_time = datetime.datetime.now()
        print "SCRAPER: Scraping Usdan Menus"
        result3 = scrape_usdan_menus()
        menus_time = datetime.datetime.now()
        print "SCRAPER: Scraping Film Series"
        result4 = scrape_film_series()
        film_series_time = datetime.datetime.now()

        # status: if None, failed to update, will be
        # noted as an offline API until it works. Otherwise,
        # last updated time will update to time given as value.
        status = {"events": None, "menus": None, "film_series": None}
        if result1 and result2:
            status["events"] = events_time
        if result3:
            status["menus"] = menus_time
        if result4:
            status["film_series"] = film_series_time
        print status
        db.update_status(status)

        if not result1 and result2 and result3 and result4:
            # TODO: Update status db
            print "SCRAPER: ERROR, UNABLE TO SCRAPE ALL SOURCES"
            continue

        # TODO: Update status db
        print "SCRAPER: Successfully scraped all sources at:", datetime.datetime.today()
        if not continuous:
            proceed = False
        else:
            print "SCRAPER: Waiting..."
            time.sleep(SLEEP_TIME)


def clear_all_sources():
    """
    Drop.
    """
    result1 = db.remove_all_events()
    result2 = db.remove_all_menus()
    result3 = db.remove_all_films()
    result4 = db.remove_directory_entries()
    if not result1 and result2 and result3 and result4:
        print "SCRAPER: Unable to clear all sources"
        return False
    return True


def clear_wesleying():
    if not db.remove_events_by_source("Wesleying"):
        print "SCRAPER: Unable to clear Wesleying db"
        return False
    return True


def clear_wesleyan_events():
    if not db.remove_events_by_source("Wesleyan Events"):
        print "SCRAPER:Unable to clear Wesleyan Events"
        return False
    return True


def scrape_wesleying():
    # scrape Wesleying
    if not SCRAPE_WESLEYING:
        return True
    try:
        wesleying_results = wesleying.scrape_wesleying()
    except:
        print "SCRAPER: Unable to scrape wesleying"
        return False
    # add to db
    for res in wesleying_results:
        add_result = db.add_event(res)
        if not add_result:
            print "AHH COULND'T ADD"
    return True


def scrape_wesleyan_events():
    # scrape Wesleyan Events
    if not SCRAPE_WESLEYAN_EVENTS:
        return True
    try:
        wesleyan_events_results = wesleyanEvents.scrape_wesleyan_events()
    except:
        print "SCRAPER: Unable to scrape Weleyan Events"
        return False
    # add to db
    for res in wesleyan_events_results:
        add_result = db.add_event(res)
        if not add_result:
            print "SCRAPER: Unable to add Wesleyan events to db"
    return True


def scrape_usdan_menus():
    # scrape Wesleyan Menus
    if not SCRAPE_USDAN:
        return True
    try:
        usdan_results = usdanMenus.fetch_all()
    except:
        print "SCRAPER: Unable to scrape usdan menus"
        return False
    usdan_items = usdan_results.get('Usdan')
    if not usdan_items:
        print "SCRAPER: No usdan items from fetch"
        return False
    for item in usdan_items:
        result = db.add_usdan_day(item)
        if not result:
            print "SCRAPER:", item, "failed to add to db"
    return True


def populate_static_directory():
    try:
        if db.populate_static_directory():
            return True
        else:
            return False
    except:
        print "SCRAPER: Unable to populate static directory"
        return False


def populate_static_menus():
    try:
        if db.populate_static_menus():
            return True
        else:
            return False
    except:
        print "SCRAPER: Unable to populate static menus"
        return False


def scrape_film_series():
    if not SCRAPE_FILM_SERIES:
        return True
    try:
        film_series_results = film_series.scrape_film_series()
    except:
        print "SCRAPER: Unable to scrape film series"
        return False
    if not film_series_results:
        print "SCRAPER: No film series results"
        return False
    for item in film_series_results:
        result = db.add_film_event(item)
        if not result:
            print "SCRAPER:", item, "failed to add to db"
    return True


def remove_all_films():
    if not db.remove_all_films():
        print "SCRAPER: Unable to remove all film series"
        return False
    return True

# scrape WesMaps

# scrape Wesleyan Hours

# if running from cmd line, scrape.
if __name__ == "__main__":
    scrape_all_sources(continuous=True)
