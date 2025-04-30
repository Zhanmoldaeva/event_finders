document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Загрузка сохраненной темы
    if (localStorage.getItem('theme') === 'dark') {
        body.setAttribute('data-theme', 'dark');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
        body.setAttribute('data-theme', 'light');
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }

    // Обработка клика по переключателю
    themeToggle.addEventListener('click', () => {
        if (body.getAttribute('data-theme') === 'dark') {
            body.setAttribute('data-theme', 'light');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            localStorage.setItem('theme', 'light');
        } else {
            body.setAttribute('data-theme', 'dark');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            localStorage.setItem('theme', 'dark');
        }
    });

    // Обработка уведомлений из Django messages
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        const type = message.classList.contains('alert-success') ? 'success' :
                     message.classList.contains('alert-danger') ? 'error' : 'info';
        showNotification(message.textContent.trim(), type);
        message.remove();
    });
});

// Функция отображения уведомлений
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `${message} <span class="close-btn" style="cursor: pointer; margin-left: 10px;">×</span>`;
    document.body.appendChild(notification);

    notification.querySelector('.close-btn').addEventListener('click', () => {
        notification.remove();
    });

    setTimeout(() => {
        notification.remove();
    }, 3000);
}