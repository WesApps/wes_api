import twitter

# IMPORTANT, REGENERATE THESE KEYS UPON PUBLIC RELEASE, HIDE IN EXTERNAL FILE
consumer_key = "AN3VofmpquALOXkuOlWXZRy6c"
consumer_secret = "f2dsiT270djcV6z5hzF8RUGL3Lpl9PwQDZwXLqKRaU1N4pYfld"
access_token = "2183203471-q8bAXEgpE9LsWEUtNe1TiMg6cKl1kCpjCIUa1fj"
access_token_secret = "hdkioPHiApEYELETaNh8IA40f2diwZq9Z4yZ3jDx7SwZo"
api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret)


sources = {"wesleyan_argus": "wesleyanargus", "whey_station":
           "wheystation", "weswings": "weswings", "wesampersand": "WesAmpersand",
           "wesleying": "wesleying"}


def get_tweets(sources):
    """
    Gets tweets from various sources.
    """
    results = {}
    for s in sources:
        try:
            data = api.GetUserTimeline(
                screen_name=sources[s], exclude_replies=True)
            # we skip if it's retweeted
            if data.retweeted_status:
                continue
            else:
            	results[s] = {"text":data.text,"favorite_count":data.favorite_count}
        except:
        	return None
