from lib.search import search
from flask import Blueprint,request
import json
import datetime

api = Blueprint('api',__name__,template_folder='templates')

def err_response(errMsg):
	"""
	Responds with:
	{"ERROR":errMsg}
	"""
	return json.dumps({"ERROR":errMsg})

def format_events(events):
	"""
	Formats python datetime into isoformat for each event
	if the event has a time.
	Also strips out object ID
	"""
	for event in events:
		#remove object_id 
		try:
			event.pop('_id')
		except:
			print "Event has no _id, panic!"
			
		old_time = event.get('time')
		if not old_time:
			print "Event",event,"has no time"
			continue
		event['time'] = old_time.isoformat()
	return events


## Events
@api.route('/events/latest',methods=['GET'])
def get_latest_events():
	"""
	Returns latest results.
	Maxresults defaults to 30.
	Max is 100
	Min is 1
	"""
	# default
	DEFAULT_MAX_RESULTS = 30

	req_max_results = request.args.get('maxresults')
	if req_max_results:
		try:
			req_max_results = int(req_max_results)
			if req_max_results < 1:
				errMsg = "Please specify between 1 - 100 maxresults"
				return err_response(errMsg)
			if req_max_results > 100:
				errMsg = "Please specify between 1 - 100 maxresults"
				return err_response(errMsg)
		except:
			errMsg = ("Unable to process your request, please ensure your"
						" request is properly formatted.")
			return err_response(errMsg)
	else:
		req_max_results = DEFAULT_MAX_RESULTS

	#Now search, check, and respond
	search_results = search.get_events(req_max_results)
	if not search_results:
		errMsg = ("Unable to find events in the database. Sadface")
		return err_response(errMsg)
	if len(search_results) < 1:
		errMsg = ("No latest events, panic.")
		return err_response(errMsg)
	else:
		return json.dumps(format_events(search_results))
  