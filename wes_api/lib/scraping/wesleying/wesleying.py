#!/usr/bin/python
import feedparser
import re
import datetime
from wesleying_fetch import xml_parser, cat_choose2
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

def initialize():
    path = "wesleying_scraper.log"
    logging.basicConfig(filename=path, level=logging.DEBUG,
                        format="%(asctime)s: %(message)s")
    logging.debug("Updating wesleying events")
    scrape_wesleying()
    logging.debug("Events updated!")

def scrape_wesleying():
    wesleying_events = []
    wesleying_feed = xml_parser()
    print "LEN WESLEYING FEED:",len(wesleying_feed)
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
                "link": link, "description": desc, "category":cat,
                "source":'Wesleying'}
        wesleying_events.append(event)

    return wesleying_events

