document.body.onload = function () {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.send(null);
    xhr.onload = function () {
        const trips = JSON.parse(xhr.responseText);
        build_graphs(trips);
    }
}

function build_graphs(trips) {
    // Filtriamo i viaggi che hanno un prezzo valido
    const validTrips = trips.filter(t => t.price != null && !isNaN(Number(t.price)));
    if (!validTrips.length) return;

    // Troviamo il minimo e il massimo reale
    const prices = validTrips.map(t => Number(t.price)).sort((a, b) => a - b);
    const minP = prices[0];
    const maxP = prices[prices.length - 1];

    const range = maxP - minP;
    const interval = range / 5 || 1; // Fallback a 1 se tutti i prezzi sono uguali

    let groups = [0, 0, 0, 0, 0];
    let carriers = {};
    let group_names = [];

    // Generiamo i nomi dei range con precisione fissa a 2 decimali
    for (let i = 0; i < 5; i++) {
        let start = minP + (interval * i);
        let end = minP + (interval * (i + 1));

        // L'ultima fascia deve includere esattamente il massimo
        if (i === 4) end = maxP;

        group_names.push(`${start.toFixed(2)} - ${end.toFixed(2)} EUR`);
    }

    validTrips.forEach(trip => {
        const p = Number(trip.price);
        // Calcoliamo l'indice in base a quanto il prezzo dista dal minimo
        let idx = Math.floor((p - minP) / interval);
        if (idx > 4) idx = 4; // Sicurezza per l'estremo superiore
        if (idx < 0) idx = 0; // Sicurezza per l'estremo inferiore

        groups[idx]++;
        carriers[trip.carrier] = (carriers[trip.carrier] || 0) + 1;
    });
    const amber = '#ffb000';
    const amberGlow = 'rgba(255, 176, 0, 0.4)';

    const price_chart = new Chart(document.getElementById('trips_per_price'), {
        type: 'bar',
        data: {
            labels: group_names,
            datasets: [{
                label: 'Number of trips',
                data: groups,
                borderWidth: 1,
                backgroundColor: amber,
                borderColor: amber,
                hoverBackgroundColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: amber } },
                x: { grid: { display: false }, ticks: { color: amber } }
            },
            plugins: {
                legend: { labels: { color: '#fff', font: { family: 'Inter' } } }
            }
        }
    });

    const carrier_labels = Object.keys(carriers);
    const carrier_data = carrier_labels.map(key => carriers[key]);

    const carrier_chart = new Chart(document.getElementById('trips_by_carrier'), {
        type: 'pie',
        data: {
            labels: carrier_labels,
            datasets: [{
                label: 'Number of trips',
                data: carrier_data,
                borderWidth: 2,
                borderColor: '#0a0a0b',
                backgroundColor: [
                    '#ffb000', '#ffcc33', '#e69900', '#cc8400', '#b37400'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#fff', padding: 20, font: { family: 'Inter' } }
                }
            }
        }
    });
}