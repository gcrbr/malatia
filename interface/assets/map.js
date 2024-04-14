var map = L.map('map').setView([45.768, 10.723], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | <a href="https://github.com/gcrbr/malatia">Malatìa</a>'
}).addTo(map);

document.body.onload = function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.send(null);
    xhr.onload = function() {
        pinpoint(JSON.parse(xhr.responseText));
    }
}

var mPinPoint = L.icon({
    iconUrl: 'assets/images/pinpoint.png',
    iconSize: [20, 20],
    iconAnchor: [0, 0],
    popupAnchor: [10, 5]
})

pinned = [];
trip_number = 0;
function pinpoint(data) {
    data.forEach(city => {
        trip_number++;
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
                    city.arrival + '<br>' + city.formatted_price + ' EUR <br> <button onclick="open_trip(' + trip_number + ')"><i class="fa fa-eye"></i> View trip</button>',
                    {
                        maxWidth: 200
                    }
                );
        }
    })
}

function open_trip(number) {
    window.opener.show_trip(number);
    window.opener.focus(); // not working :(
}