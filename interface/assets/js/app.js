set = false;
trip_list = Array();
var shown_trips = 0;

function parse_trips(trips) {
    var groups = {};
    trips.forEach(trip => {
        groups[trip.arrival] = trip.arrival in groups ? groups[trip.arrival].concat(trip) : [trip];
        if(!set) {
            set = true;
            $('#partenza').innerHTML = trip.departure.toUpperCase();
        }
    });
    for (const [_, group] of Object.entries(groups)) {
        trip_list.push(group.length > 1 ? build_tr_from_group_of_trips(group) : build_tr_from_trip(group[0]));
    }
    load_trips(10);
}

function load_trips(amount) {
    for(i=0; i < amount; ++i) {
        pop = trip_list.shift();
        if(pop) {
            shown_trips++;
            //$('#trips').innerHTML += pop;
            $('#trips').appendChild(pop);
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