// Acciones para formularios: reemplazo de onclick/oninput en línea por listeners externos

document.addEventListener("DOMContentLoaded", () => {
    // vercuentas.html
    const addAccountBtn = document.querySelector(".add-account-btn");
    if (addAccountBtn) {
        addAccountBtn.addEventListener("click", toggleAccountForm);
    }
    const cardInput = document.getElementById("card");
    if (cardInput) {
        cardInput.addEventListener("input", function() { formatCardNumber(this); });
    }

    // veringresos.html y veringresosprogramados.html
    document.querySelectorAll(".add-income-btn").forEach(btn => {
        btn.addEventListener("click", toggleIncomeForm);
    });

    // verservicios.html
    document.querySelectorAll(".add-service-btn").forEach(btn => {
        btn.addEventListener("click", toggleServiceForm);
    });

    // verprestamos.html
    document.querySelectorAll(".add-loan-btn").forEach(btn => {
        btn.addEventListener("click", toggleLoanForm);
    });

    // Confirmar eliminación de cuenta
    document.querySelectorAll("form[data-confirm-eliminar]").forEach(form => {
        form.addEventListener("submit", function(event) {
            const nombreCuenta = this.getAttribute("data-nombre-cuenta") || "la cuenta";
            if (!confirm(`¿Estás seguro de que quieres eliminar la cuenta "${nombreCuenta}"? Esta acción no se puede deshacer.`)) {
                event.preventDefault();
            }
        });
    });
});

// Lógica para mostrar/ocultar formularios
function toggleFormById(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.classList.toggle("d-none");
    }
}

function toggleAccountForm() {
    toggleFormById("accountForm");
}

// Mostrar/ocultar formulario de ingresos
function toggleIncomeForm() {
    toggleFormById("incomeForm");
}

// Mostrar/ocultar formulario de ingresos programados
function toggleScheduledIncomeForm() {
    toggleFormById("income-form-containers");
}

// Mostrar/ocultar formulario de servicios en pagos
function toggleServiceForm() {
    var formContainer = document.getElementById('serviceForm'); // Corregido: coincide con el id en verservicios.html
    if (formContainer) {
        formContainer.classList.toggle('d-none');
    }
}

function toggleLoanForm() {
    toggleFormById("loanForm");
}

// Lógica para formatear el número de tarjeta en tiempo real
function formatCardNumber(input) {
    let value = input.value.replace(/\D/g, "");
    value = value.substring(0, 16); // Máximo 16 dígitos
    let formatted = "";
    for (let i = 0; i < value.length; i += 4) {
        if (i > 0) formatted += " ";
        formatted += value.substring(i, i + 4);
    }
    input.value = formatted;
}

// Confirmar eliminación de servicio (puede usarse en otras vistas)
function confirmarEliminacion(event, nombreServicio) {
    event.preventDefault();
    if (confirm(`¿Estás seguro de que quieres eliminar el servicio "${nombreServicio}"? Esta acción no se puede deshacer.`)) {
        event.target.submit();
    }
}
