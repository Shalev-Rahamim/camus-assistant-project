// App Initialization
let currentUser = null;

// Navigation Component
function renderNavbar() {
    const navbar = document.getElementById('navbar');
    const token = localStorage.getItem('admin_token');
    
    navbar.innerHTML = `
        <div class="navbar-content">
            <a href="/" class="logo" onclick="router.navigate('/'); return false;">Campus Elad Software</a>
            <ul class="nav-links">
                <li><a href="/" onclick="router.navigate('/'); return false;">Home</a></li>
                <li><a href="/chat" onclick="router.navigate('/chat'); return false;">AI Chat</a></li>
                <li><a href="/tables" onclick="router.navigate('/tables'); return false;">Tables</a></li>
                ${token 
                    ? `<li><a href="/admin/dashboard" onclick="router.navigate('/admin/dashboard'); return false;">Admin</a></li>
                       <li><a href="#" onclick="handleLogout(); return false;">Logout</a></li>`
                    : `<li><a href="/admin/login" onclick="router.navigate('/admin/login'); return false;">Admin Login</a></li>`
                }
            </ul>
        </div>
    `;
}

function handleLogout() {
    localStorage.removeItem('admin_token');
    router.navigate('/');
}

// Landing Page
async function renderLandingPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = '<div class="loading"><div class="spinner"></div>Loading...</div>';

    try {
        const data = await API.getLandingPage();
        
        // Map API routes to frontend routes
        const routeMap = {
            '/api/v1/ask': '/chat',
            '/api/v1/tables': '/tables',
            '/api/v1/admin/login': '/admin/login'
        };
        
        mainContent.innerHTML = `
            <div class="landing-container">
                <h1 class="landing-title">${data.title}</h1>
                <p class="landing-subtitle">${data.description}</p>
                
                <div class="options-grid">
                    ${data.options.map(option => {
                        const frontendRoute = routeMap[option.route] || option.route;
                        return `
                        <a href="${frontendRoute}" class="option-card" onclick="router.navigate('${frontendRoute}'); return false;">
                            <div class="option-icon">${getIcon(option.id)}</div>
                            <h2 class="option-title">${option.title}</h2>
                            <p class="option-description">${option.description}</p>
                        </a>
                    `;
                    }).join('')}
                </div>
                
                <div class="logo-container">
                    <img src="static/Elad-logo-color.png" alt="ELAD Logo" class="elad-logo">
                </div>
            </div>
        `;
    } catch (error) {
        mainContent.innerHTML = `
            <div class="alert alert-error">
                Error loading page: ${error.message}
            </div>
        `;
    }
}

function getIcon(id) {
    const icons = {
        'chat': '💬',
        'tables': '📊',
        'admin': '🔐'
    };
    return icons[id] || '📄';
}

// Chat Page
let chatMessages = [];
let welcomeMessageShown = false;

