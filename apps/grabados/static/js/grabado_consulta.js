let sidebarOpen = false;

        function toggleSidebar() {
            const sidebar = document.querySelector('.sidebar');
            const overlay = document.querySelector('.overlay');
            const header = document.querySelector('.header');
            const hamburger = document.querySelector('.hamburger');

            sidebarOpen = !sidebarOpen;

            if (sidebarOpen) {
                sidebar.classList.add('open');
                overlay.classList.add('active');
                header.classList.add('sidebar-open');
                hamburger.classList.add('active');
            } else {
                sidebar.classList.remove('open');
                overlay.classList.remove('active');
                header.classList.remove('sidebar-open');
                hamburger.classList.remove('active');
            }
        }

        function filterTable() {
            const input = document.querySelector('.search-input');
            const filter = input.value.toLowerCase();
            const table = document.getElementById('ofTable');
            const rows = table.getElementsByTagName('tr');

            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                let found = false;
                
                for (let j = 0; j < cells.length - 1; j++) {
                    if (cells[j].textContent.toLowerCase().includes(filter)) {
                        found = true;
                        break;
                    }
                }
                
                rows[i].style.display = found ? '' : 'none';
            }
        }

        function addNewOF() {
            alert('Funcionalidad: Crear Nueva OF\n\nAbrirá formulario para crear una nueva Orden de Fabricación con todos los campos necesarios.');
        }

        function showFilters() {
            populateFilters();
            document.getElementById('filterModal').style.display = 'block';
        }

        function closeModal() {
            document.getElementById('filterModal').style.display = 'none';
        }

        function populateFilters() {
            const table = document.getElementById('ofTable');
            const rows = table.getElementsByTagName('tr');
            const filters = {
                status: new Set(),
                client: new Set(),
                engraving: new Set(),
                machine: new Set()
            };

            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                filters.status.add(cells[7].textContent.trim());
                filters.client.add(cells[3].textContent.trim());
                filters.engraving.add(cells[4].textContent.trim());
                filters.machine.add(cells[6].textContent.trim());
            }

            populateSelect('statusFilter', filters.status);
            populateSelect('clientFilter', filters.client);
            populateSelect('engravingFilter', filters.engraving);
            populateSelect('machineFilter', filters.machine);
        }

        function populateSelect(selectId, options) {
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">Todos</option>';
            options.forEach(option => {
                const opt = document.createElement('option');
                opt.value = option;
                opt.textContent = option;
                select.appendChild(opt);
            });
        }

        function applyFilters() {
            const table = document.getElementById('ofTable');
            const rows = table.getElementsByTagName('tr');
            const statusFilter = document.getElementById('statusFilter').value;
            const clientFilter = document.getElementById('clientFilter').value;
            const engravingFilter = document.getElementById('engravingFilter').value;
            const machineFilter = document.getElementById('machineFilter').value;
            const startDate = document.getElementById('startDate').value;
            const endDate = document.getElementById('endDate').value;

            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                const status = cells[7].textContent.trim();
                const client = cells[3].textContent.trim();
                const engraving = cells[4].textContent.trim();
                const machine = cells[6].textContent.trim();
                const date = cells[8].textContent.trim();

                let display = true;

                if (statusFilter && status !== statusFilter) {
                    display = false;
                }
                if (clientFilter && client !== clientFilter) {
                    display = false;
                }
                if (engravingFilter && engraving !== engravingFilter) {
                    display = false;
                }
                if (machineFilter && machine !== machineFilter) {
                    display = false;
                }
                if (startDate && date < startDate) {
                    display = false;
                }
                if (endDate && date > endDate) {
                    display = false;
                }

                rows[i].style.display = display ? '' : 'none';
            }
            closeModal();
        }

        function clearFilters() {
            document.getElementById('statusFilter').value = '';
            document.getElementById('clientFilter').value = '';
            document.getElementById('engravingFilter').value = '';
            document.getElementById('machineFilter').value = '';
            document.getElementById('startDate').value = '';
            document.getElementById('endDate').value = '';
            applyFilters();
        }

        function exportData() {
            alert('Funcionalidad: Exportar Datos\n\nPermitirá exportar la tabla en formatos:\n- Excel (XLSX)\n- PDF\n- CSV');
        }

        function refreshData() {
            const btn = event.target.closest('.header-btn');
            const icon = btn.querySelector('span:first-child');
            
            icon.style.animation = 'spin 1s linear infinite';
            
            setTimeout(() => {
                icon.style.animation = '';
                alert('Datos actualizados correctamente');
            }, 1000);
        }

        // Event listeners para acciones de la tabla
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn-view')) {
                const row = e.target.closest('tr');
                const ofRef = row.cells[1].textContent.trim();
                alert(`Ver detalles de: ${ofRef}`);
            }
            
            if (e.target.classList.contains('btn-edit')) {
                const row = e.target.closest('tr');
                const ofRef = row.cells[1].textContent.trim();
                alert(`Editar OF: ${ofRef}`);
            }
            
            if (e.target.classList.contains('btn-delete')) {
                const row = e.target.closest('tr');
                const ofRef = row.cells[1].textContent.trim();
                alert(`Eliminar OF: ${ofRef}`);
            }
        });

        // Close modal if user clicks outside of it
        window.onclick = function(event) {
            const modal = document.getElementById('filterModal');
            if (event.target == modal) {
                closeModal();
            }
        }
