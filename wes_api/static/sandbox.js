$(document).ready(initialize_sandbox);

subtype_forms = {}
previous_form = null;

function initialize_sandbox() {
    // Define dict of subtype forms here
    subtype_forms = {
        'eventsToday': $("#eventsTodayForm"),
        'eventsLatest': $("#eventsLatestForm"),
        'eventsSearch': $("#eventsSearchForm")
    }
    previous_form = subtype_forms['eventsLatest'];

    //set click listeners
    set_on_click_listeners();

    // override form submits
    for (s in subtype_forms) {
        subtype_forms[s].submit(function(e) {
            var form = $(this);
            // console.log(form.attr('action'))
            $.ajax({
                url: form.attr('action'),
                type: form.attr('method'),
                data: form.serialize(), // data to be submitted
                success: function(response) {
                    console.log(this);
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
    // hide previous form
    if (previous_form) {
        previous_form.hide();
    }
    // Clear Results
    $("#json").text("");
    clear_current_api_url();
    previous_form = subtype_forms[subtype];
    previous_form.show();
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

function display_json_result(json) {
    $("#json").JSONView(json);
    // with options
    // $("#json-collasped").JSONView(json, {
    //     collapsed: true
    // });
}
