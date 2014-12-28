$(document).ready(initialize_docs)

docs = {}
previous_doc = null;
previous_menu_item = null;

function initialize_docs() {
    // Define API types
    docs = {
        'navGeneral': $("#docsGeneral"),
        'navStatus': $("#docsStatus"),
        'navEvents': $("#docsEvents"),
        'navMenus': $("#docsMenus"),
        'navFilmSeries': $("#docsFilmSeries"),
        'navHours': $("#docsHours")
    }
    previous_doc = docs['navGeneral'];
    previous_menu_item = 'navGeneral';
    set_on_click_listeners();
    jsonify()
}

function set_on_click_listeners() {
    $("#apiNav li").on('click', function(e) {
        console.log(e.target)
        load_doc(e.target.id);
    })
}

function load_doc(doc) {
    if (!(doc in docs)) {
        console.log("Uh oh. Bad doc.", doc);
        return;
    }
    //Hide the old Docs
    if (previous_doc) {
        previous_doc.hide();
        //Change doc menu bar for previous doc
        // console.log(previous_doc)
        var menuEl = $("#" + previous_menu_item);
        menuEl[0].className = "inactive";
    }

    //Load the new API
    previous_doc = docs[doc];
    previous_menu_item = doc;
    previous_doc.show();
    console.log(previous_doc, doc);

    //Change api menu bar to show current api tab
    var menuEl = $("li #" + doc);
    menuEl[0].className = "active";
}

function jsonify(json) {
    var status = {
        "directory": {
            "status": true,
            "time": "2014-11-02T19:01:07.995000"
        },
        "menus": {
            "status": true,
            "time": "2014-12-23T15:10:30.295000"
        },
        "events": {
            "status": true,
            "time": "2014-12-23T15:10:29.799000"
        },
        "film_series": {
            "status": true,
            "time": "2014-11-02T19:01:07.995000"
        }
    };
    var events = {
        'Result Count': '2',
        'Results': [{
            "category ": "Performances ",
            "description": "Interested in the Romance Languages &#38; Literatures major? This is the open house for you:Would you like your undergraduate major to help you:· Acquire familiarity with another culture on that culture's terms?· Acquire the kind of linguistic and cross-cultural proficiency required for 21st-c. life and careers?· Put you into deep and meaningful contact with some of [...]",
            "source": "Wesleying",
            "link": "http://wesleying.org/2014/11/02/rlang-fall-open-house/?utm_source=rss&utm_medium=rss&utm_campaign=rlang-fall-open-house",
            "location": "300 High Street common room",
            "time": "2014-11-03T12:00:00",
            "name": "RLANG Fall Open House"
        }, {
            "category": "Student Groups",
            "description": "10/28/2014 09:00 pm - 10:45 pm Daniel Fishkin is an artist with the kind of tenacity that is mostly reserved for politicians and mountain climbers.",
            "source": "Wesleyan Events",
            "link": "http://www.wesleyan.edu/cfa/events/2014/10-2014/10282014daniel-fishkin-transcriptions.html",
            "location": "World Music Hall",
            "time": "2014-10-28T21:00:00",
            "name": "Daniel Fishkin: Transcriptions"
        }]
    };
    var json_collection = {
        "#json-status": status,
        "#json-events": events
    };

    for (j in json_collection) {
        $(j).JSONView(json_collection[j]);
    }
    // with options
    // $("#json-collasped").JSONView(json, {
    //     collapsed: true
    // });
}
