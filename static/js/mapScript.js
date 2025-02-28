const map = L.map('map',{
    zoomControl: false
}).setView([40.783360, -73.964351], 10);

// Base maps
const baseMaps = {
    "Light": L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'),
    "Dark": L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'),
};
  
// Add the default style to the map
baseMaps["Dark"].addTo(map);

let heatLayer = null;
let currentYear = MIN_YEAR;

async function loadYearData(year) {
    try {
        const endpoint = `/data/${year}`;
        const response = await fetch(endpoint, {
            headers: { "X-Requested-With": "XMLHttpRequest" } // Add header to differentiate with the user
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

        // Check if there is data for that year
        if (result.data.length === 0) {
            console.warn('No data found for the selected year.');
            return;
        }
        
        // Format data for heatmap
        // Each point is [lat, lng, intensity] where intensity is based on price
        const heatData = result.data.map(sale => {
            // Normalize the sale price to get intensity (0-1 range)
            // Boost the intensity because the max_price is an outlier
            const intensity = Math.min((sale.SALE_PRICE / result.max_price) * 25, 1);
            
            return [
                sale.LATITUDE, 
                sale.LONGITUDE, 
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