document.addEventListener('DOMContentLoaded', () => {
    const openBtn = document.getElementById('open-btn');
    const closeBtn = document.getElementById('close-btn');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');

    if (!openBtn || !closeBtn || !sidebar || !mainContent) {
        console.error('Uno o más elementos no se encontraron en el DOM.');
        return;
    }

    openBtn.addEventListener('click', () => {
        sidebar.classList.add('active');
        mainContent.classList.add('shift');
        openBtn.style.display = 'none'; // Hide open button when sidebar is active
    });

    closeBtn.addEventListener('click', () => {
        sidebar.classList.remove('active');
        mainContent.classList.remove('shift');
        openBtn.style.display = 'block'; // Show open button when sidebar is hidden
    });
});
