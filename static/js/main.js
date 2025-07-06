// Theme Switcher
const themeToggle = document.getElementById('theme-toggle');
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
        localStorage.setItem('theme', 
            document.documentElement.classList.contains('dark') ? 'dark' : 'light'
        );
    });
}

// Form Character Counter
const textarea = document.getElementById('texto');
if (textarea) {
    textarea.addEventListener('input', function() {
        const counter = document.getElementById('char-count');
        if (counter) {
            counter.textContent = this.value.length;
        }
    });
}

// Copy Button
const copyButtons = document.querySelectorAll('[data-copy]');
copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const textToCopy = document.querySelector(btn.dataset.copy).innerText;
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                btn.innerHTML = '<i class="fas fa-check"></i> Copiado!';
                setTimeout(() => {
                    btn.innerHTML = '<i class="fas fa-copy"></i> Copiar';
                }, 2000);
            });
    });
});