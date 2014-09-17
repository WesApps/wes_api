from xml.dom import minidom
import urllib2
import BeautifulSoup
import datetime
import re
import time
from operator import itemgetter, attrgetter


def content_parser(content,identifiers):
    """
    Content is a list of words and identifiers is a dict of lists
    """  
    info_list = []
    index = 0
    for word in content:
        for i in identifiers.keys():
            try:
                word = str(word)
            except:
                try:
                    word = word.split()[0]
                except:
                    #some random instances of unicode weird things.
                    pass 
            e = [str(z) for z in identifiers[i]]
            for t in e:
                if t in word:

                    info_list.append((word,index))
                    break
        index += 1
    if info_list:
        return info_list

def content_builder(content,identifiers,matches):
    """
    Builds list of associated content from list based on given subset/indexes of matches 
    """
    # identifiers = {"date":["Date:"],"time":["Time:"],"place":["Place:","Place"]}
    inverse_dict = {}
    for i in identifiers:
        for z in identifiers[i]:
            inverse_dict[z] = i

    #sort matches by index ascending
    matches = sorted(matches,key=itemgetter(1))
    # print matches,"matches"

    #iterating through the matches and building up a list of words that 
    #occur before the next match item. If no next match, grab everything
    #until end.
    event = {}
    index = 0
    for m in matches:
        if m[0] in inverse_dict:
            try:
                stop = matches[index+1][1]
                words = [word for word in content[m[1]+1:stop]]
            except:
                words = [word for word in content[m[1]+1:]]
            event[inverse_dict[m[0]]] = words
        index += 1

    return event


# import get_data;a = get_data.xml_parser()
def get_xml():
    xml = urllib2.urlopen("http://wesleying.org/feed/")
    dom = minidom.parse(xml)
    items = dom.getElementsByTagName('item')
    return items

def only_events(posts):
    """
    Goes through the category elements in each post and looks
    for an "event"-like tag. Returns false if no event tag is found.
    """
    categories = []
    actual_events = []
    for post in posts:
        cats = post.getElementsByTagName('category')
        for c in cats:
            categories.append(c.childNodes[0].data)
            if "event" in c.childNodes[0].data.lower():
                if post not in actual_events:
                    actual_events.append(post)
            
    # print categories
    return actual_events,categories



"""
FOR WESLEYING. Wes events is a little diff, they don't give tags/categories
in the feed. Could scrape the site every time we update since they
do give a link to the page which does have tags? Could talk to them too.

Idea:::: could create some lists of possible tags for certain 
categories in order to identify what kind of event each item is.
For example, music identifiers could be 
    [concert, band, a capella, ...]
Can look through the categories/gather some data to figure out
what these would be. WANT categories so that we can have
colored pins on the map and for filtering/searching purposes.
Could go through all the categories and figure out which cat best fits,
do some sort of max matches = category thing. Could also use description
as context for guessing but that gets a little more complicated. Might 
also be worth just talking to Wesleying people and asking them to 
put in some more generalized categories in their feed. Also better locations.
"""

def cat_choose2(posts):

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

def cat_choose(posts):
    """
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
        'softball','varsity','tennis'],
    'Admissions':['admission','tour','session','information'],
    'Other':[]
    }
    event_cats = {}
    for post in posts:
        potentials = []
        cats = post.getElementsByTagName('category')
        for c in cats:
            name = c.childNodes[0].data.lower()
            most = 0
            identifier = "Other"
            for item in cat_tags.keys():
                count = 0
                for tag in cat_tags[item]:
                    if tag in name:
                        count += 1
                if count > most:
                    most = count
                    identifier = item
            potentials.append(identifier)
        # print potentials,post.getElementsByTagName('title')[0].childNodes[0].data
        #now find the most common potential category, excluding other. If
        #none, then cat = other
        cats2 = [z for z in potentials if z != "Other"]
        most = 0
        category = "Other"
        for i in cat_tags.keys():
            x = cats2.count(i)
            if x > most:
                most = x
                category = i

        event_cats[post] = category

    return event_cats


def xml_parser():
    """FOR WESLEYING"""
    all_items = get_xml()
    events = []
    items = only_events(all_items)[0]
    event_cats = cat_choose(items)
    for i in items:
        print i,"A"
        title = i.getElementsByTagName('title')[0].childNodes[0].data
        url = i.getElementsByTagName('link')[0].childNodes[0].data
        description = i.getElementsByTagName('description')[0].childNodes[0].data
        content_html = i.getElementsByTagName('content:encoded')[0].childNodes[0].data
        parsed_content = BeautifulSoup.BeautifulSoup(content_html)
        try:
            print parsed_content
            full_description = parsed_content.find('blockquote').text
        except:
            full_description = ""

        event_location = ""
        event_time = ""
        event_date = ""
        category = event_cats[i]

        identifiers = {"date":["Date:"],"time":["Time:","Time"],"place":["Place:","Place"]}
        soup = BeautifulSoup.BeautifulSoup(content_html)
        content = soup.getText('|').split('|')
        match = content_parser(content,identifiers)
        if match:
            built = content_builder(content,identifiers,match)
            if built.get("place"):
                event_location = built.get("place")
            if built.get("time"):
                event_time = built.get("time")
            if built.get("date"):
                event_date = built.get("date")  

        event = {"title":title,"url":url,"description":description,
            "location":event_location,"time":event_time,
            "date":event_date,"full_description":full_description,
            "category":category}

        events.append(event)
    return events