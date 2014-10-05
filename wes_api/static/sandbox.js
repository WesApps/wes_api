$(document).ready(initialize_sandbox);

subtype_forms = {}
apis = {}
previous_form = null;
previous_API = null;

function initialize_sandbox() {
    // Define dict of subtype forms here
    subtype_forms = {
        'eventsToday': $("#eventsTodayForm"),
        'eventsLatest': $("#eventsLatestForm"),
        'eventsSearch': $("#eventsSearchForm"),
        'menusToday': $("#menusTodayForm"),
        'menusLatest': $("#menusLatestForm"),
        'filmseriesToday': $("#filmseriesTodayForm"),
        'filmseriesLatest': $("#filmseriesLatestForm"),
        'wesMapsSearch': $("#wesMapsSearchForm")

    }

    // Define API types
    apis = {
        'menusAPITab': $("#menusAPI"),
        'eventsAPITab': $("#eventsAPI"),
        'filmseriesAPITab': $("#filmseriesAPI"),
        'wesMapsAPITab': $("#wesMapsAPI")
    }

    defaults = {
        'menusAPITab': "menusToday",
        'eventsAPITab': "eventsToday",
        'filmseriesAPITab': "filmseriesToday",
        'wesMapsAPITab': "wesMapsSearch"
    }

    //Default API and subtype
    previous_form = subtype_forms['eventsToday'];
    previous_API = apis['eventsAPI'];

    //Load default API and subtype
    load_api("eventsAPITab");
    load_subtype_form(defaults['eventsAPITab']);

    //set click listeners
    set_on_click_listeners();

    // override form submits
    for (s in subtype_forms) {
        subtype_forms[s].submit(function(e) {
            var form = $(this);
            $.ajax({
                url: form.attr('action'),
                type: form.attr('method'),
                data: form.serialize(), // data to be submitted
                success: function(response) {
                    show_results();
                    display_json_result(response); // do what you like with the response
                    set_current_api_url(this.url);
                }
            });
            return false;
        });
    }
}

function set_current_api_url(url) {
    $("#resultUrl").val("http://wesapi.com/" + url);
}

function clear_current_api_url() {
    $("#resultUrl").val("");
}

function load_subtype_form(subtype) {
    if (!(subtype in subtype_forms)) {
        console.log("Uh oh. Bad subtype.");
        return;
    }
    console.log(subtype, "SUB")
        // hide previous form
    if (previous_form) {
        previous_form.hide();
    }
    // Clear Results
    $("#json").text("");
    clear_current_api_url();
    previous_form = subtype_forms[subtype];
    previous_form.show();
    hide_results();
}

function load_api(api) {
    if (!(api in apis)) {
        console.log("Uh oh. Bad API.", api);
        return;
    }
    //Hide the old API
    if (previous_API) {
        previous_API.hide();
        //Change api menu bar for previous API
        var menuEl = $("li #" + previous_API[0].id + "Tab");
        menuEl[0].className = "";
        menuEl[1].className = "hiddenAPI";
    }

    //Load the new API
    previous_API = apis[api];
    previous_API.show();

    //Change api menu bar to show current api tab
    var menuEl = $("li #" + api);
    menuEl[0].className = "hiddenAPI";
    menuEl[1].className = "";

    //Load the default subtype for this API
    load_subtype_form(defaults[api]);

    //Check the radio button for that default API
    console.log($("#" + defaults[api]))
    $("#" + defaults[api])[0].checked = true;

    //Hide results
    hide_results();
}

function set_on_click_listeners() {
    //API type listeners
    $(".nav-tabs li").on('click', function(e) {
        load_api(e.target.id)
    })

    // subtype listeners
    $("#subtypeSelect input").on('click', function(e) {
        load_subtype_form(e.target.id);
    })
}

function show_results() {
    $("#results").show();
}

function hide_results() {
    $("#results").hide();
}

function display_json_result(json) {
    $("#json").JSONView(json);
    // with options
    // $("#json-collasped").JSONView(json, {
    //     collapsed: true
    // });
}
