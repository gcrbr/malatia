var map = L.map('map').setView([45.768, 10.723], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | <a href="https://github.com/gcrbr/malatia">Malatìa</a>'
}).addTo(map);

document.body.onload = traverse_trips(pinpoint);

var mPinPoint = L.icon({
    iconUrl: 'assets/images/pinpoint.png',
    iconSize: [20, 20],
    iconAnchor: [0, 0],
    popupAnchor: [10, 5]
});

pinned = [];
trip_number = 0;
var trips = [];
function pinpoint(data) {
    trips = data;
    data.forEach(city => {
        if(!pinned.includes(city.arrival)) {
            pinned.push(city.arrival);
            L.marker(
                [
                    city.arrival_loc[0], 
                    city.arrival_loc[1]
                ],
                {
                    icon: mPinPoint
                }).addTo(map).bindPopup(
                    city.arrival + '<br>' + city.formatted_price + ' EUR <br> <button class="button-small" onclick="open_trip(' + trip_number + ')"><i class="fa fa-eye"></i> View trip</button>',
                    {
                        maxWidth: 200
                    }
                );
        }
        trip_number++;
    })
}

$('#modal-close').onclick = hide_modal;

function open_trip(number) {
    modalContent = $('#modal-content');
    modalContent.innerHTML = '<table>' + build_tr_from_trip(trips[number]).innerHTML + '</table>';
    show_modal();
}