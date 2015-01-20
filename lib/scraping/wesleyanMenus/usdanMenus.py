from BeautifulSoup import BeautifulSoup
import feedparser

usdan_rss = "http://legacy.cafebonappetit.com/rss/menu/332"
# summerfields_rss = 'http://legacy.cafebonappetit.com/rss/menu/337'


def fetch_all():
    usdan_meals = fetch_meals(usdan_rss)
    # summerfields_meals = fetch_meals(summerfields_rss)
    return {"Usdan": usdan_meals}


def fetch_meals(source):
    fp = feedparser.parse(source)
    items = fp['items']
    parsed_items = []
    for item in items:
        parsed_items.append(parse_day_item(item))
    return parsed_items


def parse_day_item(item):
    summary_text = item.summary
    soup = BeautifulSoup(summary_text)
    meal_tags = soup.findAll('h3')
    item_time = item.title
    meals = {"time": item_time}

    for i in meal_tags:
        meals[i.text.lower()] = get_food_items(i)

    return meals


def get_food_items(bs_obj):
    items = []
    tags = bs_obj.fetchNextSiblings()
    i = 0
    while i < len(tags):
        current_tag = tags[i]
        if current_tag.name == "h3":
            # this means we found a meal tag, probably, so end.
            break

        h4_text = current_tag.text.replace("&nbsp", "")
        p_text = tags[i + 1].text.replace("&nbsp", "")

        # get the food category and title
        category, title = h4_text.split('[')[1].split(']')

        items.append([category, title, p_text])
        i += 2

    return items

fetch_all()
