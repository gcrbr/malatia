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
    if(["flixbus", "itabus", "ryanair"].includes(carrier)) {
        return '<img class="carrier" src="assets/images/' + carrier.toLowerCase() + '-logo.png" alt="' + carrier +'"/>';
    }else {
        return carrier;
    }
}

function parse_trips(trips) {
    trips.forEach(trip => {
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
    if(!set) {
        set = true;
        document.querySelector('.partenza') = trip_list[0].departure;
    }
    for(i=0;i<amount;++i) {
        if(trip_list[i]) {
            document.querySelector('#trips').innerHTML += trip_list[i];
            trip_list.shift();
        }
    }
    if(trip_list.length == 0) {
        document.querySelector('.loadbutton').style.display = 'none';
    }
}

document.body.onload = function() {get_trips();}
document.querySelector('.loadbutton').onclick = function() {load_trips(10);}