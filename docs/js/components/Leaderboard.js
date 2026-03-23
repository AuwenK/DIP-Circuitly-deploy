window.Leaderboard = function ({ onViewPlayerProfile } = {}) {
    const wrapper = document.createElement('div');
    wrapper.style.minHeight = '300px';
    wrapper.innerHTML = '<div style="color:var(--text-muted); text-align:center; padding: 40px; margin-top:40px; background:rgba(15,23,42,0.4); border-radius:12px;">Fetching global leaderboard...</div>';

    setTimeout(async () => {
        if (window.ProfileService && window.ProfileService.getAllProfiles) {
            await window.ProfileService.getAllProfiles();
        }
        let players = window.ProfileService.getLeaderboard();
        const topicLabels = [
            "Fundamentals", "Energy Storage", "Transient/Steady",
            "Op-Amps", "Laplace", "Network Func",
            "DC vs AC", "3-Phase"
        ];

        const container = document.createElement('div');
        container.className = 'leaderboard-container animate-fade-in';
        container.style.paddingTop = '160px';
        container.style.paddingLeft = '24px';
        container.style.paddingRight = '24px';
        container.style.paddingBottom = '40px';
        container.style.maxWidth = '1200px';
        container.style.margin = '0 auto';
        container.style.width = '100%';
        container.style.boxSizing = 'border-box';

    const title = document.createElement('div');
    title.style.display = 'flex';
    title.style.justifyContent = 'space-between';
    title.style.alignItems = 'center';
    title.style.marginBottom = '40px';

    const titleText = document.createElement('h2');
    titleText.className = 'text-gradient';
    titleText.textContent = 'Leaderboard';
    titleText.style.fontSize = '2rem';
    titleText.style.fontWeight = '800';
    title.appendChild(titleText);

    const periodTabsHeader = document.createElement('div');
    periodTabsHeader.style.cssText = 'display:flex; gap:6px; flex-wrap:wrap; justify-content:flex-end;';
    title.appendChild(periodTabsHeader);

    container.appendChild(title);

    // Build period tabs in the header (once, outside renderLeaderboard)
    const periods = [
        { key: 'daily', label: '📅 Daily' },
        { key: 'weekly', label: '📊 Weekly' },
        { key: 'alltime', label: '⏰ All Time' }
    ];

    function buildHeaderPeriodTabs() {
        periodTabsHeader.innerHTML = '';
        periods.forEach(p => {
            const tab = document.createElement('button');
            const isActive = p.key === selectedPeriod;
            tab.textContent = p.label;
            tab.style.cssText = `
                padding:6px 14px;
                border-radius:50px;
                border:1px solid ${isActive ? '#34d399' : 'var(--surface-border)'};
                background:${isActive ? 'rgba(52, 211, 153, 0.15)' : 'rgba(255,255,255,0.05)'};
                color:${isActive ? '#34d399' : 'var(--text-muted)'};
                cursor:pointer;
                font-size:0.8rem;
                font-weight:500;
                transition:all 0.2s ease;
            `;
            tab.onmouseenter = () => {
                if (!isActive) tab.style.borderColor = '#9ca3af';
            };
            tab.onmouseleave = () => {
                if (!isActive) tab.style.borderColor = 'var(--surface-border)';
            };
            tab.onclick = () => {
                selectedPeriod = p.key;
                buildHeaderPeriodTabs();
                renderLeaderboard();
            };
            periodTabsHeader.appendChild(tab);
        });
    }

    if (players.length === 0) {
        const empty = document.createElement('p');
        empty.textContent = 'Competing starts soon! Be the first on the leaderboard.';
        empty.style.textAlign = 'center';
        empty.style.color = 'var(--text-muted)';
        empty.style.padding = '40px';
        container.appendChild(empty);
        return container;
    }

    // --- STATE ---
    let selectedCategory = 'overall';
    let selectedTopic = null;
    let selectedPeriod = 'alltime'; // 'daily', 'weekly', 'alltime'
    let searchQuery = '';

    // --- TIME PERIOD HELPER ---
    function getTimePeriodMs(period) {
        const now = Date.now();
        switch(period) {
            case 'daily': return now - (24 * 60 * 60 * 1000);
            case 'weekly': return now - (7 * 24 * 60 * 60 * 1000);
            case 'alltime': return 0;
            default: return 0;
        }
    }

    // --- CALCULATE SCORE FOR TIME PERIOD ---
    function getScoreForPeriod(player, category, topicId, period) {
        const cutoffTime = getTimePeriodMs(period);
        
        // Filter history by time period
        const relevantAttempts = (player.answer_history || []).filter(attempt => 
            cutoffTime === 0 || (new Date(attempt.timestamp).getTime() > cutoffTime)
        );

        if (relevantAttempts.length === 0) {
            if (category === 'overall' || category === 'xp') {
                if (cutoffTime === 0 && player.xp) return player.xp;
                if (player.xp > 0 && (!player.answer_history || player.answer_history.length === 0)) return player.xp;
            }
            return 0;
        }

        // Calculate xp, accuracy, or speed based on category
        switch(category) {
            case 'overall':
            case 'xp': {
                let xpScore = relevantAttempts.reduce((sum, a) => sum + (a.xp || 0), 0);
                if (cutoffTime === 0 && player.xp) {
                    xpScore = Math.max(xpScore, player.xp);
                } else if (xpScore === 0 && player.xp > 0 && (!player.answer_history || player.answer_history.length === 0)) {
                    xpScore = player.xp;
                }
                return xpScore;
            }
            
            case 'accuracy': {
                const totalCorrect = relevantAttempts.reduce((sum, a) => sum + (a.correct || 0), 0);
                const totalAttempts = relevantAttempts.reduce((sum, a) => sum + (a.total || 0), 0);
                return totalAttempts > 0 ? (totalCorrect / totalAttempts) * 100 : 0;
            }
            
            case 'time': {
                const totalCorrect = relevantAttempts.reduce((sum, a) => sum + (a.correct || 0), 0);
                const totalTime = relevantAttempts.reduce((sum, a) => sum + (a.time || 0), 0);
                return totalCorrect > 0 ? (totalCorrect / Math.max(totalTime / 60, 1)) : 0;
            }
            
            default: return 0;
        }
    }

    // --- CATEGORY DEFINITIONS ---
    const categories = {
        overall: { name: 'Overall', sortFn: (p) => (p.stats ? Object.values(p.stats).reduce((s, t) => s + (t.xp || 0), 0) : 0) },
        xp: { name: 'Highest XP', sortFn: (p) => (p.stats ? Object.values(p.stats).reduce((s, t) => s + (t.xp || 0), 0) : 0) },
        accuracy: { name: 'Highest Accuracy', sortFn: (p) => {
            if (!p.stats) return 0;
            const stats = Object.values(p.stats);
            if (stats.length === 0) return 0;
            const totalCorrect = stats.reduce((s, t) => s + (t.correct || 0), 0);
            const totalAttempts = stats.reduce((s, t) => s + (t.total || 0), 0);
            return totalAttempts > 0 ? (totalCorrect / totalAttempts) * 100 : 0;
        }},
        time: { name: 'Speed Champion', sortFn: (p) => {
            if (!p.stats) return 0;
            const stats = Object.values(p.stats);
            if (stats.length === 0) return 0;
            const totalCorrect = stats.reduce((s, t) => s + (t.correct || 0), 0);
            const totalTime = stats.reduce((s, t) => s + (t.time || 0), 0);
            return totalCorrect > 0 ? (totalCorrect / Math.max(totalTime / 60, 1)) : 0;
        }}
    };

    // Helper function to get ranking value
    function getRankingValue(player, category, topicId, period) {
        if (topicId) {
            // Topic-specific ranking uses history filtering
            const cutoffTime = getTimePeriodMs(period);
            const relevantAttempts = (player.answer_history || []).filter(attempt => 
                (cutoffTime === 0 || (new Date(attempt.timestamp).getTime() > cutoffTime)) &&
                attempt.topicId === topicId
            );

            if (relevantAttempts.length === 0) {
                if (category === 'xp' || category === 'overall') {
                    if (cutoffTime === 0 && player.topicProgress && player.topicProgress[topicId]) return player.topicProgress[topicId].xp || 0;
                    if (player.topicProgress && player.topicProgress[topicId] && player.topicProgress[topicId].xp > 0 && (!player.answer_history || player.answer_history.length === 0)) return player.topicProgress[topicId].xp || 0;
                }
                return 0;
            }

            switch(category) {
                case 'xp': 
                case 'overall': {
                    let xpScore = relevantAttempts.reduce((sum, a) => sum + (a.xp || 0), 0);
                    if (cutoffTime === 0 && player.topicProgress && player.topicProgress[topicId]) {
                        xpScore = Math.max(xpScore, player.topicProgress[topicId].xp || 0);
                    } else if (xpScore === 0 && player.topicProgress && player.topicProgress[topicId] && player.topicProgress[topicId].xp > 0 && (!player.answer_history || player.answer_history.length === 0)) {
                        xpScore = player.topicProgress[topicId].xp || 0;
                    }
                    return xpScore;
                }
                case 'accuracy': {
                    const totalCorrect = relevantAttempts.reduce((s, a) => s + (a.correct || 0), 0);
                    const totalAttempts = relevantAttempts.reduce((s, a) => s + (a.total || 0), 0);
                    return totalAttempts > 0 ? ((totalCorrect / totalAttempts) * 100) : 0;
                }
                case 'time': {
                    const totalCorrect = relevantAttempts.reduce((s, a) => s + (a.correct || 0), 0);
                    const totalTime = relevantAttempts.reduce((s, a) => s + (a.time || 0), 0);
                    return totalCorrect > 0 ? (totalCorrect / Math.max(totalTime / 60, 1)) : 0;
                }
                default: {
                    let xpScore = relevantAttempts.reduce((sum, a) => sum + (a.xp || 0), 0);
                    if (cutoffTime === 0 && player.topicProgress && player.topicProgress[topicId]) {
                        xpScore = Math.max(xpScore, player.topicProgress[topicId].xp || 0);
                    } else if (xpScore === 0 && player.topicProgress && player.topicProgress[topicId] && player.topicProgress[topicId].xp > 0 && (!player.answer_history || player.answer_history.length === 0)) {
                        xpScore = player.topicProgress[topicId].xp || 0;
                    }
                    return xpScore;
                }
            }
        } else {
            return getScoreForPeriod(player, category, null, period);
        }
    }

    // Helper function to render leaderboard for current category/topic
    function renderLeaderboard() {
        // Clear previous content (keep title)
        while (container.children.length > 1) {
            container.removeChild(container.lastChild);
        }

        // Add controls
        const controls = document.createElement('div');
        controls.style.cssText = 'margin-bottom:30px; display:flex; gap:20px; align-items:center; flex-wrap:wrap;';

        // Category tabs
        const tabsContainer = document.createElement('div');
        tabsContainer.style.cssText = 'display:flex; gap:8px; flex-wrap:wrap;';

        Object.keys(categories).forEach(catKey => {
            const tab = document.createElement('button');
            const isActive = catKey === selectedCategory;
            tab.textContent = categories[catKey].name;
            tab.style.cssText = `
                padding:8px 16px;
                border-radius:8px;
                border:1px solid ${isActive ? '#60a5fa' : '#374151'};
                background:${isActive ? 'rgba(96, 165, 250, 0.2)' : 'transparent'};
                color:${isActive ? '#60a5fa' : '#9ca3af'};
                cursor:pointer;
                font-size:0.85rem;
                font-weight:500;
                transition:all 0.3s ease;
            `;
            tab.onmouseenter = () => {
                if (!isActive) tab.style.borderColor = '#9ca3af';
            };
            tab.onmouseleave = () => {
                if (!isActive) tab.style.borderColor = '#374151';
            };
            tab.onclick = () => {
                selectedCategory = catKey;
                selectedTopic = null; // Reset topic when changing category
                renderLeaderboard();
            };
            tabsContainer.appendChild(tab);
        });

        controls.appendChild(tabsContainer);

        // Topic filter
        const topicLabel = document.createElement('label');
        topicLabel.style.cssText = 'color:#9ca3af; font-size:0.85rem; font-weight:500;';
        topicLabel.textContent = 'Topic:';

        const topicSelect = document.createElement('select');
        topicSelect.style.cssText = `
            padding:6px 12px;
            border-radius:6px;
            border:1px solid #374151;
            background:#1f2937;
            color:#e5e7eb;
            font-size:0.85rem;
            cursor:pointer;
            transition:all 0.3s ease;
        `;

        const optionAll = document.createElement('option');
        optionAll.value = 'all';
        optionAll.textContent = 'Overall';
        topicSelect.appendChild(optionAll);

        topicLabels.forEach((label, idx) => {
            const option = document.createElement('option');
            option.value = idx + 1;
            option.textContent = label;
            topicSelect.appendChild(option);
        });

        topicSelect.value = selectedTopic ? selectedTopic : 'all';
        topicSelect.onchange = (e) => {
            selectedTopic = e.target.value === 'all' ? null : parseInt(e.target.value);
            renderLeaderboard();
        };

        controls.appendChild(topicLabel);
        controls.appendChild(topicSelect);

        // Search Input wrapper for icon
        const searchWrapper = document.createElement('div');
        searchWrapper.style.cssText = 'position:relative; margin-left:auto; z-index: 10;';

        const searchIcon = document.createElement('div');
        searchIcon.textContent = '🔍';
        searchIcon.style.cssText = 'position:absolute; left:14px; top:50%; transform:translateY(-50%); opacity:0.6; pointer-events:none;';
        
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search username...';
        searchInput.value = searchQuery;
        searchInput.className = 'leaderboard-search';
        searchInput.style.cssText = `
            padding: 10px 18px 10px 40px;
            border-radius: 50px;
            border: 1px solid rgba(255,255,255,0.15);
            background: rgba(15,23,42,0.6);
            color: #fff;
            font-size: 0.95rem;
            width: 250px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            outline: none;
        `;
        searchInput.onfocus = () => {
             searchInput.style.borderColor = '#60a5fa';
             searchInput.style.boxShadow = '0 0 20px rgba(96, 165, 250, 0.4)';
             searchInput.style.transform = 'translateY(-2px)';
        };
        searchInput.onblur = () => {
             searchInput.style.borderColor = 'rgba(255,255,255,0.15)';
             searchInput.style.boxShadow = '0 4px 15px rgba(0,0,0,0.2)';
             searchInput.style.transform = 'none';
        };
        searchInput.oninput = (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            renderLeaderboard();
        };

        searchWrapper.appendChild(searchIcon);
        searchWrapper.appendChild(searchInput);
        controls.appendChild(searchWrapper);

        container.appendChild(controls);

        // Scrollable wrapper (acting as the Leaderboard Card)
        const listWrapper = document.createElement('div');
        listWrapper.className = 'card-glass';
        listWrapper.style.cssText = 'max-height: 550px; overflow-y: auto; padding: 24px; background: rgba(15, 23, 42, 0.4); margin-top: 10px; border-radius: 12px;';

        // Sort players by current category
        const allSortedPlayers = [...players].sort((a, b) => 
            getRankingValue(b, selectedCategory, selectedTopic, selectedPeriod) - getRankingValue(a, selectedCategory, selectedTopic, selectedPeriod)
        );
        const activePlayers = allSortedPlayers.filter(p => getRankingValue(p, selectedCategory, selectedTopic, selectedPeriod) > 0);

        let displayPlayers = activePlayers;
        let bottomPlayers = [];

        if (!searchQuery && activePlayers.length > 1) {
            // Guarantee top 1 is safe in small environments. Take up to the bottom 5 players for the "Needs XP" section.
            const bottomCount = Math.min(5, activePlayers.length - 1);
            bottomPlayers = activePlayers.slice(-bottomCount);
            displayPlayers = activePlayers.filter(p => !bottomPlayers.includes(p));
        }

        if (searchQuery) {
            displayPlayers = displayPlayers.filter(p => p.name && p.name.toLowerCase().includes(searchQuery));
        } else {
            displayPlayers = displayPlayers.slice(0, 50); // Top 50 if no search
        }

        // Tier definitions
        const tiers = [
            { name: 'Legendary Circuit Masters', range: [1, 5], icon: '⚡', color: '#fbbf24', bgColor: 'rgba(251, 191, 36, 0.1)', borderColor: 'rgba(251, 191, 36, 0.3)' },
            { name: 'Rising Voltage Experts', range: [6, 10], icon: '🔮', color: '#a78bfa', bgColor: 'rgba(167, 139, 250, 0.1)', borderColor: 'rgba(167, 139, 250, 0.3)' },
            { name: 'Ascending Engineers', range: [11, 20], icon: '🚀', color: '#34d399', bgColor: 'rgba(52, 211, 153, 0.1)', borderColor: 'rgba(52, 211, 153, 0.3)' },
            { name: 'Voltage Seekers', range: [21, 50], icon: '⚙️', color: '#60a5fa', bgColor: 'rgba(96, 165, 250, 0.1)', borderColor: 'rgba(96, 165, 250, 0.3)' }
        ];

        // Render tiers
        tiers.forEach(tier => {
            const tieredPlayers = displayPlayers.filter((_, idx) => idx >= tier.range[0] - 1 && idx < tier.range[1]);
            if (tieredPlayers.length === 0) return;

            // Tier Header
            const tierHeader = document.createElement('div');
            tierHeader.style.display = 'flex';
            tierHeader.style.alignItems = 'center';
            tierHeader.style.marginTop = '32px';
            tierHeader.style.marginBottom = '16px';
            tierHeader.style.paddingBottom = '12px';
            tierHeader.style.borderBottom = `2px solid ${tier.color}`;

            const tierIcon = document.createElement('span');
            tierIcon.style.fontSize = '1.5rem';
            tierIcon.style.marginRight = '10px';
            tierIcon.textContent = tier.icon;
            tierHeader.appendChild(tierIcon);

            const tierName = document.createElement('h3');
            tierName.style.fontSize = '1.2rem';
            tierName.style.fontWeight = '700';
            tierName.style.color = tier.color;
            tierName.textContent = tier.name;
            tierHeader.appendChild(tierName);

            const tierRange = document.createElement('span');
            tierRange.style.marginLeft = 'auto';
            tierRange.style.fontSize = '0.8rem';
            tierRange.style.color = 'var(--text-muted)';
            tierRange.style.background = tier.bgColor;
            tierRange.style.border = `1px solid ${tier.borderColor}`;
            tierRange.style.padding = '4px 12px';
            tierRange.style.borderRadius = '50px';
            tierRange.textContent = `#${tier.range[0]} - #${tier.range[1]}`;
            tierHeader.appendChild(tierRange);

            listWrapper.appendChild(tierHeader);

            // Tier Players
            const tierContainer = document.createElement('div');
            tierContainer.style.display = 'flex';
            tierContainer.style.flexDirection = 'column';
            tierContainer.style.gap = '8px';
            tierContainer.style.marginBottom = '24px';

            tieredPlayers.forEach((player, idx) => {
                const actualRank = tier.range[0] + idx;
                const row = document.createElement('div');
                row.style.display = 'flex';
                row.style.alignItems = 'center';
                row.style.padding = '14px 18px';
                row.style.background = tier.bgColor;
                row.style.border = `1px solid ${tier.borderColor}`;
                row.style.borderRadius = '10px';
                row.style.transition = 'all 0.3s ease';
                row.style.cursor = 'pointer';
                
                row.onmouseenter = () => {
                    row.style.background = tier.bgColor.replace(/0.\d/, '0.2');
                    row.style.transform = 'translateX(4px)';
                };
                row.onmouseleave = () => {
                    row.style.background = tier.bgColor;
                    row.style.transform = 'translateX(0)';
                };

                // Click to view profile
                row.onclick = () => {
                    if (onViewPlayerProfile) {
                        onViewPlayerProfile(player);
                    }
                };

                // Rank Badge
                const rankBadge = document.createElement('div');
                rankBadge.style.display = 'flex';
                rankBadge.style.alignItems = 'center';
                rankBadge.style.justifyContent = 'center';
                rankBadge.style.width = '36px';
                rankBadge.style.height = '36px';
                rankBadge.style.borderRadius = '8px';
                rankBadge.style.background = tier.color;
                rankBadge.style.color = '#0f172a';
                rankBadge.style.fontWeight = '900';
                rankBadge.style.fontSize = '0.9rem';
                rankBadge.style.flexShrink = '0';
                rankBadge.textContent = `#${actualRank}`;
                row.appendChild(rankBadge);

                // Player Name
                const name = document.createElement('div');
                name.textContent = player.name;
                name.style.flex = '1';
                name.style.fontWeight = '600';
                name.style.marginLeft = '14px';
                name.style.overflow = 'hidden';
                name.style.textOverflow = 'ellipsis';
                name.style.whiteSpace = 'nowrap';
                row.appendChild(name);

                // Score (varies by category)
                const scoreValue = getRankingValue(player, selectedCategory, selectedTopic);
                const scoreText = selectedCategory === 'accuracy' ? `${scoreValue.toFixed(1)}%` :
                                selectedCategory === 'time' ? `${scoreValue.toFixed(1)} q/min` :
                                `⚡ ${Math.round(scoreValue)}`;

                const score = document.createElement('div');
                score.textContent = scoreText;
                score.style.fontWeight = '700';
                score.style.fontSize = '0.95rem';
                score.style.marginRight = '10px';
                score.style.color = tier.color;
                row.appendChild(score);

                // View Icon
                const viewIcon = document.createElement('div');
                viewIcon.textContent = '→';
                viewIcon.style.color = tier.color;
                viewIcon.style.fontSize = '1.2rem';
                viewIcon.style.opacity = '0.6';
                viewIcon.style.transition = 'opacity 0.3s ease';
                row.appendChild(viewIcon);

                row.onmouseenter = () => {
                    row.style.background = tier.bgColor.replace(/0.\d/, '0.2');
                    row.style.transform = 'translateX(4px)';
                    viewIcon.style.opacity = '1';
                };
                row.onmouseleave = () => {
                    row.style.background = tier.bgColor;
                    row.style.transform = 'translateX(0)';
                    viewIcon.style.opacity = '0.6';
                };

                tierContainer.appendChild(row);
            });

            listWrapper.appendChild(tierContainer);
        });

        // Recharging Zone (Lowest XP logic)
        if (bottomPlayers.length > 0) {
            const bottomHeader = document.createElement('div');
            bottomHeader.style.display = 'flex';
            bottomHeader.style.alignItems = 'center';
            bottomHeader.style.marginTop = '48px';
            bottomHeader.style.marginBottom = '16px';
            bottomHeader.style.paddingBottom = '12px';
            bottomHeader.style.borderBottom = `2px solid rgba(239, 68, 68, 0.5)`;

            bottomHeader.innerHTML = `
                <span style="font-size: 1.5rem; margin-right: 10px;">🔌</span>
                <h3 style="font-size: 1.2rem; font-weight: 700; color: #fca5a5;">Time to Recharge (Lowest XP)</h3>
                <span style="margin-left: auto; font-size: 0.8rem; color: var(--text-muted); background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); padding: 4px 12px; border-radius: 50px;">Keep pushing! You got this!</span>
            `;
            listWrapper.appendChild(bottomHeader);

            const bottomContainer = document.createElement('div');
            bottomContainer.style.display = 'flex';
            bottomContainer.style.flexDirection = 'column';
            bottomContainer.style.gap = '8px';
            bottomContainer.style.marginBottom = '24px';

            const startIndex = activePlayers.length - bottomPlayers.length;

            bottomPlayers.forEach((player, idx) => {
                const actualRank = startIndex + idx + 1;
                const row = document.createElement('div');
                row.style.display = 'flex';
                row.style.alignItems = 'center';
                row.style.padding = '14px 18px';
                row.style.background = 'rgba(239, 68, 68, 0.05)';
                row.style.border = `1px solid rgba(239, 68, 68, 0.2)`;
                row.style.borderRadius = '10px';
                row.style.transition = 'all 0.3s ease';
                row.style.cursor = 'pointer';

                row.onmouseenter = () => {
                    row.style.background = 'rgba(239, 68, 68, 0.1)';
                    row.style.transform = 'translateX(4px)';
                };
                row.onmouseleave = () => {
                    row.style.background = 'rgba(239, 68, 68, 0.05)';
                    row.style.transform = 'translateX(0)';
                };

                    row.onclick = () => {
                        if (onViewPlayerProfile) onViewPlayerProfile(player);
                    };

                    // Rank Badge
                    const rankBadge = document.createElement('div');
                    rankBadge.style.display = 'flex';
                    rankBadge.style.alignItems = 'center';
                    rankBadge.style.justifyContent = 'center';
                    rankBadge.style.width = '36px';
                    rankBadge.style.height = '36px';
                    rankBadge.style.borderRadius = '8px';
                    rankBadge.style.background = 'rgba(239, 68, 68, 0.15)';
                    rankBadge.style.color = '#fca5a5';
                    rankBadge.style.fontWeight = '900';
                    rankBadge.style.fontSize = '0.9rem';
                    rankBadge.style.flexShrink = '0';
                    rankBadge.style.border = '1px solid rgba(239, 68, 68, 0.3)';
                    rankBadge.textContent = `#${actualRank}`;
                    row.appendChild(rankBadge);

                    // Player Name
                    const name = document.createElement('div');
                    name.textContent = player.name;
                    name.style.flex = '1';
                    name.style.fontWeight = '600';
                    name.style.marginLeft = '14px';
                    name.style.overflow = 'hidden';
                    name.style.textOverflow = 'ellipsis';
                    name.style.whiteSpace = 'nowrap';
                    row.appendChild(name);

                    // Score
                    const scoreValue = getRankingValue(player, selectedCategory, selectedTopic);
                    const scoreText = selectedCategory === 'accuracy' ? `${scoreValue.toFixed(1)}%` :
                                    selectedCategory === 'time' ? `${scoreValue.toFixed(1)} q/min` :
                                    `⚡ ${Math.round(scoreValue)}`;

                    const score = document.createElement('div');
                    score.textContent = scoreText;
                    score.style.fontWeight = '700';
                    score.style.fontSize = '0.95rem';
                    score.style.marginRight = '10px';
                    score.style.color = '#fca5a5';
                    row.appendChild(score);

                    const rightArrow = document.createElement('div');
                    rightArrow.textContent = '→';
                    rightArrow.style.color = 'var(--text-muted)';
                    rightArrow.style.fontSize = '1.2rem';
                    rightArrow.style.marginLeft = '4px';
                    row.appendChild(rightArrow);

                    bottomContainer.appendChild(row);
                });

                listWrapper.appendChild(bottomContainer);
        }

        container.appendChild(listWrapper);

        // Restore focus if searching
        if (searchQuery) {
            setTimeout(() => {
                const searchBox = container.querySelector('.leaderboard-search');
                if (searchBox) {
                    searchBox.focus();
                    const val = searchBox.value;
                    searchBox.value = '';
                    searchBox.value = val;
                }
            }, 0);
        }
    }

    // Initial render
    buildHeaderPeriodTabs();
    renderLeaderboard();

    wrapper.innerHTML = '';
    wrapper.appendChild(container);

    // Auto-refresh leaderboard silently every 30 seconds
    const lbTimer = setInterval(async () => {
        if (!document.body.contains(wrapper)) {
            clearInterval(lbTimer);
            return;
        }
        if (window.ProfileService && window.ProfileService.getAllProfiles) {
            await window.ProfileService.getAllProfiles();
            players = window.ProfileService.getLeaderboard();
            renderLeaderboard();
        }
    }, 30000);
    }, 0);

    return wrapper;
};
