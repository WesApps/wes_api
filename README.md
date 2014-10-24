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
	
	TODO (high priority):
    -Get data for Red and Black and Weswings
    -Write Wesleying scraper for S&C
    -Upgrade the random api component on home page
    to include more sources
    -Documentation, including some code samples
    -Add more info to Directory
    -Write tests. 
    
    TODO (lower priority):
    -Give status a 'last modified' field in so people can check to see if they need to grab new data.
    -Store a set of categories used by events, make a route for it
    -Styling on home page.
    -Store a "Last Updated" time for every source 
    -Integrate caching system
