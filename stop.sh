kill $(ps aux | grep '[p]ython scraper_control.py continuous' | awk '{print $2}')
pkill gunicorn