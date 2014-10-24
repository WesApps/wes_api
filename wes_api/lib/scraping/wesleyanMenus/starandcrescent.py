# from BeautifulSoup import BeautifulSoup
# import urllib
# url = "http://wesleying.org/author/star-and-crescent/"
# raw = urllib.urlopen(url)
# soup = BeautifulSoup(raw)
# articles = soup.findAll("article")
# stuff = ""
# for i in articles:
# 	if "star and crescent menu" in i.text.lower():
# 		print i.text
# 		break
# text = """Star and Crescent Menu 10/22 and 10/23.entry-headerS&amp;C HOURSLUNCH:TUESDAY &#8211; THURSDAY 12:00- 12:50.DINNER:MONDAY-THURSDAY 5:00-6:45FIRST THREE FRESHMEN EAT FREE!!!WEDNESDAYLUNCH- Pear, Goat Cheese, Walnut Salad w/ Crispy Shallots and Sherry Vin. With Roasted Chicken or TofuDES- Oatmeal Raisin, Chocolate Chip CookiesDINNER- Greens w/ Cilantro Dressing. Chili w/ Pork and Beef or Veggie. Garnished w/ Buttermilk Cornbread, Cheddar, Sour Cream and Scallion. VEGAN w/out GarnishDES- Banana CakeTHURSDAYLUNCH- Minestrone Soup w/Herb FocacciaDES- Peanut Butter Chocolate Chip CookiesDINNER- Greens w/ Curry Dressing. Tadka Dal w/ Basmati Rice &amp; Garlic NaanDES- Lemon Poppy Cake w/Berry Coulis.entry-contentPostedbyStar and CrescentonOctober 21, 2014at 1:37 PM.Leave a reply.comments-link.entry-meta"""
# for i in text.split("DINNER"): print i,"\n" 