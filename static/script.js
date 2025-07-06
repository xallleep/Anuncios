// Live Preview
document.getElementById('texto')?.addEventListener('input', function() {
    const preview = document.getElementById('live-preview');
    const charCount = document.getElementById('char-count');
    
    if (preview) {
        preview.innerText = this.value || '✨ Digite acima para ver a pré-visualização... ✨';
    }
    
    if (charCount) {
        charCount.innerText = this.value.length;
    }
});

// Theme Toggle
const toggle = document.getElementById('theme-toggle');
if (toggle) {
    toggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        toggle.innerHTML = newTheme === 'light' 
            ? '<i class="fas fa-moon"></i>' 
            : '<i class="fas fa-sun"></i>';
    });
}

// Check for saved theme preference
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
if (toggle) {
    toggle.innerHTML = savedTheme === 'light' 
        ? '<i class="fas fa-moon"></i>' 
        : '<i class="fas fa-sun"></i>';
}

// Copy functionality
const copyBtn = document.getElementById('copy-btn');
if (copyBtn) {
    copyBtn.addEventListener('click', () => {
        const postContent = document.querySelector('.result-content .post-content').innerText;
        navigator.clipboard.writeText(postContent)
            .then(() => {
                const originalText = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copiado!';
                copyBtn.style.backgroundColor = '#00b894';
                
                setTimeout(() => {
                    copyBtn.innerHTML = originalText;
                    copyBtn.style.backgroundColor = '';
                }, 2000);
            })
            .catch(err => {
                console.error('Failed to copy: ', err);
            });
    });
}

// New post button
const newBtn = document.getElementById('new-btn');
if (newBtn) {
    newBtn.addEventListener('click', () => {
        window.location.href = '/';
    });
}

// Character counter
const textarea = document.getElementById('texto');
if (textarea) {
    textarea.addEventListener('input', function() {
        const charCount = document.getElementById('char-count');
        if (charCount) {
            charCount.innerText = this.value.length;
            
            if (this.value.length > 190) {
                charCount.style.color = '#d63031';
            } else if (this.value.length > 150) {
                charCount.style.color = '#fdcb6e';
            } else {
                charCount.style.color = '';
            }
        }
    });
}