/**
 * Authentication Helper Functions
 * Milestone 2: Authentication and Role-Based Access
 */

const auth = {
    // Set user data after successful login/register
    setUser(userData) {
        localStorage.setItem('user_data', JSON.stringify(userData));
        
        // Dispatch custom event to notify app.js
        window.dispatchEvent(new Event('auth-state-changed'));
    },
    
    // Get current user data
    getUser() {
        const user = localStorage.getItem('user_data');
        return user ? JSON.parse(user) : null;
    },
    
    // Clear user data on logout
    clearUser() {
        localStorage.removeItem('user_data');
        localStorage.removeItem('token');
        
        // Dispatch custom event to notify app.js
        window.dispatchEvent(new Event('auth-state-changed'));
    },
    
    // Check if user is authenticated
    isAuthenticated() {
        return !!this.getUser();
    },
    
    // Get user role
    getRole() {
        const user = this.getUser();
        return user ? user.role : null;
    }
};

// Export auth helper globally
window.auth = auth;

console.log('Auth Helper Loaded');