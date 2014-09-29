$(document).ready(initialize_try);

function initialize_try() {
    var json = {
        "Result Count": 4,
        "Results": [{
            "category": "Student Groups",
            "description": "From Talia Baurer '15:The senior CAs are at it again! Start out your Saturday night withyummy s'mores around a campfire in the Home Ave backyards. Guitarsencouraged.Date: Saturday, September 27Time: 8PM-10PMPlace: 52 Home Ave.",
            "source": "Wesleying",
            "link": "http://wesleying.org/2014/09/26/smores-on-home/?utm_source=rss&utm_medium=rss&utm_campaign=smores-on-home",
            "location": "52 Home Ave.",
            "time": "2014-09-27T20:00:00",
            "name": "Smores on Home"
        }, {
            "category": "Student Groups",
            "description": "From Andrew Chatfield:The exhibition “A World of Dreams” includes new large-scale paintings in which Professor of Art Tula Telfair presents monumental landscapes and epic-scale vistas that are simultaneously awe-inspiring and intimate. She combines stillness with motion, solitude with universality, and definition with suggestion in her bold and quiet works. Ms. Telfair’s paintings are fully contemporary in their [...]",
            "source": "Wesleying",
            "link": "http://wesleying.org/2014/09/26/artist-talk-tula-telfair/?utm_source=rss&utm_medium=rss&utm_campaign=artist-talk-tula-telfair",
            "location": "CFA Hall",
            "time": "2014-09-27T14:00:00",
            "name": "Artist TalkTula Telfair"
        }, {
            "category": "Auditions",
            "description": "From Sophia Jennings '16:Date: Saturday, September 27th, 2014Time: 1PMPlace: Albritton 103",
            "source": "Wesleying",
            "link": "http://wesleying.org/2014/09/26/audition-for-jimmy-okeeffes-film-thesis/?utm_source=rss&utm_medium=rss&utm_campaign=auditio</div>n-for-jimmy-okeeffes-film-thesis",
            "location": "Albritton 103",
            "time": "2014-09-27T13:00:00",
            "name": "Audition for Jimmy OKeeffes Film Thesis"
        }, {
            "category": "Student Groups",
            "description": "From Isabel Fine '17:Parents stressing you out? You stressing parents out? Don't know whatto do with your parents? Then come to FAMILY WEEKEND YOGA sponsored byWesBAM!Drop your parents off, come as a family, bring someone else's family,anything you want goes. This class will be fun, relaxing, and open topractitioners of all levels and ages.Date: Saturday, September [...]",
            "source": "Wesleying",
            "link": "http://wesleying.org/2014/09/26/family-weekend-yoga/?utm_source=rss&utm_medium=rss&utm_campaign=family-weekend-yoga",
            "location": "Westco Lounge",
            "time": "2014-09-27T05:00:00",
            "name": "Family Weekend Yoga"
        }]
    }

    $("#json").JSONView(json);
    // with options
    $("#json-collasped").JSONView(json, {
        collapsed: true
    });
}
