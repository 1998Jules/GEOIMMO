document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les cartes dans les modales
    document.querySelectorAll('[id^="map-modal-"]').forEach(mapElement => {
        const bienId = mapElement.id.split('-')[2];
        const coords = getCoordsFromModal(bienId); // Fonction à implémenter selon votre modèle
        
        if (coords) {
            const map = L.map(mapElement.id).setView([coords.lat, coords.lng], 15);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap'
            }).addTo(map);
            
            L.marker([coords.lat, coords.lng]).addTo(map)
                .bindPopup('Localisation du bien');
        }
    });
    
    // Fonction pour extraire les coordonnées (à adapter)
    function getCoordsFromModal(bienId) {
        // Implémentez cette fonction selon comment vous stockez les coordonnées
        // Par exemple, vous pourriez avoir un champ hidden dans le modal
        const hiddenField = document.getElementById(`coords-${bienId}`);
        if (hiddenField) {
            const [lng, lat] = hiddenField.value.split(',');
            return { lat: parseFloat(lat), lng: parseFloat(lng) };
        }
        return null;
    }
});