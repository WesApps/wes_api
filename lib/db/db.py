from pymongo import MongoClient
import datetime
import csv
import json

client = MongoClient()
db = client.wes_api

status = db.status

events = db.events
usdan_menus = db.usdan_menus
late_night_menu = db.late_night_menu
summerfields_menu = db.summerfields_menu
red_and_black_menu = db.red_and_black_menu
weswings_menu = db.weswings_menu
film_series = db.film_series
directory = db.directory


json_directory = "static/wesleyanDirectory.json"
json_filmseries = "static/filmListMarMay.json"
json_red_and_black = "static/RedandBlack.json"
json_weswings = "static/weswings_menu.json"
# json_s_and_c = "static/wesleyanDirectory.json"

"""
GENERAL DB METHODS
"""


def populate_from_json(json_obj, target_db):
    """
    json_obj: a json obj ( from json.loads(file("foo.json").read())) )
    target_db: the db object to add to
    modification_fn: if modification_fn, applies it to the json. Ex: could be 
    """
    for i in json_obj:
        if not target_db.find({"name": i}).count() != 0:
            target_db.insert({"name": i, "data": json_obj[i]})
        else:
            target_db.update(
                {'name': i}, {"$set": {"data": json_obj[i]}})
    return True


def update_status(apis):
    """
    Upserts the last updated times and statuses for the APIs.
    """
    for i in apis:
        try:
            # check if scrape succeeded.
            # Note: it IS possible for a None time value to exist here
            # if the API hasn't ever succeeded before.
            # Normally, the time should be equal to the last successful scrape.
            if not apis[i]:
                api_status = False
            else:
                api_status = True
            if status.find({"name": i}).count() == 0:
                print "INSERTING"
                status.insert(
                    {"name": i, "time": apis[i], "status": api_status})
            else:
                # if have new time, overwrite old. else keep old.
                if api_status:
                    status.update(
                        {'name': i}, {"$set": {"time": apis[i], "status": api_status}})
                else:
                    status.update(
                        {'name': i}, {"$set": {"status": api_status}})
        except:
            print "DB: Unable to update 'update status' for", i


"""
EVENT DB METHODS
"""


def add_event(event):
    """
    Upserts the event. Returns False if unable to upsert.
    Uses 'name' of event as unique ID
    """
    # ensure event['name'] exists
    name = event.get('name')
    if not name:
        print 'DB: Unable to upsert event, no name', event
        return False
    try:
        events.update({'name': name}, event, True)
        return True
    except:
        print 'DB: Unable to upsert event, can\'t add to db', event
        return False


def remove_event_by_name(eventName):
    """
    Removes one instance of the event with 'name' == 'eventName'
    if it exists, otherwise do nothing.
    """
    try:
        events.remove({'name': eventName})
        return True
    except:
        print 'DB: Unable to remove event', eventName
        return False


def remove_events_by_source(sourceName):
    """
    Removes all event documents with source == sourceName
    """
    try:
        events.remove({'source': sourceName})
        return True
    except:
        print 'DB: Unable to remove events from source', sourceName
        return False


def remove_all_events():
    """
    Removes all events from the DB
    """
    try:
        events.drop()
        print 'DB: Dropped events DB'
        return True
    except:
        print 'DB: Unable to drop events DB'
        return False

"""
MENU DB METHODS
"""


def populate_static_menus():
    try:
        print "DB: Populating static menus"
        #summerfields
        populate_static_menu("static/summerfields_menu.csv", summerfields_menu)
        #late night
        populate_static_menu("static/late_night.csv", late_night_menu)
        
        #red and black
        json_obj = json.loads(file(json_red_and_black).read())
        populate_from_json(json_obj, red_and_black_menu)

        #weswings
        json_obj2 = json.loads(file(json_weswings).read())
        populate_from_json(json_obj2, weswings_menu)

        return True

    except Exception, e:
        print "DB: Populating static menus failed"
        print e
        return False


def populate_static_menu(csv_file, target_db):
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
            "title": title,
            "filter": item_filter,
            "description": description,
            "price": price
        }
        # if it does not exist, insert it.
        if csv_file == "static/late_night.csv":
            print target_db.count()
            print obj
            print line['item']
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
        meal_data = {'title': meal[1], 'extra': meal[2]}
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
        day_time = datetime.datetime.strptime(raw_day_time, '%a, %d %b %Y')

        # if we already have the item, can stop.
        # print usdan_menus.find({'time':day_time}).count()
        if usdan_menus.find({'time': day_time}).count() != 0:
            return True

        processed_meals = {}
        meals = ['breakfast', 'lunch', 'dinner', 'brunch']
        for meal in meals:
            raw_meal = day_item.get(meal)
            if raw_meal:
                dict_meal = flatten_meal_item(raw_meal)
                processed_meals[meal] = dict_meal

        processed_day_item = {
            "time": day_time,
            "breakfast": processed_meals.get('breakfast'),
            "lunch": processed_meals.get('lunch'),
            "dinner": processed_meals.get('dinner'),
            "brunch": processed_meals.get('brunch')
        }
        usdan_menus.insert(processed_day_item)
        return True
    except Exception,e:
        print "DB: Unable to add usdan day,", day_item
        print e
        return False


def remove_all_menus():
    """
    Removes all events from the DB
    """
    try:
        usdan_menus.drop()
        summerfields_menu.drop()
        late_night_menu.drop()
        red_and_black_menu.drop()
        print 'DB: Dropped Menus DB'
        return True
    except Exception,e:
        print 'DB: Unable to drop menus DB'
        print e
        return False

"""
FILM SERIES METHODS
"""


def populate_static_filmseries():
    """
    Populates film series data from file
    """
    try:
        # Read in file to json
        json_obj = json.loads(file(json_filmseries).read())
        year = datetime.datetime.now().year
        for i in json_obj:
            data = json_obj[i]
            c_date = data.get("date")[0]
            c_day = data.get("day")[0]
            if not c_date and c_day:
                print "DB: No date for film series item", i
                return False
            # Convert the day and date fields to one datetime
            new_time = datetime.datetime.strptime(
                c_day + ", " + c_date + " "+str(year), "%A, %B %d %Y")
            data["time"] = [new_time]

            # remove old day and dates
            data.pop("date")
            data.pop("day")

        # add to db
        populate_from_json(json_obj, film_series)
        return True
    except Exception, e:
        print "DB: populate static film error", e
        return False


def remove_all_filmseries():
    try:
        film_series.drop()
        print 'DB: Dropped Film Series DB'
        return True
    except:
        print 'DB: Unable to drop Film Series DB'
        return False


"""
DIRECTORY METHODS
"""


def populate_static_directory():
    """
    Reads from static/wesleyanDirectory.json
    and adds new entries to the db
    """
    try:
        json_obj = json.loads(file(json_directory).read())
        populate_from_json(json_obj, directory)
        return True
    except Exception, e:
        print e,
        return False


def remove_directory_entries():
    try:
        directory.drop()
        print "DB: Dropped directory entries"
        return True
    except:
        print "DB: Unable to drop directory DB"
        return False