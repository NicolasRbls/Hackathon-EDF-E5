import axios from 'axios';

// Create Axios Instance
const api = axios.create({
    baseURL: '/api', // Vite proxy will handle this -> http://localhost:8000
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add Request Interceptor to attach Token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Add Response Interceptor to handle 401 (Auto-Logout)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Token expired or invalid
            // Only redirect if not already on login page to avoid loops
            if (!window.location.pathname.includes('/login')) {
                localStorage.removeItem('token');
                localStorage.removeItem('user_role');
                localStorage.removeItem('username');
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export const authService = {
    async login(username, password) {
        // 1. Get Token
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);

        const response = await api.post('/auth/login', params, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });

        const { access_token } = response.data;

        // 2. Decode Token to get Role (Simple decode, no need for heavy lib if format is known)
        // Or call /users/me to be safe. Let's call /users/me to get clean user object.
        localStorage.setItem('token', access_token);

        const userRes = await api.get('/auth/users/me');
        const user = userRes.data;

        localStorage.setItem('user_role', user.role);
        localStorage.setItem('username', user.username);

        return user;
    },

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user_role');
        localStorage.removeItem('username');
        window.location.href = '/login';
    },

    isAuthenticated() {
        return !!localStorage.getItem('token');
    },

    getUserRole() {
        return localStorage.getItem('user_role');
    }
};

export default api;
