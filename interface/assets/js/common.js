function traverse_trips(callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.send(null);
    xhr.onload = function () {
        callback(JSON.parse(xhr.responseText));
    };
}

function parse_carrier_logo(carrier) {
    return '<img class="carrier" src="assets/images/carriers/' + carrier.toLowerCase() + '.png" alt="' + carrier + '"/>';
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
    tr = document.createElement('tr');

    td = document.createElement('td');
    td.innerHTML = trip.date;
    tr.appendChild(td);

    td = document.createElement('td');
    td.innerHTML = trip.time;
    tr.appendChild(td);

    td = document.createElement('td');
    td.innerHTML = trip.arrival;
    tr.appendChild(td);

    td = document.createElement('td');
    td.innerHTML = parse_carrier_logo(trip.carrier);
    tr.appendChild(td);

    td = document.createElement('td');
    td.innerHTML = trip.duration;
    tr.appendChild(td);

    td = document.createElement('td');
    td.innerHTML = trip.formatted_price || (trip.price + ' EUR');
    tr.appendChild(td);

    return tr;
}

function toggle_trip_group(id) {
    for (let block of document.getElementsByClassName('group_' + id)) {
        block.style.display = block.style.display == 'none' ? 'table-row' : 'none';
    }
}

var counter = 0;
function build_tr_from_group_of_trips(trips) {
    sub_trs = [];
    trips.forEach(trip => {
        let trip_block = build_tr_from_trip(trip);
        trip_block.style.display = 'none';
        trip_block.setAttribute('class', 'group_' + counter);
        sub_trs.push(trip_block);
    });

    container = document.createElement('tbody');

    m_tr = document.createElement('tr');
    m_tr.setAttribute('id', 'toggable');
    m_tr.setAttribute('style', 'cursor: pointer;');
    m_tr.setAttribute('onclick', 'toggle_trip_group(' + counter + ')');

    td = document.createElement('td');
    td.innerHTML = '<i class="fa fa-chevron-down" style="font-size: 0.8rem; opacity: 0.5;"></i>';
    m_tr.appendChild(td);

    td = document.createElement('td');
    td.innerHTML = '*';
    m_tr.appendChild(td);

    td = document.createElement('td');
    td.innerHTML = trips[0].arrival;
    m_tr.appendChild(td);

    td = document.createElement('td');
    //td.innerHTML = 'VARIOUS';
    m_tr.appendChild(td);

    td = document.createElement('td');
    m_tr.appendChild(td);

    td = document.createElement('td');
    td.innerHTML = 'FROM ' + trips[0].price + ' EUR';
    m_tr.appendChild(td);

    container.appendChild(m_tr);

    for (let sub_tr of sub_trs) {
        container.appendChild(sub_tr);
    }

    ++counter;
    return container;
}