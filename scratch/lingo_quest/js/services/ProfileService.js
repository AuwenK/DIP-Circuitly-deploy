window.ProfileService = {
    STORAGE_KEY: 'circuitly_profiles',
    ACTIVE_KEY: 'circuitly_active_profile',
    profiles: [],
    activeProfileId: null,

    init: function () {
        const stored = localStorage.getItem(this.STORAGE_KEY);
        if (stored) {
            try {
                this.profiles = JSON.parse(stored);
            } catch (e) {
                console.error("Failed to parse profiles", e);
                this.profiles = [];
            }
        }

        const active = localStorage.getItem(this.ACTIVE_KEY);
        if (active) {
            this.activeProfileId = active;
        }
    },

    getProfiles: function () {
        return this.profiles;
    },

    getActiveProfile: function () {
        if (!this.activeProfileId) return null;
        return this.profiles.find(p => p.studentId === this.activeProfileId);
    },

    setActiveProfile: function (studentId) {
        this.activeProfileId = studentId;
        localStorage.setItem(this.ACTIVE_KEY, studentId);
    },

    addProfile: function (profile) {
        // Validation
        if (!profile.name || !profile.studentId || !profile.username || !profile.password) {
            return { success: false, error: "All fields are required (Name, ID, Username, Password)." };
        }

        // Check for duplicate ID
        if (this.profiles.some(p => p.studentId === profile.studentId)) {
            return { success: false, error: "Student ID already exists." };
        }

        // Check for duplicate Username
        if (this.profiles.some(p => p.username === profile.username)) {
            return { success: false, error: "Username already taken." };
        }

        const newProfile = {
            ...profile,
            createdAt: new Date().toISOString(),
            // Default App State
            xp: 0,
            weeklyXP: 0,
            lastResetWeek: this.getCurrentWeekId(),
            hearts: 5,
            topicProgress: {},
            revisionPool: [],
            unfamiliarPool: [],
            stats: {},
            answer_history: [],
            questionMastery: {},
            streakData: { currentStreak: 0, bestStreak: 0 }
        };

        this.profiles.push(newProfile);
        this.save();
        return { success: true };
    },

    authenticate: function (username, password) {
        // Admin Backdoor
        if (username === 'admin' && password === 'admin') {
            return {
                success: true,
                profile: {
                    name: 'Administrator',
                    studentId: 'ADMIN',
                    role: 'admin',
                    xp: 0,
                    hearts: 999
                }
            };
        }

        const profile = this.profiles.find(p => p.username === username && p.password === password);
        if (profile) {
            this.setActiveProfile(profile.studentId);
            return { success: true, profile };
        }
        return { success: false, error: "Invalid username or password." };
    },

    deleteProfile: function (studentId) {
        this.profiles = this.profiles.filter(p => p.studentId !== studentId);
        if (this.activeProfileId === studentId) {
            this.activeProfileId = null;
            localStorage.removeItem(this.ACTIVE_KEY);
        }
        this.save();
    },

    resetProfile: function (studentId) {
        const profile = this.profiles.find(p => p.studentId === studentId);
        if (profile) {
            console.warn(`[ProfileService] DESTRICTIVE RESET triggered for: ${profile.name} (${studentId})`);

            // Learning-related fields
            profile.xp = 0;
            profile.weeklyXP = 0;
            profile.lastResetWeek = this.getCurrentWeekId();
            profile.hearts = 5;
            profile.topicProgress = {};
            profile.revisionPool = [];
            profile.unfamiliarPool = []; // Clear unfamiliar concepts

            // Stats object: holds correct_count, total_attempts, proficiency scores
            profile.stats = {};

            // Per-question mastery
            profile.questionMastery = {};

            // Historical logs
            profile.answer_history = [];

            // Streak data
            profile.streakData = {
                currentStreak: 0,
                bestStreak: 0,
                lastActivityDate: null
            };

            // Sync metadata
            profile.lastActive = new Date().toISOString();
            profile.nextHeartRestoreTime = null;

            console.log(`[ProfileService] SUCCESS: All learning data cleared from database for ${profile.name}.`);
            this.save();
            return { success: true };
        }
        console.error(`[ProfileService] RESET FAILED: Profile ${studentId} not found.`);
        return { success: false, error: "Profile not found" };
    },

    // Generic Progress Update
    updateProgress: function (studentId, data) {
        const profile = this.profiles.find(p => p.studentId === studentId);
        if (profile) {
            this.checkWeeklyReset(profile);
            // Merge data (xp, hearts, topicProgress, nextHeartRestoreTime)
            if (data.xp !== undefined) {
                const diff = data.xp - profile.xp;
                if (diff > 0) profile.weeklyXP = (profile.weeklyXP || 0) + diff;
                profile.xp = data.xp;
            }
            if (data.hearts !== undefined) profile.hearts = data.hearts;
            if (data.topicProgress !== undefined) profile.topicProgress = data.topicProgress;
            if (data.revisionPool !== undefined) profile.revisionPool = data.revisionPool;
            if (data.nextHeartRestoreTime !== undefined) profile.nextHeartRestoreTime = data.nextHeartRestoreTime;

            profile.lastActive = new Date().toISOString();
            this.save();
        }
    },

    updateStats: function (studentId, topicId, correctAdded, totalAdded, xpAdded, timeAdded = 0) {
        const profile = this.profiles.find(p => p.studentId === studentId);
        if (profile) {
            this.checkWeeklyReset(profile);
            if (!profile.stats) profile.stats = {};
            if (!profile.stats[topicId]) profile.stats[topicId] = { xp: 0, time: 0, correct: 0, total: 0, score: 0 };

            // Ensure legacy stats have correct/total if they don't exist
            if (profile.stats[topicId].correct === undefined) profile.stats[topicId].correct = 0;
            if (profile.stats[topicId].total === undefined) profile.stats[topicId].total = 0;

            profile.stats[topicId].xp += xpAdded;
            profile.weeklyXP = (profile.weeklyXP || 0) + xpAdded;
            profile.stats[topicId].correct += correctAdded;
            profile.stats[topicId].total += totalAdded;

            if (timeAdded) {
                profile.stats[topicId].time = (profile.stats[topicId].time || 0) + timeAdded;
            }

            // Record in answer_history
            if (!profile.answer_history) profile.answer_history = [];
            profile.answer_history.push({
                topicId: topicId,
                correct: correctAdded,
                total: totalAdded,
                xp: xpAdded,
                time: timeAdded,
                timestamp: new Date().toISOString()
            });

            // EMA score: weight recent session performance (alpha = 0.3)
            // Naturally forgets old bad runs as performance improves
            if (totalAdded > 0) {
                const alpha = 0.3;
                const sessionAccuracy = correctAdded / totalAdded;
                const oldScore = profile.stats[topicId].score || 0;
                profile.stats[topicId].score = alpha * sessionAccuracy + (1 - alpha) * oldScore;
            }

            // Also update timestamp
            profile.lastActive = new Date().toISOString();
            this.save();
        }
    },

    // Update mastery for a single question
    updateQuestionMastery: function (studentId, questionId, isCorrect) {
        if (!questionId) return;
        const profile = this.profiles.find(p => p.studentId === studentId);
        if (!profile) return;
        if (!profile.questionMastery) profile.questionMastery = {};
        if (!profile.questionMastery[questionId]) {
            profile.questionMastery[questionId] = { correct: 0, total: 0, mastered: false };
        }
        const qm = profile.questionMastery[questionId];
        qm.total++;
        if (isCorrect) qm.correct++;
        // Mastered = correctly answered on 2 or more separate attempts
        qm.mastered = qm.correct >= 2;
        this.save();
    },

    // Get mastery counts for a topic from the questionMastery map
    getTopicMastery: function (profile, topicId) {
        if (!profile || !profile.questionMastery) return { mastered: 0, attempted: 0 };
        const entries = Object.entries(profile.questionMastery).filter(([id]) => {
            return Math.floor(Number(id) / 100) === Number(topicId);
        });
        const attempted = entries.length;
        const mastered = entries.filter(([, v]) => v.mastered).length;
        return { mastered, attempted };
    },

    getCurrentWeekId: function () {
        const d = new Date();
        const year = d.getFullYear();
        const start = new Date(year, 0, 1);
        const days = Math.floor((d - start) / (24 * 60 * 60 * 1000));
        const week = Math.ceil((days + start.getDay() + 1) / 7);
        return `${year}-W${week}`;
    },

    checkWeeklyReset: function (profile) {
        const currentWeek = this.getCurrentWeekId();
        if (profile.lastResetWeek !== currentWeek) {
            profile.weeklyXP = 0;
            profile.lastResetWeek = currentWeek;
            return true;
        }
        return false;
    },

    getLeaderboard: function () {
        // Filter out admins and sorts by weeklyXP
        return this.profiles
            .filter(p => !p.role || p.role !== 'admin')
            .map(p => {
                this.checkWeeklyReset(p);
                return {
                    name: p.name,
                    username: p.username,
                    weeklyXP: p.weeklyXP || 0,
                    xp: p.xp || 0
                };
            })
            .sort((a, b) => b.weeklyXP - a.weeklyXP)
            .slice(0, 10); // Show top 10
    },

    calculateBayesianScore: function (correct, total) {
        const k = 5;
        if (!total || total === 0) return 0;
        return (correct + k) / (total + 2 * k);
    },

    recalculateAllScores: function (studentId) {
        const profile = this.profiles.find(p => p.studentId === studentId);
        if (!profile) return;

        console.log(`[ProfileService] Recalculating scores for: ${profile.name}`);

        // 1. Rebuild stats from history if history exists (Step 218 requirement)
        if (profile.answer_history && profile.answer_history.length > 0) {
            const newStats = {};
            profile.answer_history.forEach(log => {
                const tid = log.topicId;
                if (!newStats[tid]) {
                    newStats[tid] = { xp: 0, time: 0, correct: 0, total: 0, score: 0 };
                    // Preserve existing time if we have it in old stats
                    if (profile.stats && profile.stats[tid] && profile.stats[tid].time) {
                        newStats[tid].time = profile.stats[tid].time;
                    }
                }
                newStats[tid].correct += log.correct;
                newStats[tid].total += log.total;
                newStats[tid].xp += log.xp;
                newStats[tid].time += (log.time || 0);
            });
            profile.stats = newStats;
        }

        // 2. Apply Bayesian smoothing to all categories
        if (profile.stats) {
            Object.keys(profile.stats).forEach(topicId => {
                const stat = profile.stats[topicId];
                if (stat.total !== undefined && stat.correct !== undefined) {
                    stat.score = this.calculateBayesianScore(stat.correct, stat.total);
                }
            });
        }

        this.save();
    },

    timeOffset: 0,
    syncTime: async function () {
        try {
            const start = Date.now();
            // Fallback to a few different time APIs if one fails
            const apis = [
                'https://worldtimeapi.org/api/timezone/Etc/UTC',
                'https://worldtimeapi.org/api/ip'
            ];
            let data;
            for (const api of apis) {
                try {
                    const response = await fetch(api);
                    data = await response.json();
                    if (data && (data.utc_datetime || data.datetime)) break;
                } catch (e) { continue; }
            }

            const serverNow = new Date(data.utc_datetime || data.datetime).getTime();
            const lat = (Date.now() - start) / 2;
            this.timeOffset = serverNow - (Date.now() - lat);
            console.log("Time synced. Offset:", this.timeOffset);
        } catch (e) {
            console.warn("Failed to sync time, using local clock", e);
            this.timeOffset = 0;
        }
    },

    getNow: function () {
        return Date.now() + this.timeOffset;
    },

    getServerTime: async function () {
        if (this.timeOffset === 0) await this.syncTime();
        return this.getNow();
    },

    save: function () {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.profiles));
    },

    exportToExcel: function () {
        if (!window.XLSX) {
            alert("Excel export library (SheetJS) is not loaded.");
            return;
        }

        if (this.profiles.length === 0) {
            alert("No profiles to export.");
            return;
        }

        // 1. Convert data to worksheet
        // Format data for nice columns
        const dataForSheet = this.profiles.map(p => ({
            "Student Name": p.name,
            "Student ID": p.studentId,
            "Class/Group": p.classGroup || "N/A",
            "Date Added": new Date(p.createdAt).toLocaleDateString() + ' ' + new Date(p.createdAt).toLocaleTimeString()
        }));

        const ws = XLSX.utils.json_to_sheet(dataForSheet);

        // 2. Create workbook and add the worksheet
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Profiles");

        // 3. Generate file and trigger download
        const dateStr = new Date().toISOString().slice(0, 10);
        XLSX.writeFile(wb, `PlayerProfiles_${dateStr}.xlsx`);
    }
};

// Auto-init on load
window.ProfileService.init();
