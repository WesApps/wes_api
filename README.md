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
    -Convert and store times as UNIX timestamp where appropriate
    -Store a set of categories used by events, make a route for it
    -Store a "Last Updated" time for every source 
    -Sort filmseries in time descending order.
		-Build basic frontend to showcase API, have a few interactive examples
    -Documentation, including some code samples
		-WesMaps data
		-Wesleyan Hours of Operations
	
	TODO (lower priority):
    -Weswings static menu + specials from RSS
    -Integrate caching system
	-Determine how to collect and parse the menu emails sent out by Bon Appetite. May require using SendGrid.
		
