"""
Approach: Scan for links, filter to links if they contain
a month AND do NOT contain 'archive/...'
Then, set(links) to get unique, then 
for each link, get the page and grab all films found on that page.
"""