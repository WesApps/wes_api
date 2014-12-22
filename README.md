wes-api
=======
<pre>
__          __                  _____ _____ 
\ \        / /            /\   |  __ \_   _|
 \ \  /\  / /__  ___     /  \  | |__) || |  
  \ \/  \/ / _ \/ __|   / /\ \ |  ___/ | |  
   \  /\  /  __/\__ \  / ____ \| |    _| |_ 
    \/  \/ \___||___/ /_/    \_\_|   |_____|
</pre>
									
	RESTful API that fetches, stores, and serves Wesleyan related information.
       
        Documentation forthcoming.
        Current status: Collecting data scrapers.
        	Have:
        		+Wesleying Events  
        		+Wesleyan Events   
        		+Usdan Daily Menus
        		+Summerfields Static Menu
        		+Late Night Static Menu
        		+Film Series Info


        Data scrapers have been collected and modified from:
         	Wesleying and Wesleyan event data scrapers: https://github.com/WesAppGroup/
         	Summerfields Static Menu: https://github.com/weshack/FoodyCall
            Manually entered data for Film Series and 
	
	TODO (high priority):
    -Integrate caching system on backend and set cache headers on responses
    -Write methods to put static data from Swings into DB, add routes
    -Figure out best way of getting S&C data
    -Documentation, including some code samples
    -Add logging for scraping.

    TODO (lower priority):
    -Write tests. 
    -Upgrade the random api component on home page
    to include more sources
    -Standardize menu output data
    -Give status a 'last modified' field in so people can check to see if they need to grab new data.
    -Store a set of categories used by events, make a route for it
    -Styling on home page.
    -Store a "Last Updated" time for every source 
