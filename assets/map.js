var map = L.map('map').setView([45.768, 10.723], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

document.body.onload = function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.send(null);
    xhr.onload = function() {
        pinpoint(JSON.parse(xhr.responseText));
    }
}

pinned = [];
function pinpoint(data) {
    data.forEach(city => {
        if(!pinned.includes(city.arrival)) {
            pinned.push(city.arrival);
            L.marker([city.arrival_loc[0], city.arrival_loc[1]]).addTo(map).bindPopup(city.arrival + ' (' + city.formatted_price + ' €)');
        }
    })
}