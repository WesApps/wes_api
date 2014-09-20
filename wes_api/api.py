from lib.search import search
from flask import Blueprint,request
import json
import datetime

api = Blueprint('api',__name__,template_folder='templates')
EVENT_SOURCES = ["wesleying","wesleyanEvents"]
MENU_SOURCES = ["usdan"]

def err_response(errMsg):
	"""
	Responds with:
	{"ERROR":errMsg}
	"""
	return json.dumps({"ERROR":errMsg})


def validate_max_results_arg(req_max_results,min_results,max_results):
	try:
		req_max_results = int(req_max_results)
		errMsg = "Please specify between "+str(min_results)+ " and "+str(max_results)+" maxresults."
		if req_max_results < min_results:
			return [False,err_response(errMsg)]
		if req_max_results > 100:
			return [False,err_response(errMsg)]
		else:
			return [True,req_max_results]
	except:
		errMsg = ("Unable to process your request, please ensure your"
					" request is properly formatted.")
		return [False,err_response(errMsg)]

def validate_source(req_source,accepted_sources):
	return req_source in accepted_sources


def validate_request(request_obj,min_results,max_results,accepted_sources=None):
	"""
	Pulls out maxresults and source out of args. 
	Validates maxresults and source, if either bad, returns 
	[False, errormsg], else, [True,maxresults,source]. 
	If no maxresults or source in request, return defaults,
	respectively.
	Right now, source only allows for one source. 
	"""
	req_max_results = request.args.get('maxresults')
	raw_data_source = request.args.get('source')
	if req_max_results:
		# check the request
		valid = validate_max_results_arg(req_max_results,min_results,max_results)
		if not valid[0]:
			return [False,valid[1]]
		# grab the int-ified result from validate since valid
		req_max_results = valid[1]
	else:
		req_max_results = max_results

	if raw_data_source and accepted_sources:
		#validate source
		valid = validate_source(raw_data_source,accepted_sources)
		if not valid:
			source_string = ",".join(accepted_sources)
			return [False,err_response("Invalid source, please select from: "+source_string)]
		data_source = raw_data_source
	else:
		data_source = None
	return [True,{"max_results":req_max_results,"source":data_source}]

"""
EVENTS
"""
def format_mongo_objs(mongo_objs):
	"""
	Formats python datetime into isoformat for each mongo_obj
	if the obj has a time.
	Also strips out object ID
	"""
	print len(mongo_objs),"COUNT"
	for mongo_obj in mongo_objs:
		#remove object_id 
		try:
			mongo_obj.pop('_id')
		except:
			print "mongo_obj has no _id, panic!"
			
		old_time = mongo_obj.get('time')
		if not old_time:
			print "mongo_obj",mongo_obj,"has no time"
			continue
		mongo_obj['time'] = old_time.isoformat()
	return [{"Result Count":len(mongo_objs)},{"Results":mongo_objs}]


@api.route('/events/latest',methods=['GET'])
def get_latest_events():
	"""
	Returns latest results.
	Maxresults defaults to 30.
	Max is 100
	Min is 1
	"""
	# default
	MIN_RESULTS = 1
	MAX_RESULTS = 100
	accepted_sources = ["Wesleying","Wesleyan Events"]
	validation_result = validate_request(request,MIN_RESULTS,MAX_RESULTS,accepted_sources)
	if not validation_result[0]:
		return validation_result[1]
	else:
		req_max_results = validation_result[1]['max_results']
		req_source = validation_result[1]['source']

	#Now search, check, and respond
	search_results = search.get_events(req_max_results,req_source)
	if not search_results:
		errMsg = ("Unable to find events in the database. Sadface")
		return err_response(errMsg)
	if len(search_results) < 1:
		errMsg = ("No latest events, panic.")
		return err_response(errMsg)
	else:
		return json.dumps(format_mongo_objs(search_results))

@api.route('/events/sources',methods=['GET'])
def get_sources():
	return json.dumps(EVENT_SOURCES)

"""
MENUS

/all --gets everything, default maxresults = 7 days, 
			default both usdan and summerfields
/today --gets everything, default both usdan and summerfields
"""
@api.route('/menus/all',methods=['GET'])
def get_menus_all():
	# default
	MIN_RESULTS = 1
	MAX_RESULTS = 100

	validation_result = validate_request(request,MIN_RESULTS,MAX_RESULTS)
	if not validation_result[0]:
		return validation_result[1]
	else:
		req_max_results = validation_result[1]['max_results']

	#Now search, check, and respond
	search_results = search.get_menus_all(req_max_results)

	if not search_results:
		errMsg = ("Unable to find menus in the database. Sadface")
		return err_response(errMsg)
	if len(search_results) < 1:
		errMsg = ("No latest events, panic.")
		return err_response(errMsg)
	else:
		return json.dumps(format_mongo_objs(search_results))



@api.route('/menus/today',methods=['GET'])
def get_menus_today():
	pass

@api.route('/menus/clear/password',methods=['GET'])
def clear_menus():
	pass