function renderChatPage() {
    const mainContent = document.getElementById('main-content');
    
    // Show welcome message only once when chat page is first loaded
    if (!welcomeMessageShown && chatMessages.length === 0) {
        chatMessages.push({
            type: 'ai',
            text: 'Hi! I\'m the AI Chat Assistant. I\'m here to help answer questions related to the campus, schedules, exams, and more. How can I assist you today?'
        });
        welcomeMessageShown = true;
    }
    
    mainContent.innerHTML = `
        <div class="chat-container">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">AI Chat</h2>
                    <p class="card-description">Ask questions about campus, schedules, exams, and more</p>
                </div>
                
                <div class="chat-messages" id="chat-messages">
                    ${chatMessages.map(msg => renderMessage(msg)).join('')}
                </div>
                
                <div class="chat-input-container">
                    <input 
                        type="text" 
                        id="chat-input" 
                        class="chat-input" 
                        placeholder="Type your question..."
                        maxlength="150"
                    />
                    <button class="btn btn-primary" onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>
    `;

    // Enter key to send
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Scroll to bottom
    const messagesDiv = document.getElementById('chat-messages');
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function renderMessage(message) {
    const time = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    return `
        <div class="message ${message.type}">
            <div>${message.text}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const question = input.value.trim();

    if (!question || question.length < 2) {
        alert('Question must contain at least 2 characters');
        return;
    }

    if (question.length > 150) {
        alert('Question is too long (maximum 150 characters)');
        return;
    }

    // Add user message
    chatMessages.push({ type: 'user', text: question });
    renderChatPage();

    // Disable input
    input.disabled = true;
    const sendBtn = input.nextElementSibling;
    sendBtn.disabled = true;
    sendBtn.textContent = 'Sending...';

    try {
        const response = await API.askQuestion(question);
        
        // Add AI response
        chatMessages.push({ type: 'ai', text: response.answer });
        renderChatPage();
    } catch (error) {
        chatMessages.push({ 
            type: 'ai', 
            text: error.message.includes('rate limit') 
                ? 'Too many requests. Please try again in a minute.'
                : 'Sorry, an error occurred. Please try again.'
        });
        renderChatPage();
    } finally {
        input.disabled = false;
        sendBtn.disabled = false;
        sendBtn.textContent = 'Send';
        input.value = '';
        input.focus();
    }
}

// Tables Page
let currentTab = 'schedules';

function renderTablesPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">Information Tables</h2>
                <p class="card-description">View schedules, technical questions, and general questions</p>
            </div>
            
            <div class="tabs">
                <button class="tab ${currentTab === 'schedules' ? 'active' : ''}" 
                        onclick="switchTab('schedules')">Schedules</button>
                <button class="tab ${currentTab === 'technical' ? 'active' : ''}" 
                        onclick="switchTab('technical')">Technical Questions</button>
                <button class="tab ${currentTab === 'general' ? 'active' : ''}" 
                        onclick="switchTab('general')">General Questions</button>
            </div>
            
            <div id="table-content">
                <div class="loading"><div class="spinner"></div>Loading...</div>
            </div>
        </div>
    `;

    loadTableData();
}

async function switchTab(tab) {
    currentTab = tab;
    renderTablesPage();
}

async function loadTableData() {
    const tableContent = document.getElementById('table-content');
    
    try {
        let data;
        if (currentTab === 'schedules') {
            data = await API.getSchedules();
            renderSchedulesTable(data);
        } else {
            data = await API.getKnowledgeBase(currentTab);
            renderKnowledgeBaseTable(data);
        }
    } catch (error) {
        tableContent.innerHTML = `
            <div class="alert alert-error">
                Error loading data: ${error.message}
            </div>
        `;
    }
}

function formatTime(timeString) {
    // Convert "09:00:00" to "09:00"
    if (!timeString) return '';
    return timeString.substring(0, 5);
}

function getDayOrder(day) {
    // Order: Sunday=0, Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5, Saturday=6
    const dayMap = {
        'sunday': 0, 'ראשון': 0,
        'monday': 1, 'שני': 1,
        'tuesday': 2, 'שלישי': 2,
        'wednesday': 3, 'רביעי': 3,
        'thursday': 4, 'חמישי': 4,
        'friday': 5, 'שישי': 5,
        'saturday': 6, 'שבת': 6
    };
    return dayMap[day.toLowerCase()] ?? 99;
}

function sortSchedules(data) {
    return [...data].sort((a, b) => {
        // First sort by day of week
        const dayA = getDayOrder(a.day_of_week);
        const dayB = getDayOrder(b.day_of_week);
        
        if (dayA !== dayB) {
            return dayA - dayB;
        }
        
        // Then sort by start time
        const timeA = a.start_time || '00:00:00';
        const timeB = b.start_time || '00:00:00';
        return timeA.localeCompare(timeB);
    });
}

function renderSchedulesTable(data) {
    const tableContent = document.getElementById('table-content');
    
    if (data.length === 0) {
        tableContent.innerHTML = '<p class="text-center">No data available</p>';
        return;
    }

    // Sort schedules by day and time
    const sortedData = sortSchedules(data);

    tableContent.innerHTML = `
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Day</th>
                        <th>Start Time</th>
                        <th>End Time</th>
                        <th>Course</th>
                        <th>Lecturer</th>
                        <th>Room</th>
                    </tr>
                </thead>
                <tbody>
                    ${sortedData.map(item => `
                        <tr>
                            <td class="day-cell">${item.day_of_week}</td>
                            <td class="time-cell">${formatTime(item.start_time)}</td>
                            <td class="time-cell">${formatTime(item.end_time)}</td>
                            <td>${item.course_name}</td>
                            <td>${item.lecturer_name}</td>
                            <td>${item.room_name}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

function renderKnowledgeBaseTable(data) {
    const tableContent = document.getElementById('table-content');
    
    if (data.length === 0) {
        tableContent.innerHTML = '<p class="text-center">No data available</p>';
        return;
    }

    tableContent.innerHTML = `
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Topic/Question</th>
                        <th>Answer/Content</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(item => `
                        <tr>
                            <td class="topic-cell">${item.topic_or_question}</td>
                            <td class="content-cell">${item.content_or_answer}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

// Admin Login Page
function renderAdminLoginPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
        <div class="admin-container">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title">Admin Login</h2>
                    <p class="card-description">Enter your username and password</p>
                </div>
                
                <form id="login-form" onsubmit="handleAdminLogin(event)">
                    <div class="form-group">
                        <label class="form-label" for="username">Username</label>
                        <input 
                            type="text" 
                            id="username" 
                            class="form-input" 
                            placeholder="Enter username"
                            required
                        />
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="password">Password</label>
                        <input 
                            type="password" 
                            id="password" 
                            class="form-input" 
                            placeholder="Enter password"
                            required
                        />
                    </div>
                    
                    <div id="login-error" class="hidden"></div>
                    
                    <button type="submit" class="btn btn-primary" style="width: 100%;">
                        Login
                    </button>
                </form>
            </div>
        </div>
    `;
}

async function handleAdminLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');
    const submitBtn = event.target.querySelector('button[type="submit"]');

    errorDiv.classList.add('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Logging in...';

    try {
        const response = await API.adminLogin(username, password);
        localStorage.setItem('admin_token', response.access_token);
        router.navigate('/admin/dashboard');
    } catch (error) {
        errorDiv.classList.remove('hidden');
        errorDiv.className = 'alert alert-error';
        errorDiv.textContent = error.message || 'Login error. Please try again.';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Login';
    }
}

// Admin Dashboard Page
async function renderAdminDashboardPage() {
    const token = localStorage.getItem('admin_token');
    if (!token) {
        router.navigate('/admin/login');
        return;
    }

    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = '<div class="loading"><div class="spinner"></div>Loading...</div>';

    try {
        const data = await API.getAdminDashboard();
        
        mainContent.innerHTML = `
            <div class="admin-container">
                <div class="card">
                    <div class="card-header">
                        <h2 class="card-title">${data.title}</h2>
                        <p class="card-description">${data.description}</p>
                    </div>
                    
                    ${data.options.length > 0 ? `
                        <div class="options-grid">
                            ${data.options.map(option => `
                                <div class="option-card">
                                    <div class="option-icon">📊</div>
                                    <h3 class="option-title">${option.title}</h3>
                                    <p class="option-description">${option.description}</p>
                                </div>
                            `).join('')}
                        </div>
                    ` : `
                        <div class="text-center mt-md">
                            <p>No options available at the moment</p>
                        </div>
                    `}
                </div>
            </div>
        `;
    } catch (error) {
        if (error.message.includes('403') || error.message.includes('Invalid')) {
            localStorage.removeItem('admin_token');
            router.navigate('/admin/login');
        } else {
            mainContent.innerHTML = `
                <div class="alert alert-error">
                    Error loading page: ${error.message}
                </div>
            `;
        }
    }
}

// Route Registration
router.register('/', () => {
    renderNavbar();
    renderLandingPage();
});

router.register('/chat', () => {
    renderNavbar();
    renderChatPage();
});

router.register('/tables', () => {
    renderNavbar();
    renderTablesPage();
});

router.register('/admin/login', () => {
    renderNavbar();
    renderAdminLoginPage();
});

router.register('/admin/dashboard', () => {
    renderNavbar();
    renderAdminDashboardPage();
});

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    router.init();
});
