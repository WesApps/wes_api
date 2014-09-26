$(document).ready(initialize_index)

function initialize_index() {
    get_film_today();
}

function get_film_today() {
    var data = $.getJSON("/api/filmseries/today", function(res) {
            if (!(res)) {
                return {};
            } else {
                return film_callback(res);
            }
        })
        // console.log(data)
}

function time_from_string(str_time) {
    var msec = Date.parse(str_time);
    var d = new Date(msec);
    return d.toDateString()+", "+d.toLocaleTimeString();
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
    var title = results.title;
    var short_description = results.short_description;
    var time = time_from_string(results.time);
    var long_description = results.long_description;

    var innerhtml = "<div id='film_title' class='randomData'><b>Title: </b>" + title + "</div>";
    innerhtml += "<div id='film_short_description' class='randomData'><b>Info: </b>" + short_description + "</div>";
    innerhtml += "<div id='film_time' class='randomData'><b>Time: </b>" + time + "</div>";
    innerhtml += "<div id='long_description' class='randomData'><b>Description: </b>" + long_description + "</div>";

    // Set the text of the container on the page
    data_div.innerHTML = innerhtml;
}
