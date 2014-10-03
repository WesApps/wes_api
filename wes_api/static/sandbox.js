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
            console.log(form);
            $.ajax({
                url: form.attr('action'),
                type: form.attr('method'),
                data: form.serialize(), // data to be submitted
                success: function(response) {
                    console.log(response);
                    display_json_result(response); // do what you like with the response
                }
            });
            return false;
        });
    }
}




function load_subtype_form(subtype) {
    if (!(subtype in subtype_forms)) {
        console.log("Uh oh. Bad subtype.");
        return;
    }
    // hide 
    console.log(previous_form)
    if (previous_form) {
        previous_form.hide();
    }
    console.log(subtype_forms);
    previous_form = subtype_forms[subtype];
    previous_form.show()

}

function set_on_click_listeners() {
    // events
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
