window.Login = function ({ onLogin, onRegister }) {
    const container = document.createElement('div');
    container.className = 'dashboard-container animate-fade-in';
    container.style.height = '100vh';
    container.style.display = 'flex';
    container.style.flexDirection = 'column';
    container.style.alignItems = 'center';
    container.style.justifyContent = 'center';
    container.style.padding = '20px';

    const card = document.createElement('div');
    card.className = 'card-glass';
    card.style.maxWidth = '400px';
    card.style.width = '100%';
    card.style.padding = '32px';
    card.style.textAlign = 'center';

    // Title
    const title = document.createElement('h1');
    title.className = 'brand-title';
    title.innerHTML = 'Impulse';
    title.style.fontSize = '2.5rem';
    title.style.marginBottom = '8px';
    card.appendChild(title);

    const subtitle = document.createElement('p');
    subtitle.className = 'brand-motto';
    subtitle.innerHTML = 'Mastery in every pulse.';
    subtitle.style.fontSize = '0.9rem';
    subtitle.style.marginBottom = '24px';
    card.appendChild(subtitle);

    // Form Container
    const formContainer = document.createElement('div');
    card.appendChild(formContainer);

    // Helper: Create Input
    const createInput = (placeholder, type = 'text') => {
        const input = document.createElement('input');
        input.type = type;
        input.placeholder = placeholder;
        input.style.width = '100%';
        input.style.padding = '12px';
        input.style.background = 'rgba(0,0,0,0.2)';
        input.style.border = '1px solid var(--surface-border)';
        input.style.borderRadius = 'var(--border-radius)';
        input.style.color = 'white';
        input.style.fontSize = '1rem';
        input.style.outline = 'none';
        input.style.marginBottom = '12px';
        return input;
    };

    // --- RENDER LOGIN ---
    function renderLogin() {
        formContainer.innerHTML = '';
        
        const userIn = createInput('E-Mail');
        const passIn = createInput('Matriculation Number', 'password');
        const btn = document.createElement('button');
        btn.className = 'btn btn-primary';
        btn.style.width = '100%';
        btn.style.marginTop = '12px';
        btn.textContent = 'LOG IN';

        btn.onclick = () => {
            if (onLogin) onLogin(userIn.value, passIn.value);
        };

        // Enter key support
        passIn.onkeypress = (e) => { if (e.key === 'Enter') btn.click(); };

        formContainer.appendChild(userIn);
        formContainer.appendChild(passIn);
        formContainer.appendChild(btn);
    }

    // Default View
    renderLogin();

    container.appendChild(card);
    return container;
};
