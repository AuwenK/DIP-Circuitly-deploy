window.LeaderboardNameModal = function ({ onSave }) {
    const overlay = document.createElement('div');
    overlay.id = 'leaderboard-modal-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.background = 'rgba(0, 0, 0, 0.85)';
    overlay.style.backdropFilter = 'blur(10px)';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.zIndex = '2000';
    overlay.className = 'animate-fade-in';

    const card = document.createElement('div');
    card.className = 'card-glass';
    card.style.maxWidth = '450px';
    card.style.width = '90%';
    card.style.padding = '40px';
    card.style.textAlign = 'center';
    card.style.borderRadius = '24px';
    card.style.boxShadow = '0 20px 50px rgba(0,0,0,0.5)';

    card.innerHTML = `
        <div style="font-size: 3rem; margin-bottom: 20px;">🏆</div>
        <h2 style="margin-bottom: 12px; color: #fff; font-size: 1.8rem;">Welcome to Impulse!</h2>
        <p style="color: rgba(255,255,255,0.7); margin-bottom: 30px; line-height: 1.6;">
            To track your progress on the global leaderboard, please choose a unique <b>Leaderboard Name</b>. 
            This name will be visible to other students.
        </p>
    `;

    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Enter your leaderboard name...';
    input.style.width = '100%';
    input.style.padding = '14px 20px';
    input.style.background = 'rgba(255,255,255,0.05)';
    input.style.border = '1px solid rgba(255,255,255,0.1)';
    input.style.borderRadius = '12px';
    input.style.color = '#fff';
    input.style.fontSize = '1.1rem';
    input.style.marginBottom = '24px';
    input.style.outline = 'none';
    input.style.transition = 'all 0.3s ease';

    input.onfocus = () => {
        input.style.border = '1px solid var(--primary)';
        input.style.background = 'rgba(255,255,255,0.1)';
    };

    const btn = document.createElement('button');
    btn.className = 'btn btn-primary';
    btn.style.width = '100%';
    btn.style.padding = '14px';
    btn.style.fontSize = '1.1rem';
    btn.style.fontWeight = 'bold';
    btn.textContent = 'START MY JOURNEY';

    const saveName = () => {
        const val = input.value.trim();
        if (val.length < 3) {
            alert("Please enter at least 3 characters.");
            return;
        }
        if (onSave) onSave(val);
        document.body.removeChild(overlay);
    };

    btn.onclick = saveName;
    input.onkeypress = (e) => { if (e.key === 'Enter') saveName(); };

    card.appendChild(input);
    card.appendChild(btn);
    overlay.appendChild(card);

    return overlay;
};
