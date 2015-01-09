$(document).ready(initialize_index)

function initialize_index() {
    get_film_upcoming();
    get_status();
}

function get_status() {
    var data = $.getJSON("/api/status", function(res) {
        if (!(res)) {
            return {};
        } else {
            return populate_status(res);
        }
    })
}

function populate_status(response) {
    console.log(response);

    var apis = {
        "events": [$("#events_status")[0], $("#events_updated")[0]],
        "film_series": [$("#film_series_status")[0], $("#film_series_updated")[0]],
        "menus": [$("#menus_status")[0], $("#menus_updated")[0]],
        "directory": [$("#directory_status")[0], $("#directory_updated")[0]]
    }

    // ignores things that aren't in the status response,
    // so directory is hardcoded offline now,
    // but events, film_series, and menus are dynamic.
    for (i in apis) {
        if (response[i]) {
            if (response[i]["status"]) {
                apis[i][0].innerHTML = "nominal";
                apis[i][0].className = "label label-outline label-green";
            } else {
                apis[i][0].innerHTML = "offline";
                apis[i][0].className = "label label-outline label-red";
            }
            if (response[i]["time"]) {
                var r_date = new Date(response[i]["time"]);
                var f_date = new Date(r_date.getUTCFullYear(), r_date.getUTCMonth(),
                    r_date.getUTCDate(), r_date.getUTCHours(),
                    r_date.getUTCMinutes(), r_date.getUTCSeconds());
                apis[i][1].innerHTML = "Last Updated: " + f_date.toLocaleString();
            } else {
                apis[i][1].innerHTML = "Last Updated: Never";
            }
        }
    }
}

function get_film_upcoming() {
    var data = $.getJSON("/api/filmseries/all", function(res) {
        if (!(res)) {
            return {};
        } else {
            return film_callback(res);
        }
    })
}

function time_from_string(str_time) {
    var msec = Date.parse(str_time);
    var d = new Date(msec);
    return d.toDateString() + ", " + d.toLocaleTimeString();
}

function film_callback(response) {
    data_div = $(".randomData")[0];
    if (!(response) || (response['Result Count'] < 1)) {
        err_div = document.createElement("div");
        err_div.setAttribute("class", "err_div");
        err_div.innerHTML = "No film today.";
        data_div.innerHTML = err_div;
        return;
    }
    var results = response['Results'][0];
    var title = results["name"];
    var results_data = results["data"]
    var short_description = results_data["short"];
    var time = time_from_string(results_data["time"]);
    var long_description = results_data["long"];
    console.log(response["Results"][0])

    var innerhtml = "<div id='film_title' class='randomData'><b>Title: </b>" + title + "</div>";
    innerhtml += "<div id='film_short_description' class='randomData'><b>Info: </b>" + short_description + "</div>";
    innerhtml += "<div id='film_time' class='randomData'><b>Time: </b>" + time + "</div>";
    innerhtml += "<div id='long_description' class='randomData'><b>Description: </b>" + long_description + "</div>";

    // Set the text of the container on the page
    data_div.innerHTML = innerhtml;
}
