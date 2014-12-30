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
        'navDirectory': $("#docsDirectory")
    }
    previous_doc = docs['navGeneral'];
    previous_menu_item = 'navGeneral';
    set_on_click_listeners();
    jsonify()
}

function set_on_click_listeners() {
    $("#apiNav li").on('click', function(e) {
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
        var menuEl = $("#" + previous_menu_item);
        menuEl[0].className = "inactive";
    }

    //Load the new API
    previous_doc = docs[doc];
    previous_menu_item = doc;
    previous_doc.show();

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
        'Result Count': 2,
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
    var menus = {
        "Results": {
            "summerfields": [{
                "filter": "none",
                "price": "6.99",
                "description": "all burgers are served with french fries. If your topping choice is not available as a preset, indicate in special requests your topping...",
                "title": "Regular burger"
            }, {
                "filter": "none",
                "price": "6.99",
                "description": "served with french fries",
                "title": "Cheddar cheeseburger"
            }],
            "latenight": [{
                "filter": "none",
                "price": "7.5",
                "description": "burger with lettuce and tomato ",
                "title": "Plain jane"
            }, {
                "filter": "none",
                "price": "7.95",
                "description": "burger with lettuce, tomato, and american cheese",
                "title": "Plain jane with cheese"
            }],
            "usdan": [{
                "time": "2014-11-02T19:01:07.995000",
                "breakfast": [{
                    'classics': [{
                        'extra': 'prepared with hoisin sauce, oyster sauce, soy sauce, fish sauce, garlic, ginger, sriracha, lemon grass, butter and pineapple',
                        'title': ' spicy scallop stir fry;'
                    }],
                    'pastabilities': [{
                        'extra': 'local tomatoes \nHorse Listeners Orchard',
                        'title': ' meat sauce;'
                    }, {
                        'extra': '',
                        'title': ' mushroom ragout;'
                    }]
                }],
                "lunch": []
            }],
            "redandblack": [{
                "data": {
                    "info": [
                        "American on white"
                    ],
                    "category": [
                        "kids menu"
                    ],
                    "price": [
                        "$3.95"
                    ]
                },
                "name": "Grilled Cheese"
            }, {
                "data": {
                    "info": [
                        "Crisp romaine lettuce tossed with grilled chicken, homemade croutons, authentic Caesar dressing and grated Parmesan cheese."
                    ],
                    "category": [
                        "salad"
                    ],
                    "price": [
                        "$9.25"
                    ]
                },
                "name": "Chicken Caesar Salad"
            }]
        }
    }

    var film_series = {
        "Result Count": 1,
        "Results": [{
            "data": {
                "short": [
                    "1972. USA. Dir: John Waters. With Divine, David Lochary. 93 min."
                ],
                "imdb": [
                    "http://www.imdb.com/title/tt0069089/"
                ],
                "long": [
                    "Yes, Divine does eat dog shit at the end, but Waters' cult classic has many more playful perversions up its sleeve. This black comedy chronicles a fight for the obscene, as an upper middle class couple scheme to steal a trash-talking drag queen's title of 'The Filthiest Person Alive.'"
                ],
                "time": [
                    "2014-11-05T00:00:00"
                ]
            },
            "name": "Pink Flamingos"
        }]
    }
    var directory = {
        "Result Count": 26,
        "Results": [{
            "data": {
                "hours": [
                    "Daily, 9:30pm - 1am"
                ],
                "info": [
                    "Text-To-Order: 860-724-2526"
                ],
                "category": "dining"
            },
            "name": "Late Night"
        }, {
            "data": {
                "hours": [
                    "Tuesday - Saturday, 10am - 4:30pm"
                ],
                "category": "other"
            },
            "name": "Usdan Box Office"
        }]
    }
    var json_collection = {
        "#json-status": status,
        "#json-events": events,
        "#json-menus": menus,
        "#json-film_series": film_series,
        "#json-directory": directory
    };

    for (j in json_collection) {
        $(j).JSONView(json_collection[j]);
    }
    // with options
    // $("#json-collasped").JSONView(json, {
    //     collapsed: true
    // });
}
