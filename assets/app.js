set = false;

trip_list = Array();

function get_trips() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.send(null);
    xhr.onload = function() {
        parse_trips(JSON.parse(xhr.responseText));
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
            document.querySelector('#trips').innerHTML += pop;
        }
    }
    if(trip_list.length == 0) {
        document.querySelector('#loadbutton').style.display = 'none';
    }
}

document.body.onload = function() {get_trips();}
document.querySelector('#loadbutton').onclick = function() {load_trips(10);}
document.querySelector('#mapbutton').onclick = function() {window.open('map.html', '_blank');}