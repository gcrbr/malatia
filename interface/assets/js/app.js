set = false;
trip_list = Array();
var shown_trips = 0;

function parse_trips(trips) {
    trips.forEach(trip => {
        if(!set) {
            set = true;
            $('#partenza').innerHTML = trip.departure.toUpperCase();
        }
        trip_list.push(build_tr_from_trip(trip));
    });
    load_trips(10);
}

function load_trips(amount) {
    for(i=0; i < amount; ++i) {
        pop = trip_list.shift();
        if(pop) {
            shown_trips++;
            $('#trips').innerHTML += pop;
        }
    }
    if(trip_list.length == 0) {
        $('#loadbutton').style.display = 'none';
    }
}

document.body.onload = function() {
    traverse_trips(parse_trips);
}

$('#loadbutton').onclick = function() {
    load_trips(10);
}

$('#mapbutton').onclick = function() {
    window.open('map.html', '_blank', 'modal=yes');
}

$('#statsbutton').onclick = function() {
    window.open('stats.html', '_blank', 'modal=yes');
}