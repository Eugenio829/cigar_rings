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

function addNewOF() {
    console.log("Función addNewOF() llamada.");
    alert("Abriendo formulario para nueva OF...");
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

// Cerrar el modal si se hace clic fuera de él
window.onclick = function(event) {
    const modal = document.getElementById('filterModal');
    if (event.target == modal) {
        closeModal();
    }
}

$(document).ready(function() {
    // Initialize Select2 on the "Tipo de Grabado" dropdown
    $('#id_tipo_grabado').select2({
        placeholder: "Seleccione o busque un tipo",
        allowClear: true,
        width: '100%',
        dropdownParent: $('#filterModal .modal-content') // Attach dropdown to the modal
    });

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