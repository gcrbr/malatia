var map = L.map('map').setView([45.768, 10.723], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | <a href="https://github.com/gcrbr/malatia">Malatìa</a>'
}).addTo(map);

document.body.onload = function () {
    traverse_trips(pinpoint);
};

var mPinPoint = L.icon({
    iconUrl: 'assets/images/pinpoint.png',
    iconSize: [20, 20],
    iconAnchor: [0, 0],
    popupAnchor: [10, 5]
});

var pinned = [];
var trip_number = 0;
var trips = [];

function pinpoint(data) {
    trips = data;
    data.forEach(city => {
        if (!pinned.includes(city.arrival) && city.arrival_loc) {
            pinned.push(city.arrival);
            L.marker(
                [
                    city.arrival_loc[0],
                    city.arrival_loc[1]
                ],
                {
                    icon: mPinPoint
                }).addTo(map).bindPopup(
                    city.arrival + '<br>' + (city.formatted_price || city.price) + ' EUR <br> <button class="button-small" onclick="open_trip(' + trip_number + ')"><i class="fa fa-eye"></i> View trip</button>',
                    {
                        maxWidth: 200
                    }
                );
        }
        trip_number++;
    });
}

const modalClose = $('#modal-close');
if (modalClose) {
    modalClose.onclick = hide_modal;
}

window.open_trip = function (number) {
    const modalContent = $('#modal-content');
    if (modalContent && trips[number]) {
        modalContent.innerHTML = '<table>' + build_tr_from_trip(trips[number]).outerHTML + '</table>';
        show_modal();
    }
};