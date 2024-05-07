function traverse_trips(callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.send(null);
    xhr.onload = function() {
        callback(JSON.parse(xhr.responseText));
    };
}

function parse_carrier_logo(carrier) {
    return '<img class="carrier" src="assets/images/carriers/' + carrier.toLowerCase() + '.png" alt="' + carrier +'"/>';
}

function $(selector) {
    return document.querySelector(selector);
}

function show_modal() {
    $('#modal').style.display = 'block';
}

function hide_modal() {
    $('#modal').style.display = 'none';
}

function build_tr_from_trip(trip) {
    tr = '<tr>';
    tr += '<td>' + trip.date + '</td>';
    tr += '<td>' + trip.time + '</td>';
    //tr += '<td>' + trip.departure + '</td>';
    tr += '<td>' + trip.arrival + '</td>';
    tr += '<td>' + parse_carrier_logo(trip.carrier) + '</td>';
    tr += '<td>' + trip.duration + '</td>';
    tr += '<td>' + trip.formatted_price + ' EUR</td>';
    tr += '</tr>';
    return tr;
}