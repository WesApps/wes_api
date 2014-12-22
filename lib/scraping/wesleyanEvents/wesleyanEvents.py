#!/usr/bin/python
import feedparser
import re
import datetime
from time import sleep
import logging
import os

def u_to_string(string):
    return eval('"' + string.replace('"','') + '"')


def no_unicode(string):
    lst = list(string)
    lst2 = lst[:]
    ite = 0
    for i in lst:
        try:
            str(i)
            ite += 1
        except:
            lst2.pop(ite)
        
    return ''.join(lst2)

# path = "weshappening.log"
# path = "weshappening.log"
# logging.basicConfig(filename=path, level=logging.DEBUG,
#                         format="%(asctime)s: %(message)s")
# logging.debug("Updating events")

def wesleyan_events_categorizer(posts):
    """
    FOR WESLEYAN EVENTS until they get their ....  together and give us the actual categories.
    For each event in posts, for each category in cat_tags, return the category 
    with the maximum number of cat_tag matches. If matches = 0 for a post, 
    return 'other' for that post. Returns a dictionary of all events and
    their corrosponding category.
    """
    cat_tags = {
    'Film':['film','movie','film series'],
    'Auditions':['auditions','seek','try','out'],
    'Theater':['play','see','92','theater','stage','second'],
    'Performances':['dance','slam','poetry','reading','mic','open','soul'],
    'Student Groups':['cause','education','meeting','food','student','group',
        'student group','queer','?','community','club','sustain','environment',
        'help','civic','forums','engage','art','culture','academic','art','diversity'],
    'Sports':['football','soccer','baseball','swimming','lacross','basketball',
        'softball','varsity','tennis','hockey','athlet','freeman','sport'],
    'Admissions':['admission','tour','session','information']
    }
    event_cats = {}
    for post in posts:
        potentials = []
        description = post['description'].lower()
        best_match = "Other"
        best_count = 0
        for item in cat_tags.keys():
            count = 0
            for tag in cat_tags[item]:
                occurs = description.count(tag)
                count += occurs
                if count > best_count:
                    best_count = count
                    best_match = item
        event_cats[post] = best_match
    return event_cats


def scrape_wesleyan_events():
    wesleyan_events = []
    feed_url = "http://events.wesleyan.edu/events/cal_rss_today"
    feed = feedparser.parse(feed_url)
    wes_events_cats = wesleyan_events_categorizer(feed['items'])

    for item in feed["items"]:
        name = str(item["title"])
        if name.startswith("TBA"):
            name = name[4:]
        else:
            name = name[9:]
        value = item["summary_detail"]["value"].split("<br />")
        value0 = str(no_unicode(value[0]))
        date = re.match("\d\d/\d\d/\d\d\d\d", value0)
        time = re.search("(TBA|\d\d:\d\d (a|p)m( - \d\d:\d\d (a|p)m)*)", value0)        
        if not time:
            date = date.group().split("/")
            dt = datetime.datetime(int(date[2]), int(date[0]), int(date[1]))
        elif date.group() and time.group():
            date = date.group().split("/")
            time = time.group().split(" ")
        
            if len(time) > 1:
                t = time[0].split(":")
                if (time[1] == "pm") and not (int(t[0]) == 12):
                    dt = datetime.datetime(int(date[2]), int(date[0]), int(date[1]), (int(t[0])+12)%24, int(t[1]))
                elif (int(t[0]) == 12) and (t[1] == ("am")):
                    dt = datetime.datetime(int(date[2]), int(date[0]), int(date[1]), 0, int(t[1]))
                else:
                    dt = datetime.datetime(int(date[2]), int(date[0]), int(date[1]), int(t[0]), int(t[1]))
            else:
                dt = datetime.datetime(int(date[2]), int(date[0]), int(date[1]))
        else:
            dt = str(datetime.dateime.today())
        desc = value[0]
        try:
            loc = re.search("Location: .*", str(value[-1])).group().lstrip("Location: ")
        except:
            loc = ""
        link = ""
        for v in value:
            if v.startswith("URL"):
                link = v.lstrip("URL: ")

        #Category choosing
        cat = wes_events_cats[item]

        event = {"name": name, "location": loc, 
                 "time": dt, "link": link, 
                 "description": desc, "category":cat,
                 "source":'Wesleyan Events'
                 }
        wesleyan_events.append(event)
    return wesleyan_events

        
