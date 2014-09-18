from BeautifulSoup import BeautifulSoup
import feedparser

usdan_rss = "http://legacy.cafebonappetit.com/rss/menu/332"
# summerfields_rss = 'http://legacy.cafebonappetit.com/rss/menu/337'

def fetch_all():
	usdan_meals = fetch_meals(usdan_rss)
	# summerfields_meals = fetch_meals(summerfields_rss)
	return {"Usdan":usdan_meals}

def fetch_meals(source):
	fp = feedparser.parse(source)
	items = fp['items']
	parsed_items = []
	for item in items:
		parsed_items.append(parse_day_item(item))
	return parsed_items
	
def parse_day_item(item):
	# This parser will assume a few things about the structure
	# of the data. If assumptions break, there will be no menu
	# for that meal/day :(

	# Assume: Usdan has 3 meals, Summerfields has only lunch and dinner.
	summary_text = item.summary
	soup = BeautifulSoup(summary_text)
	meals = soup.findAll('h3')
	item_time = item.title

	#weekday, breakfast,lunch,dinner
	if len(meals) == 3:
		breakfast = meals[0]
		if not breakfast.text == "Breakfast":
			print "Umm... Usdan haz no breakfast. Should we be concerned?"
			return
		breakfast_items = get_food_items_until(breakfast,"Lunch")
		lunch_items = get_food_items_until(meals[1],"Dinner")
		dinner_items = get_food_items_until(meals[2],"")
		
		items_obj = {"time":item_time,
					 "breakfast":breakfast_items,
					 "lunch":lunch_items,
					 "dinner":dinner_items
					 }
		return items_obj

	#weekend, brunch, dinner
	elif len(meals) == 2:
		brunch = meals[0]
		if not brunch.text == "Brunch":
			print "Umm... Usdan haz no brunch. Should we be concerned?"
			return
		brunch_items = get_food_items_until(brunch,"Dinner")
		dinner_items = get_food_items_until(meals[1],"")
		
		items_obj = {"time":item_time,
					 "brunch":brunch_items,
					 "dinner":dinner_items
					 }
		return items_obj
	else:
		print "PANIC, usdan does not have 2 or 3 meals."
		
	# else:
	# 	#Summerfields case
	# 	lunch_items = get_food_items_until(meals[0],"Dinner")
	# 	dinner_items = get_food_items_until(meals[1],"")
	# 	items_obj = {"time":item_time,
	# 				 "lunch":lunch_items,
	# 				 "dinner":dinner_items
	# 				 }
	# 	return items_obj

def get_food_items_until(bs_obj,stop):
	"""
	Walks through the items in the BeautifulSoup object in format:
	<h4>[ _category_ ] _title_ </h4>
	<p> _extra-description_ </p>
	...
	<h3>stop</h3>
	"""
	items = []
	tags = bs_obj.fetchNextSiblings()
	i = 0
	while i < len(tags):
		current_tag = tags[i]
		if str(current_tag)[0:4] == "<h3>":
			#this means we found a meal tag! Probably!
			if current_tag.text == stop:
				#this means we're done here
				break

		#now assume we're dealing with a food item, so grab this tag and the next one.
		# and assume the first is h4, second is p
		h4_text = current_tag.text.replace("&nbsp","")
		p_text = tags[i+1].text.replace("&nbsp","")

		#get the food category and title
		try:
			category,title = h4_text.split('[')[1].split(']')
		except:
			print "Unable to get the category + food title. Sadface."
			continue

		items.append([category,title,p_text])
		i += 2
		
	return items