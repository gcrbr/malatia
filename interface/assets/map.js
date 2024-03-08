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
function pinpoint(data) {
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
                    city.arrival + '<br>' + city.formatted_price + ' EUR',
                    {
                        maxWidth: 200
                    }
                );
        }
    })
}