document.addEventListener('DOMContentLoaded', function() {
    // Éléments du DOM
    const applyFiltersBtn = document.getElementById('apply-filters');
    const resetFiltersBtn = document.getElementById('reset-filters');
    const biensContainer = document.getElementById('biens-container');
    
    // Fonction principale de filtrage
    function filterBiens() {
        const typeValue = document.getElementById('filter-type').value.toLowerCase();
        const priceValue = parseFloat(document.getElementById('filter-price').value) || 0;
        const surfaceValue = parseFloat(document.getElementById('filter-surface').value) || 0;
        
        let hasVisibleItems = false;
        
        document.querySelectorAll('#biens-container > [data-type]').forEach(card => {
            const cardType = card.dataset.type.toLowerCase();
            const cardPrice = parseFloat(card.dataset.price);
            const cardSurface = parseFloat(card.dataset.surface);
            const cardStatut = card.dataset.statut.toLowerCase();
            
            // Conditions de filtrage
            const typeMatch = !typeValue || cardType.includes(typeValue);
            const priceMatch = !priceValue || cardPrice <= priceValue;
            const surfaceMatch = !surfaceValue || cardSurface >= surfaceValue;
            
            // Appliquer le filtre
            if (typeMatch && priceMatch && surfaceMatch) {
                card.style.display = 'block';
                hasVisibleItems = true;
                
                // Animation
                card.style.animation = 'fadeIn 0.5s ease-out';
            } else {
                card.style.display = 'none';
            }
        });
        
        // Afficher un message si aucun résultat
        const noResultsMsg = document.getElementById('no-results-message');
        if (!hasVisibleItems) {
            if (!noResultsMsg) {
                const message = document.createElement('div');
                message.id = 'no-results-message';
                message.className = 'col-12 text-center py-5';
                message.innerHTML = `
                    <i class="bi bi-exclamation-circle fs-1 text-muted"></i>
                    <h4 class="mt-3">Aucun bien ne correspond à vos critères</h4>
                    <button class="btn btn-outline-primary mt-3" id="reset-filters-msg">
                        Réinitialiser les filtres
                    </button>
                `;
                biensContainer.appendChild(message);
                
                // Gestion du bouton de réinitialisation dans le message
                document.getElementById('reset-filters-msg').addEventListener('click', resetFilters);
            }
        } else if (noResultsMsg) {
            noResultsMsg.remove();
        }
    }
    
    // Fonction de réinitialisation
    function resetFilters() {
        document.getElementById('filter-type').value = '';
        document.getElementById('filter-price').value = '';
        document.getElementById('filter-surface').value = '';
        
        document.querySelectorAll('#biens-container > [data-type]').forEach(card => {
            card.style.display = 'block';
            card.style.animation = 'fadeIn 0.5s ease-out';
        });
        
        const noResultsMsg = document.getElementById('no-results-message');
        if (noResultsMsg) noResultsMsg.remove();
    }
    
    // Événements
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', filterBiens);
    }
    
    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', resetFilters);
    }
    
    // Filtrer aussi quand on appuie sur Entrée
    document.querySelectorAll('#filter-type, #filter-price, #filter-surface').forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') filterBiens();
        });
    });
});