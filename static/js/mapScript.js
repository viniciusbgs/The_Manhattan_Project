const map = L.map('map',{
    zoomControl: false
}).setView([40.783360, -73.964351], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let heatLayer = null;
let currentYear = MIN_YEAR;

async function loadYearData(year) {
    try {
        const endpoint = `/data/${year}`;
        const response = await fetch(endpoint, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });
        const result = await response.json();
        
        if (result.error) {
            console.error(result.error);
            return;
        }

        // Remove existing heat layer if it exists
        if (heatLayer) {
            map.removeLayer(heatLayer);
        }
        
        // Format data for heatmap
        // Each point is [lat, lng, intensity] where intensity is based on price
        const heatData = result.data.map(property => {
            // Normalize the sale price to get intensity (0-1 range)
            // You might want to adjust this logic based on your price range
            const maxPrice = 10000000; // Example max price $10M
            const intensity = Math.min(property['SALE PRICE'] / maxPrice, 1);
            
            return [
                property.LATITUDE, 
                property.LONGITUDE, 
                intensity
            ];
        });
        
        // Create and add heat layer
        heatLayer = L.heatLayer(heatData, {
            radius: 20,
            blur: 15,
            maxZoom: 17,
            // Gradient defines the colors of the heatmap
            gradient: {
                0.2: 'blue',
                0.4: 'lime',
                0.6: 'yellow',
                0.8: 'orange',
                1.0: 'red'
            }
        }).addTo(map);
        
        // Add click handler to show property details
        map.on('click', function(e) {
            // Find properties near the click point
            const clickLat = e.latlng.lat;
            const clickLng = e.latlng.lng;
            const threshold = 0.001; // Approximate radius to search
            
            const nearbyProperties = result.data.filter(property => 
                Math.abs(property.LATITUDE - clickLat) < threshold && 
                Math.abs(property.LONGITUDE - clickLng) < threshold
            );
            
            if (nearbyProperties.length > 0) {
                // Show the closest property
                const property = nearbyProperties[0];
                L.popup()
                    .setLatLng([property.LATITUDE, property.LONGITUDE])
                    .setContent(`
                        <b>Price:</b> $${property['SALE PRICE'].toLocaleString()}<br>
                        <b>Latitude:</b> ${property.LATITUDE.toFixed(6)}<br>
                        <b>Longitude:</b> ${property.LONGITUDE.toFixed(6)}
                    `)
                    .openOn(map);
            }
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// Events
document.getElementById('yearSlider').addEventListener('input', (e) => {
    currentYear = parseInt(e.target.value);
    document.getElementById('yearValue').textContent = currentYear;
    loadYearData(currentYear);
});

// Function to redirect to the "Game" page
function irParaGame() {
    window.location.href = "/game";
}

// Load initial data
loadYearData(currentYear);