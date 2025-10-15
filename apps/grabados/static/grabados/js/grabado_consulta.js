// Funciones para la tabla de consulta de grabados

function showFilters() {
    console.log("Función showFilters() llamada.");
    const modal = document.getElementById('filterModal');
    if (modal) {
        modal.style.display = 'block';
    }
}

function closeModal() {
    const modal = document.getElementById('filterModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function exportData() {
    console.log("Función exportData() llamada.");
    alert("Exportando datos...");
}

function refreshData() {
    console.log("Función refreshData() llamada.");
    alert("Actualizando datos de la tabla...");
}

function applyFilters() {
    // Logic to apply filters will go here
    console.log("Función applyFilters() llamada.");
    closeModal();
}

function clearFilters() {
    console.log("Función clearFilters() llamada.");
    alert("Limpiando filtros...");
}

$(document).ready(function() {
    // Modal de exportación
    var exportModal = document.getElementById("exportModal");
    var exportBtn = document.getElementById("exportBtn");
    var closeButton = document.getElementsByClassName("close-button")[0];

    if(exportBtn) {
        exportBtn.onclick = function() {
            exportModal.style.display = "block";
        }
    }

    if(closeButton) {
        closeButton.onclick = function() {
            exportModal.style.display = "none";
        }
    }

    // Cerrar modales si se hace clic fuera de ellos
    window.onclick = function(event) {
        const filterModal = document.getElementById('filterModal');
        if (event.target == filterModal) {
            closeModal();
        }
        if (event.target == exportModal) {
            exportModal.style.display = "none";
        }
    }

    // Conditionally initialize Select2 for the filter modal on the consultation page
    if ($('#filterModal').length) {
        $('#id_tipo_grabado').select2({
            placeholder: "Seleccione o busque un tipo",
            allowClear: true,
            width: '100%',
            dropdownParent: $('#filterModal .modal-content') // Attach dropdown to the modal
        });
    }

    // Initialize Select2 for all select elements on the new form page
    if ($('.form-container').length) {
        $('.form-container select').select2({
            placeholder: "Seleccione una opción",
            allowClear: true,
            width: '100%'
        });
    }

    // Live search functionality
    let debounceTimeout;
    const searchInput = document.getElementById('search-input');
    const tableBody = document.getElementById('grabado-table-body');
    const url = new URL(window.location.href.split('?')[0]); // Get base URL without params

    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            clearTimeout(debounceTimeout);
            const query = this.value;

            debounceTimeout = setTimeout(() => {
                url.searchParams.set('q', query);

                fetch(url.href, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                })
                .then(response => response.text())
                .then(html => {
                    tableBody.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error during fetch:', error);
                });
            }, 300); // 300ms delay
        });
    }
});