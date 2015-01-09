gunicorn runserver:app -w 3 --bind 104.131.29.221:80 &
python scraper_control.py continuous &