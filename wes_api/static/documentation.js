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
}

function set_on_click_listeners() {
    $("#apiNav li").on('click', function(e) {
        console.log(e.target)
        load_doc(e.target.id);
    })
}

function load_doc(doc) {
    console.log(doc, "?")
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
    console.log(previous_doc,doc);

    //Change api menu bar to show current api tab
    var menuEl = $("li #" + doc);
    menuEl[0].className = "active";
}
