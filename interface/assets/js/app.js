set = false;
trip_list = [];
var shown_trips = 0;

function parse_trips(trips) {
    // Sort by price globally first
    trips.sort((a, b) => a.price - b.price);

    var groups = {};
    trips.forEach(trip => {
        if (!groups[trip.arrival]) groups[trip.arrival] = [];
        groups[trip.arrival].push(trip);
        if (!set) {
            set = true;
            $('#partenza').innerHTML = trip.departure.toUpperCase();
        }
    });

    // Clear list before adding
    trip_list = [];
    for (const [_, group] of Object.entries(groups)) {
        trip_list.push(group.length > 1 ? build_tr_from_group_of_trips(group) : build_tr_from_trip(group[0]));
    }
    load_trips(10);
}

function load_trips(amount) {
    const table = $('#trips');
    for (i = 0; i < amount; ++i) {
        let pop = trip_list.shift();
        if (pop) {
            shown_trips++;
            table.appendChild(pop);
        }
    }
    if (trip_list.length == 0) {
        $('#loadbutton').style.display = 'none';
    }
}

document.body.onload = function () {
    traverse_trips(parse_trips);
}

$('#loadbutton').onclick = function () {
    load_trips(10);
}

$('#mapbutton').onclick = function () {
    window.open('map.html', '_blank', 'modal=yes');
}

$('#statsbutton').onclick = function () {
    window.open('stats.html', '_blank', 'modal=yes');
}