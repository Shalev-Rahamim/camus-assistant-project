// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// API Helper Functions
class API {
    static async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        // Add JWT token to headers if available
        const token = localStorage.getItem('admin_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Server error');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Landing Page
    static async getLandingPage() {
        return this.request('/');
    }

    // Chat
    static async askQuestion(question) {
        return this.request('/ask', {
            method: 'POST',
            body: JSON.stringify({ question }),
        });
    }

    // Tables
    static async getSchedules(limit = 100, offset = 0) {
        return this.request(`/tables/schedules?limit=${limit}&offset=${offset}`);
    }

    static async getKnowledgeBase(category = null, limit = 100, offset = 0) {
        const params = new URLSearchParams({ limit, offset });
        if (category) {
            params.append('category', category);
        }
        return this.request(`/tables/knowledge-base?${params}`);
    }

    // Admin
    static async adminLogin(username, password) {
        return this.request('/admin/login', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        });
    }

    static async getAdminDashboard() {
        return this.request('/admin/dashboard');
    }
}
