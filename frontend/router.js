// Simple Router with hash-based routing (works with simple HTTP servers)
class Router {
    constructor() {
        this.routes = {};
        this.currentRoute = '';
    }

    register(path, handler) {
        this.routes[path] = handler;
    }

    getPath() {
        // Get path from hash or pathname
        const hash = window.location.hash.slice(1); // Remove #
        return hash || window.location.pathname || '/';
    }

    navigate(path) {
        if (this.routes[path]) {
            this.currentRoute = path;
            // Use hash routing for compatibility with simple HTTP servers
            window.location.hash = path;
            this.routes[path]();
        } else {
            console.warn(`Route not found: ${path}`);
        }
    }

    init() {
        // Handle hash change
        window.addEventListener('hashchange', () => {
            const path = this.getPath();
            if (this.routes[path]) {
                this.currentRoute = path;
                this.routes[path]();
            }
        });

        // Handle initial load
        const path = this.getPath();
        if (this.routes[path]) {
            this.currentRoute = path;
            this.routes[path]();
        } else {
            // Default to home if route not found
            this.navigate('/');
        }
    }
}

const router = new Router();
