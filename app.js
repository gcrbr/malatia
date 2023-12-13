function get_trips() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.send(null);
    xhr.onload = function() {
        parse_trips(JSON.parse(xhr.responseText));
    }
}

function parse_trips(trips) {
    trips.forEach(trip => {
        tr = '<tr>';
        tr += '<td>' + trip.date + '</td>';
        tr += '<td>' + trip.departure + '</td>';
        tr += '<td>' + trip.arrival + '</td>';
        tr += '<td>' + trip.carrier + '</td>';
        tr += '<td>' + trip.duration + '</td>';
        tr += '<td>' + trip.formatted_price + '</td>';
        tr += '</tr>';
        document.querySelector('#trips').innerHTML += tr;
    });
}

document.body.onload = function() {get_trips();}