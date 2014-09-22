"""
Approach: Scan for links, filter to links if they contain
a month AND do NOT contain 'archive/...'
Then, set(links) to get unique, then 
for each link, get the page and grab all films found on that page.
http://www.wesleyan.edu/filmseries/index.html
"""

import urllib2
import BeautifulSoup
import datetime
import re

def scrape_film_series():
	# try:
	raw_week_pages = get_week_pages()
	processed_week_pages = process_week_pages(raw_week_pages)
	return processed_week_pages
	# except:
	print "Unable to scrape film series."
	return None

def get_week_pages():
	url = "http://www.wesleyan.edu/filmseries/index.html"
	text = urllib2.urlopen(url).read()
	soup = BeautifulSoup.BeautifulSoup(text)
	#gather links
	all_links = soup.findAll('a')
	months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
	week_pages= set()
	for link in all_links:
		link_text = link.get('href')
		if not link_text:
			print "NO LINK TEXT??",link
			continue
		for month in months:
			if month in link_text and "archive" not in link_text:
				week_pages.add(link_text)
	return week_pages

def process_week_pages(week_pages):
	base_url = "http://www.wesleyan.edu/filmseries/"
	all_processed = []
	for week in week_pages:
		url = base_url + urllib2.quote(week)
		text = urllib2.urlopen(url).read()
		soup = BeautifulSoup.BeautifulSoup(text)
		#There seem to be TWO different formats
		#One with paragraphs, one with divs.

		#Style 1
		style1 = soup.findAll('p',{'class':'ParagraphStyle1'})
		if style1:
			processed = [all_processed.append(process_p_style(i)) for i in style1]
		else:
			#Style 2 
			style2 = soup.findAll('div',{'class':'movie'})
			if style2:
				processed = [all_processed.append(process_div_style(i)) for i in style2]
			else:
				return False
	return all_processed


def remove_date_end(s):                                             
    return re.sub(r'(\d)(st|nd|rd|th)', r'\1', s)

def process_date(date):
	"""
	Takes in a date like:
	September 22
	and outputs a Python datetime obj with
	the current year.
	"""
	curr_year = str(datetime.date.today().year)
	date_with_year = curr_year+" "+remove_date_end(date).strip()
	return datetime.datetime.strptime(date_with_year,"%Y %B %d")

def process_p_style(soup):
	date = process_date(soup.next)
	movie_span = soup.find('span',{"class":"LargeText"})
	movie_title = movie_span.text
	short_description = movie_span.next.next.next
	
	#Catch italic cases for this.. hacky :(
	long_description = movie_span.next.next.next.next.next
	print type(long_description),"type"
	if type(long_description) not in  [BeautifulSoup.NavigableString,unicode]:
		long_description = long_description.text + long_description.nextSibling

	movie_obj = {"date":date,"title":movie_title,
				 "short_description":short_description,
				 "long_description":long_description}
 	return movie_obj

def process_div_style(soup):
	date = process_date(soup.next)
	movie_h3 = soup.find('h3',{'class':'movietitle'})
	movie_title = movie_h3.next
	short_description = movie_h3.next.next
	long_description = soup.find('p').text

	#Catch italic
	if type(long_description) not in  [BeautifulSoup.NavigableString,unicode]:
		long_description = long_description.next + long_description.next.nextSibling

	movie_obj = {"date":date,"title":movie_title,
				 "short_description":short_description,
				 "long_description":long_description}
	return movie_obj

