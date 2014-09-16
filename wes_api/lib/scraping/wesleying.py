#!/usr/bin/python
import feedparser
import re
import datetime
from weshappening import add_event
from get_data import xml_parser,cat_choose2
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


wesleying_feed = xml_parser()
os.system("curl http://localhost/events/clear")
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

    event = {"name": name, "location": loc, "time": dt, "link": link, "description": desc, "category":cat}

    add_event(event)
    sleep(1)




##FOR WESLEYING
for item in wesleying_feed:
    name = no_unicode(item["title"])

    try:
        date_time,desc = item['description'].split("]",1)
        desc = desc.strip()
        date_time = date_time.lower()
    except:
        desc = item['description'].strip()
        date_time = str(datetime.datetime.today())
    d1 = list(desc)
    d1 = [i for i in d1 if i != "\n"]
    desc = "".join(d1)
    time = re.search("(:?january|february|march|april|may|june|july|august|september|october|november|december).*\d{1,2}, .*\d{4}.*; \d{1,2}:\d{2}.*to.*\d{1,2}:\d{2}.*(a|p)m(.|;)",date_time)
    if not time:
        time = re.search("(:?january|february|march|april|may|june|july|august|september|october|november|december).*\d{2}, .*\d{4}.*; \d{1}:\d{2}.*(a|p)m(;|.)",date_time)
    if time:
        time = [i.split() for i in time.group().split(".") if i.split()]
    loc = item["location"]
    if loc:
        ##ADD FOSS HILL TO BUILDINGS.TXT ?
        loc = no_unicode(no_unicode(loc[0]).strip().replace("$","s"))
    link = str(item['url'])
    cat = item["category"]

    times = []
    if time:
        for t in time:
            #this catches the weird cases where the next time is a dupe and is 
            # messed up and has no month. 
            if str(t[0]).count(":") == 0:
                month = t[0]
                try:
                    day = int(t[1].split(",")[0])
                except ValueError:
                    day = int(t[1])
                year = int(t[2].split(";")[0])
                z = t[3].split(":")
                hour = int(z[0])
                minutes = int(z[1])

                if t[4] == "pm" and not hour == 12:
                    start_dt = datetime.datetime(year,datetime.datetime.strptime(month,"%B").month,
                        day,hour+12,minutes)
                elif t[4] == "am" and hour == 12:
                    start_dt = datetime.datetime(year,datetime.datetime.strptime(month,"%B").month,
                        day,0,minutes)
                else:
                    start_dt = datetime.datetime(year,datetime.datetime.strptime(month,"%B").month,
                        day,hour,minutes)

                #End time case will be -1 for now
                try:
                    if t[5] == "to":
                        z = t[6].split(":")
                        hour = int(z[0])
                        minutes = int(z[1])

                        if t[7] == "pm" and not hour == 12:
                            end_dt = datetime.datetime(year,datetime.datetime.strptime(month,"%B").month,
                                day,hour+12,minutes)
                        elif t[7] == "am" and hour == 12:
                            end_dt = datetime.datetime(year,datetime.datetime.strptime(month,"%B").month,
                                day,0,minutes)
                        else:
                            end_dt = datetime.datetime(year,datetime.datetime.strptime(month,"%B").month,
                                day,hour,minutes)
                    else: 
                        end_dt = -1

                except IndexError:
                    end_dt = -1

                times.append((start_dt,end_dt))


    if not times:
        times = [[datetime.datetime.today()]]
    event = {"name": name, "location": loc, "time": times[0][0], 
            "link": link, "description": desc, "category":cat}
    add_event(event)
    sleep(1)

logging.debug("Events updated!")