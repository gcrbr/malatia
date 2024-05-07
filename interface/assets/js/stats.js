document.body.onload = function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.send(null);
    xhr.onload = function() {
        const trips = JSON.parse(xhr.responseText);
        build_graphs(trips);
    }
}

function build_graphs(trips) {
    lowest_price = 0;
    highest_price = 0;
    trips.forEach(trip => {
        if(lowest_price == 0){
            lowest_price = trip.price;
        }
        highest_price = trip.price;
    });
    
    interval = (highest_price - lowest_price) / 5;
    groups = [0, 0, 0, 0, 0];
    carriers = {};
    group_names = [
        lowest_price + ' EUR - ' + (interval*1).toFixed(2) + ' EUR',
        (interval*1).toFixed(2) + ' EUR - ' + (interval*2).toFixed(2) + ' EUR',
        (interval*2).toFixed(2) + ' EUR - ' + (interval*3).toFixed(2) + ' EUR',
        (interval*3).toFixed(2) + ' EUR - ' + (interval*4).toFixed(2) + ' EUR',
        (interval*4).toFixed(2) + ' EUR - ' + highest_price + ' EUR',
    ];

    trips.forEach(trip => {
        for(i=1;i<=5;++i) {
            l = i==1 ? lowest_price : interval*i;
            h = i==5 ? highest_price : interval*(i+1);
            if(trip.price <= h && trip.price > l) {
                groups[i-1]++;
            }
        }
        carriers[trip.carrier] = (carriers[trip.carrier] == undefined) ? 1 : carriers[trip.carrier] + 1;
    });
    
    var price_chart = new Chart(document.getElementById('trips_per_price'), {
        type: 'bar',
        data: {
            labels: group_names,
            datasets: [{
                label: 'Number of trips',
                data: groups,
                borderWidth: 1,
                backgroundColor: '#d07c15'
            }]
        },
        options: {
            responsitve: true,
            aspectRatio: 1.5
        }
    });
    
    _carriers = [];
    for(const [key, value] of Object.entries(carriers)) {
        _carriers.push(value);
    }

    var carrier_chart = new Chart(document.getElementById('trips_by_carrier'), {
        type: 'pie',
        data: {
            labels: Object.keys(carriers),
            datasets: [{
                label: 'Number of trips',
                data: _carriers,
                borderWidth: 1,
                backgroundColor: '#d07c15'
            }]
        },
        options: {
            responsive: true,
            aspectRatio: 2
        }
    });
}