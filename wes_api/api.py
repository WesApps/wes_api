from lib.search import search
from flask import Blueprint, make_response, request, current_app
import json
import time
import datetime
from datetime import timedelta
from functools import update_wrapper

api = Blueprint('api', __name__, template_folder='templates')
EVENT_SOURCES = ["wesleying", "wesleyanEvents"]
MENU_SOURCES = ["usdan"]

"""
http://flask.pocoo.org/snippets/56/
"""


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


"""
TODO: Refactor some of this to get rid of the
repeated code..
"""


def err_response(errMsg):
    """
    Responds with:
    {"ERROR":errMsg}
    """
    return json.dumps({"ERROR": errMsg})


def validate_max_results_arg(req_max_results, min_results, max_results):
    try:
        req_max_results = int(req_max_results)
        errMsg = "Please specify between " + \
            str(min_results) + " and " + str(max_results) + " maxresults."
        if req_max_results < min_results:
            return [False, err_response(errMsg)]
        if req_max_results > 100:
            return [False, err_response(errMsg)]
        else:
            return [True, req_max_results]
    except:
        errMsg = ("Unable to process your request, please ensure your"
                  " request is properly formatted.")
        return [False, err_response(errMsg)]


def validate_source(req_source, accepted_sources):
    return req_source in accepted_sources


def time_from_raw_string(raw_time):
    try:
        nt = time.strptime(raw_time, "%m-%d-%Y")
        new_date = datetime.datetime(
            month=nt.tm_mon,
            day=nt.tm_mday,
            year=nt.tm_year
        )
        return new_date
    except:
        return False


def validate_search_request(request_obj, min_results, max_results):
    """
    Grabs search terms from request if they exist, including:
    -title
    -location
    -time_from
    -time_until
    -category_query
    -source
    -maxresults
    """
    raw_title = request.args.get('title')
    raw_location = request.args.get('location')
    raw_time_from = request.args.get('timeFrom')
    raw_time_until = request.args.get('timeUntil')
    raw_category = request.args.get('category')
    raw_source = request.args.get('source')
    raw_max_results = request.args.get('maxresults')

    if raw_time_from:
        raw_time_from = time_from_raw_string(raw_time_from)
        if not raw_time_from:
            return [False, err_response("Invalid: time from")]
    if raw_time_until:
        raw_time_until = time_from_raw_string(raw_time_until)
        if not raw_time_until:
            return [False, err_response("Invalid: time until")]
    if raw_max_results:
        # check the request
        valid = validate_max_results_arg(
            raw_max_results, min_results, max_results)
        if not valid[0]:
            return [False, valid[1]]
        # grab the int-ified result from validate since valid
        raw_max_results = valid[1]
    else:
        raw_max_results = max_results

    return [True, {"max_results": raw_max_results, "source": raw_source,
                   "title": raw_title, "location": raw_location,
                   "time_from": raw_time_from, "time_until": raw_time_until,
                   "category": raw_category}]


def validate_request(request_obj, min_results, max_results, accepted_sources=None):
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
        valid = validate_max_results_arg(
            req_max_results, min_results, max_results)
        if not valid[0]:
            return [False, valid[1]]
        # grab the int-ified result from validate since valid
        req_max_results = valid[1]
    else:
        req_max_results = max_results

    if raw_data_source and accepted_sources:
        # validate source
        valid = validate_source(raw_data_source, accepted_sources)
        if not valid:
            source_string = ",".join(accepted_sources)
            return [False, err_response("Invalid source, please select from: " + source_string)]
        data_source = raw_data_source
    else:
        data_source = None
    return [True, {"max_results": req_max_results, "source": data_source}]


def validate_search_results(search_results):
    if not search_results:
        return json.dumps({"Result Count": 0, "Results": []})

    final_objs = format_mongo_objs(search_results)
    response = {"Result Count": len(final_objs),
                "Results": final_objs}
    return json.dumps(response)


def format_mongo_objs(mongo_objs):
    """
    Formats python datetime into isoformat for each mongo_obj
    if the obj has a time.
    Also strips out object ID
    """
    for mongo_obj in mongo_objs:
        # remove object_id
        try:
            mongo_obj.pop('_id')
        except:
            print "API: mongo_obj has no _id, panic!"

        old_time = mongo_obj.get('time')
        if not old_time:
            continue
        mongo_obj['time'] = old_time.isoformat()
    return mongo_objs


def format_status(status):
    return dict((i["name"], {"time": i["time"], "status": i["status"]}) for i in status)

"""
GENERAL ROUTES
"""


