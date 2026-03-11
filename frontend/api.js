// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Session ID Management
function getOrCreateSessionId() {
    let sessionId = localStorage.getItem('chat_session_id');
    if (!sessionId) {
        // Generate a unique session ID
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('chat_session_id', sessionId);
    }
    return sessionId;
}

// API Helper Functions
class API {
    static async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'X-Session-Id': getOrCreateSessionId(),
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
            
            // Handle 204 No Content responses (like DELETE)
            if (response.status === 204) {
                return null;
            }
            
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

    // Conversations
    static async createConversation(title = null) {
        return this.request('/conversations', {
            method: 'POST',
            body: JSON.stringify({ title }),
        });
    }

    static async listConversations(limit = 50, offset = 0) {
        return this.request(`/conversations?limit=${limit}&offset=${offset}`);
    }

    static async getConversation(conversationId) {
        return this.request(`/conversations/${conversationId}`);
    }

    static async addMessage(conversationId, role, content) {
        return this.request(`/conversations/${conversationId}/messages`, {
            method: 'POST',
            body: JSON.stringify({ role, content }),
        });
    }

    static async deleteConversation(conversationId) {
        return this.request(`/conversations/${conversationId}`, {
            method: 'DELETE',
        });
    }

    static async updateConversationTitle(conversationId, title) {
        return this.request(`/conversations/${conversationId}/title`, {
            method: 'PATCH',
            body: JSON.stringify({ title }),
        });
    }
}
