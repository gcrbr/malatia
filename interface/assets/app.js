set = false;

trip_list = Array();

var shown_trips = 0;

function get_trips() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.send(null);
    xhr.onload = function() {
        parse_trips(JSON.parse(xhr.responseText));
        if(location.hash) {
            const query = location.hash.substring(1);
            show_trip(parseInt(query));
        }
    }
}

function parse_carrier_logo(carrier) {
    return '<img class="carrier" src="assets/images/' + carrier.toLowerCase() + '-logo.png" alt="' + carrier +'"/>';
}

function parse_trips(trips) {
    trips.forEach(trip => {
        if(!set) {
            set = true;
            document.querySelector('#partenza').innerHTML = trip.departure.toUpperCase();
        }
        tr = '<tr>';
        tr += '<td>' + trip.date + '</td>';
        tr += '<td>' + trip.time + '</td>';
        //tr += '<td>' + trip.departure + '</td>';
        tr += '<td>' + trip.arrival + '</td>';
        tr += '<td>' + parse_carrier_logo(trip.carrier) + '</td>';
        tr += '<td>' + trip.duration + '</td>';
        tr += '<td>' + trip.formatted_price + ' EUR</td>';
        tr += '</tr>';
        trip_list.push(tr);
    });
    load_trips(10);
}

function load_trips(amount) {
    for(i=0;i<amount;++i) {
        pop = trip_list.shift();
        if(pop) {
            shown_trips++;
            document.querySelector('#trips').innerHTML += pop;
        }
    }
    if(trip_list.length == 0) {
        document.querySelector('#loadbutton').style.display = 'none';
    }
}

function show_trip(number) {
    if(number > shown_trips) {
        /*var diff = number - shown_trips;
        var delay = setInterval(function() {
            if(diff > 0) {
                load_trips(20);
                diff -= 20;
            }else {
                clearInterval(delay);
            }
        }, 100);*/
        load_trips(number - shown_trips);
    }
    var trip_block = document.getElementsByTagName('tr')[number];
    trip_block.childNodes.forEach(function(node) {
        node.style.background = '#303030';
    });
    trip_block.scrollIntoView();
}

document.body.onload = function() {get_trips();}
document.querySelector('#loadbutton').onclick = function() {load_trips(10);}
document.querySelector('#mapbutton').onclick = function() {window.open('map.html', '_blank', 'modal=yes');}
document.querySelector('#statsbutton').onclick = function() {window.open('stats.html', '_blank', 'modal=yes');}