@api.route('/status', methods=['GET'])
@crossdomain(origin='*')
def get_status():
    tmp = format_mongo_objs(search.get_status())
    return json.dumps(format_status(tmp))


"""
EVENTS
"""


@api.route('/events/today', methods=['GET'])
@crossdomain(origin='*')
def get_today_events():
    return get_events(True)


@api.route('/events/latest', methods=['GET'])
@crossdomain(origin='*')
def get_latest_events():
    return get_events()


@api.route('/events/search', methods=['GET'])
@crossdomain(origin='*')
def search_events_route():
    return search_events()


def search_events():
    """
    Moar powarful searching RAWR!
    """
    # default
    MIN_RESULTS = 1
    MAX_RESULTS = 100
    validation_result = validate_search_request(
        request, MIN_RESULTS, MAX_RESULTS)
    if not validation_result[0]:
        return validation_result[1]
    else:
        req_max_results = validation_result[1]['max_results']
        req_source = validation_result[1]['source']
        req_title = validation_result[1]['title']
        req_time_from = validation_result[1]['time_from']
        req_time_until = validation_result[1]['time_until']
        req_category = validation_result[1]['category']
        req_location = validation_result[1]['location']

    # Now search, check, and respond
    """
	def search_events(numResults,title_query,location_query,
					time_from,time_until,category_query,source):
	"""
    search_results = search.search_events(
        numResults=req_max_results,
        title_query=req_title,
        location_query=req_location,
        time_from=req_time_from,
        time_until=req_time_until,
        category_query=req_category,
        source=req_source)

    return validate_search_results(search_results)


def get_events(today=False):
    """
    Returns latest results.
    Maxresults defaults to 30.
    Max is 100
    Min is 1
    """
    # default
    MIN_RESULTS = 1
    MAX_RESULTS = 100
    accepted_sources = ["Wesleying", "Wesleyan Events"]
    validation_result = validate_request(
        request, MIN_RESULTS, MAX_RESULTS, accepted_sources)
    if not validation_result[0]:
        return validation_result[1]
    else:
        req_max_results = validation_result[1]['max_results']
        req_source = validation_result[1]['source']

    # Now search, check, and respond
    if today:
        search_results = search.get_events_today()
    else:
        search_results = search.get_events(req_max_results, req_source)

    return validate_search_results(search_results)


@api.route('/events/sources', methods=['GET'])
@crossdomain(origin='*')
def get_sources():
    return json.dumps(EVENT_SOURCES)


"""
MENUS

/latest --gets everything, default maxresults = 7 days, 
			default both usdan and summerfields
/today --gets everything, default both usdan and summerfields
"""


def get_menus(min_res, max_res, today=False):
    # default
    MIN_RESULTS = min_res
    MAX_RESULTS = max_res

    validation_result = validate_request(request, MIN_RESULTS, MAX_RESULTS)
    if not validation_result[0]:
        return validation_result[1]
    else:
        req_max_results = validation_result[1]['max_results']

    # Now search, check, and respond
    if today:
        search_results = search.get_menus_today()
    else:
        search_results = search.get_menus_all(req_max_results)
    # only need to validate the usdan ones.
    usdan_results = search_results.get('usdan')
    if not usdan_results:
        return json.dumps({"Result Count": 0, "Results": []})

    # get late night and summerfields.
    # this method will return all or nothing,
    # so if usdan fails, you get nothing.
    # ALSO, number of results is tied to usdan results
    summerfields = format_mongo_objs(search_results.get('summerfields'))
    late_night = format_mongo_objs(search_results.get('late_night'))
    usdan = format_mongo_objs(usdan_results)
    final_objs = {"usdan": usdan,
                  "summerfields": summerfields,
                  "late_night": late_night}

    response = {"Result Count": len(usdan),
                "Results": final_objs}
    return json.dumps(response)


@api.route('/menus/latest', methods=['GET'])
@crossdomain(origin='*')
def get_menus_all():
    return get_menus(1, 100)


@api.route('/menus/today', methods=['GET'])
def get_menus_today():
    """
    Only source argument accepted here.
    """
    return get_menus(1, 1, True)

"""
FILM SERIES METHODS
"""


def get_film_series(today=False):
    if today:
        search_results = search.get_film_series_today()
    else:
        search_results = search.get_film_series_all()
    # only need to validate the usdan ones.
    return validate_search_results(search_results)


@api.route('/filmseries/all')
@crossdomain(origin='*')
def get_film_series_all():
    return get_film_series()


@api.route('/filmseries/today')
@crossdomain(origin='*')
def get_film_series_today():
    return get_film_series(True)
