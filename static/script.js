// Live Preview
document.getElementById('texto').addEventListener('input', function() {
    document.getElementById('live-preview').innerText = this.value || 'Digite algo para ver a pré-visualização...';
});

// Theme Toggle
const toggle = document.getElementById('theme-toggle');
toggle.addEventListener('click', () => {
    document.documentElement.setAttribute('data-theme', 
        document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light'
    );
    toggle.innerHTML = document.documentElement.getAttribute('data-theme') === 'light' 
        ? '<i class="fas fa-moon"></i>' 
        : '<i class="fas fa-sun"></i>';
});

// Copiar para área de transferência
function copiarTexto() {
    // Implementação do copy
}