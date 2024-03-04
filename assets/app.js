function get_trips() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.send(null);
    xhr.onload = function() {
        parse_trips(JSON.parse(xhr.responseText));
    }
}

function parse_carrier_logo(carrier) {
    if(carrier == "Flixbus" || carrier == "Ryanair") {
        return '<img class="carrier" src="assets/' + carrier.toLowerCase() + '-logo.png" alt="' + carrier +'"/>';
    }else {
        return carrier;
    }
}

function parse_trips(trips) {
    trips.forEach(trip => {
        tr = '<tr>';
        tr += '<td>' + trip.date + '</td>';
        tr += '<td>' + trip.time + '</td>';
        tr += '<td>' + trip.departure + '</td>';
        tr += '<td>' + trip.arrival + '</td>';
        tr += '<td>' + parse_carrier_logo(trip.carrier) + '</td>';
        tr += '<td>' + trip.duration + '</td>';
        tr += '<td>' + trip.formatted_price + ' EUR</td>';
        tr += '</tr>';
        document.querySelector('#trips').innerHTML += tr;
    });
}

document.body.onload = function() {get_trips();}