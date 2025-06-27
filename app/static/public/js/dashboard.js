// dashboard.js - Lógica de la página de resumen financiero

document.addEventListener("DOMContentLoaded", function() {
    // Obtener datos desde el bloque JSON
    const summary = JSON.parse(document.getElementById('summary-data').textContent);
    const total = summary.total_income + summary.total_services + summary.total_loans;

    // Calcular porcentajes
    function calculatePercentage(value) {
        return total > 0 ? ((value / total) * 100).toFixed(2) + '%' : '0%';
    }

    // Insertar valores en la tabla
    document.getElementById('incomeValue').innerText = `$${summary.total_income.toFixed(2)}`;
    document.getElementById('incomePercentage').innerText = calculatePercentage(summary.total_income);

    document.getElementById('servicesValue').innerText = `$${summary.total_services.toFixed(2)}`;
    document.getElementById('servicesPercentage').innerText = calculatePercentage(summary.total_services);

    document.getElementById('loansValue').innerText = `$${summary.total_loans.toFixed(2)}`;
    document.getElementById('loansPercentage').innerText = calculatePercentage(summary.total_loans);

    // Configurar el gráfico de pie
    var ctx = document.getElementById('financialChart').getContext('2d');
    var financialChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Ingresos', 'Servicios', 'Préstamos'],
            datasets: [{
                label: 'Resumen Financiero',
                data: [
                    summary.total_income,
                    summary.total_services,
                    summary.total_loans
                ],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.6)',  // Ingresos
                    'rgba(255, 99, 132, 0.6)',  // Servicios
                    'rgba(255, 206, 86, 0.6)'   // Préstamos
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            let value = tooltipItem.raw;
                            let percentage = calculatePercentage(value);
                            return `${tooltipItem.label}: $${value.toFixed(2)} (${percentage})`;
                        }
                    }
                }
            }
        }
    });
});
