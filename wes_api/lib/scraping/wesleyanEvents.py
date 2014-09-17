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

path = "weshappening.log"
# path = "weshappening.log"
logging.basicConfig(filename=path, level=logging.DEBUG,
                        format="%(asctime)s: %(message)s")
logging.debug("Updating events")

feed_url = "http://events.wesleyan.edu/events/cal_rss_today"
feed = feedparser.parse(feed_url)
wes_events_cats = cat_choose2(feed['items'])


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
    if date.group() and time.group():
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
        date = str(datetime.dateime.today())
    desc = value[0]
    loc = re.search("Location: .*", str(value[-1])).group().lstrip("Location: ")
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

    add_event(event)
    sleep(1)
