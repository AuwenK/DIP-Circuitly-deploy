const API_BASE = 'http://localhost:3000/api';
const SESSION_KEY = 'circuitly_session_user';

window.AuthService = {
    getCurrentUser: () => {
        const json = localStorage.getItem(SESSION_KEY);
        return json ? JSON.parse(json) : null;
    },

    login: async (username, password) => {
        try {
            const response = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (data.success) {
                localStorage.setItem(SESSION_KEY, JSON.stringify(data.user));
                return { success: true, user: data.user };
            }

            return { success: false, error: data.error || 'Login failed' };
        } catch (err) {
            console.error(err);
            return { success: false, error: 'Server connection failed' };
        }
    },

    register: async (username, password, studentId, name, classGroup) => {
        try {
            const response = await fetch(`${API_BASE}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username,
                    password,
                    studentId,
                    name,
                    classGroup
                })
            });

            const data = await response.json();

            if (data.success) {
                localStorage.setItem(SESSION_KEY, JSON.stringify(data.user));
                return { success: true, user: data.user };
            }

            return { success: false, error: data.error || 'Registration failed' };
        } catch (err) {
            console.error(err);
            return { success: false, error: 'Server connection failed' };
        }
    },

    logout: async () => {
        localStorage.removeItem(SESSION_KEY);
        return { success: true };
    },

    saveProgress: async (userData) => {
        const currentUser = window.AuthService.getCurrentUser();
        if (!currentUser || !currentUser.id) return;

        try {
            await fetch(`${API_BASE}/profile/progress`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    userId: currentUser.id,
                    xp: userData.xp,
                    hearts: userData.hearts,
                    topicProgress: userData.topicProgress || {}
                })
            });

            const updatedSessionUser = {
                ...currentUser,
                xp: userData.xp,
                hearts: userData.hearts,
                topicProgress: userData.topicProgress || {}
            };

            localStorage.setItem(SESSION_KEY, JSON.stringify(updatedSessionUser));
        } catch (err) {
            console.error('Failed to save progress:', err);
        }
    }
};