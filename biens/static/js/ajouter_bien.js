<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

        // Initialisation carte Leaflet
        const map = L.map('map').setView([6.1319, 1.2226], 13); // Lomé, Togo par défaut

        // Couche OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        let marker = null;

        // Clic sur la carte pour placer/move marker
        map.on('click', function(e) {
            const lat = e.latlng.lat.toFixed(6);
            const lng = e.latlng.lng.toFixed(6);

            if (marker) {
                marker.setLatLng(e.latlng);
            } else {
                marker = L.marker(e.latlng, { draggable: true }).addTo(map);
                marker.on('dragend', function(event) {
                    const pos = event.target.getLatLng();
                    updateLocationField(pos.lat, pos.lng);
                });
            }
            updateLocationField(lat, lng);
        });

        // Bouton "Me localiser"
        document.getElementById('locate-me').addEventListener('click', function() {
            if (!navigator.geolocation) {
                alert("La géolocalisation n'est pas supportée par votre navigateur.");
                return;
            }
            navigator.geolocation.getCurrentPosition(function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                map.setView([lat, lng], 16);
                if (marker) {
                    marker.setLatLng([lat, lng]);
                } else {
                    marker = L.marker([lat, lng], { draggable: true }).addTo(map);
                    marker.on('dragend', function(event) {
                        const pos = event.target.getLatLng();
                        updateLocationField(pos.lat, pos.lng);
                    });
                }
                updateLocationField(lat.toFixed(6), lng.toFixed(6));
            }, function() {
                alert("Impossible d'obtenir votre position.");
            });
        });

        // Met à jour le champ localisation (WKT)
        function updateLocationField(lat, lng) {
    const wkt = `POINT(${lng} ${lat})`;  // ✅ PAS D'ESPACE avant POINT
    document.getElementById('id_localisation').value = wkt;
}

        // Si localisation préremplie, placer le marker
        window.addEventListener('load', function() {
            const val = document.getElementById('id_localisation').value;
            if (val) {
                const matches = val.match(/POINT\(([-\d\.]+) ([-\d\.]+)\)/);
                if (matches) {
                    const lng = parseFloat(matches[1]);
                    const lat = parseFloat(matches[2]);
                    const latlng = L.latLng(lat, lng);
                    marker = L.marker(latlng, { draggable: true }).addTo(map);
                    map.setView(latlng, 16);
                    marker.on('dragend', function(event) {
                        const pos = event.target.getLatLng();
                        updateLocationField(pos.lat, pos.lng);
                    });
                }
            }
        });

        // Affichage des fichiers images supplémentaires sélectionnés
        document.getElementById('id_medias').addEventListener('change', function(e) {
            var files = e.target.files;
            var fileList = document.getElementById('file-list');
            fileList.innerHTML = '';
            
            if (files.length > 0) {
                var list = document.createElement('ul');
                list.className = 'list-unstyled';
                
                for (var i = 0; i < files.length; i++) {
                    var item = document.createElement('li');
                    item.className = 'd-flex align-items-center mb-2';
                    item.innerHTML = `
                        <i class="bi bi-file-image text-primary me-2"></i>
                        <span class="text-truncate" style="max-width: 250px">${files[i].name}</span>
                        <small class="text-muted ms-auto">${(files[i].size / 1024 / 1024).toFixed(2)} Mo</small>
                    `;
                    list.appendChild(item);
                }
                
                fileList.appendChild(list);
            }
        });

        // Validation image principale
        document.getElementById('id_image_principale').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                if (!file.type.match('image.*')) {
                    e.target.setCustomValidity('Veuillez sélectionner une image valide');
                } else {
                    e.target.setCustomValidity('');
                }
            }
        });
    