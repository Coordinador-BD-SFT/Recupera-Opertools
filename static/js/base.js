document.addEventListener('DOMContentLoaded', function () {
    // Selecciona todos los toasts en el DOM
    const toastElements = document.querySelectorAll('.toast');

    // Recorre cada toast y lo muestra si está presente
    toastElements.forEach(toastElement => {
        const toast = new bootstrap.Toast(toastElement);
        toast.show(); // Muestra el toast
    });
});
