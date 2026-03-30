/**
 * Placement Portal Application V2
 * Main Vue Application Entry Point
 * Milestone 7: Complete Application
 * CDN Version (No Build Tool Required)
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    
    // Get Vue and VueRouter from global scope (loaded via CDN in index.html)
    const { createApp } = Vue;
    const { createRouter, createWebHashHistory } = VueRouter;
    
    // Import routes from router.js (make sure it exports globally)
    const routes = window.appRoutes || [];
    
    // Create router instance
    const router = createRouter({
        history: createWebHashHistory(),
        routes
    });
    
    // Navigation guard for authentication
    router.beforeEach((to, from, next) => {
        // Update page title
        document.title = to.meta.title || 'Placement Portal V2';
        
        // Check authentication
        const user = localStorage.getItem('user_data');
        const isAuthenticated = !!user;
        let userRole = null;
        
        if (user) {
            try {
                userRole = JSON.parse(user).role;
            } catch (e) {
                userRole = null;
            }
        }
        
        // Check if route requires auth
        if (to.meta.requiresAuth && !isAuthenticated) {
            next('/login');
        }
        // Check if route requires specific role
        else if (to.meta.role && to.meta.role !== userRole) {
            // Redirect to appropriate dashboard based on role
            if (userRole === 'admin') {
                next('/admin/dashboard');
            } else if (userRole === 'company') {
                next('/company/dashboard');
            } else if (userRole === 'student') {
                next('/student/dashboard');
            } else {
                next('/login');
            }
        }
        // Check if login/register page accessed while logged in
        else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
            if (userRole === 'admin') {
                next('/admin/dashboard');
            } else if (userRole === 'company') {
                next('/company/dashboard');
            } else if (userRole === 'student') {
                next('/student/dashboard');
            } else {
                next();
            }
        }
        else {
            next();
        }
    });
    
    // Create Vue app
    const app = createApp({
        data() {
            return {
                isAuthenticated: false,
                userRole: null,
                userName: '',
                isLoading: true
            }
        },
        created() {
            this.checkAuth();
            
            // Listen for storage events (for cross-tab sync)
            window.addEventListener('storage', (e) => {
                if (e.key === 'user_data') {
                    this.checkAuth();
                }
            });
            
            // Listen for custom auth events (for same-tab updates)
            window.addEventListener('auth-state-changed', () => {
                this.checkAuth();
            });
            
            // Check auth on route changes
            this.$router.afterEach((to, from) => {
                this.checkAuth();
            });
        },
        methods: {
            checkAuth() {
                const user = localStorage.getItem('user_data');
                if (user) {
                    try {
                        const userData = JSON.parse(user);
                        this.isAuthenticated = true;
                        this.userRole = userData.role;
                        this.userName = userData.username || userData.full_name;
                    } catch (e) {
                        this.isAuthenticated = false;
                        this.userRole = null;
                        this.userName = '';
                        localStorage.removeItem('user_data');
                    }
                } else {
                    this.isAuthenticated = false;
                    this.userRole = null;
                    this.userName = '';
                }
                this.isLoading = false;
            },
            logout() {
                localStorage.removeItem('user_data');
                localStorage.removeItem('token');
                
                // Dispatch custom event to notify other components
                window.dispatchEvent(new Event('auth-state-changed'));
                
                this.isAuthenticated = false;
                this.userRole = null;
                this.userName = '';
                this.$router.push('/login');
            },
            getNavbarClass() {
                if (!this.isAuthenticated) {
                    return 'bg-primary';
                } else if (this.userRole === 'admin') {
                    return 'bg-dark';
                } else if (this.userRole === 'company') {
                    return 'bg-success';
                } else if (this.userRole === 'student') {
                    return 'bg-info';
                }
                return 'bg-primary';
            }
        },
        template: `
            <div id="app" class="d-flex flex-column min-vh-100">
                <!-- Navigation Bar -->
                <nav v-if="!isLoading" class="navbar navbar-expand-lg navbar-dark" :class="getNavbarClass()">
                    <div class="container-fluid">
                        <a class="navbar-brand" href="#">
                            <i class="bi bi-briefcase"></i> Placement Portal V2
                        </a>
                        <button class="navbar-toggler" type="button" 
                                data-bs-toggle="collapse" 
                                data-bs-target="#navbarNav">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarNav">
                            <ul class="navbar-nav me-auto">
                                <!-- Public Links -->
                                <li class="nav-item" v-if="!isAuthenticated">
                                    <router-link class="nav-link" to="/login">
                                        <i class="bi bi-box-arrow-in-right"></i> Login
                                    </router-link>
                                </li>
                                <li class="nav-item" v-if="!isAuthenticated">
                                    <router-link class="nav-link" to="/register">
                                        <i class="bi bi-person-plus"></i> Register
                                    </router-link>
                                </li>
                                
                                <!-- Admin Links -->
                                <li class="nav-item" v-if="isAuthenticated && userRole === 'admin'">
                                    <router-link class="nav-link" to="/admin/dashboard">
                                        <i class="bi bi-speedometer2"></i> Dashboard
                                    </router-link>
                                </li>
                                <li class="nav-item dropdown" v-if="isAuthenticated && userRole === 'admin'">
                                    <a class="nav-link dropdown-toggle" href="#" 
                                       id="adminDropdown" role="button" 
                                       data-bs-toggle="dropdown">
                                        <i class="bi bi-people"></i> Management
                                    </a>
                                    <ul class="dropdown-menu">
                                        <li><router-link class="dropdown-item" to="/admin/companies">
                                            <i class="bi bi-building"></i> Companies
                                        </router-link></li>
                                        <li><router-link class="dropdown-item" to="/admin/students">
                                            <i class="bi bi-people"></i> Students
                                        </router-link></li>
                                        <li><router-link class="dropdown-item" to="/admin/drives">
                                            <i class="bi bi-briefcase"></i> Drives
                                        </router-link></li>
                                        <li><router-link class="dropdown-item" to="/admin/applications">
                                            <i class="bi bi-file-earmark-text"></i> Applications
                                        </router-link></li>
                                        <li><hr class="dropdown-divider"></li>
                                        <li><router-link class="dropdown-item" to="/admin/monthly_reports">
                                            <i class="bi bi-file-earmark-bar-graph"></i> Monthly Reports
                                        </router-link></li>
                                    </ul>
                                </li>
                                
                                <!-- Company Links -->
                                <li class="nav-item" v-if="isAuthenticated && userRole === 'company'">
                                    <router-link class="nav-link" to="/company/dashboard">
                                        <i class="bi bi-speedometer2"></i> Dashboard
                                    </router-link>
                                </li>
                                <li class="nav-item dropdown" v-if="isAuthenticated && userRole === 'company'">
                                    <a class="nav-link dropdown-toggle" href="#" 
                                       id="companyDropdown" role="button" 
                                       data-bs-toggle="dropdown">
                                        <i class="bi bi-briefcase"></i> Jobs
                                    </a>
                                    <ul class="dropdown-menu">
                                        <li><router-link class="dropdown-item" to="/company/drives">
                                            <i class="bi bi-briefcase"></i> My Drives
                                        </router-link></li>
                                        <li><router-link class="dropdown-item" to="/company/applications">
                                            <i class="bi bi-file-earmark-text"></i> Applications
                                        </router-link></li>
                                        <li><router-link class="dropdown-item" to="/company/placements">
                                            <i class="bi bi-check-circle"></i> Placements
                                        </router-link></li>
                                    </ul>
                                </li>
                                
                                <!-- Student Links -->
                                <li class="nav-item" v-if="isAuthenticated && userRole === 'student'">
                                    <router-link class="nav-link" to="/student/dashboard">
                                        <i class="bi bi-speedometer2"></i> Dashboard
                                    </router-link>
                                </li>
                                <li class="nav-item dropdown" v-if="isAuthenticated && userRole === 'student'">
                                    <a class="nav-link dropdown-toggle" href="#" 
                                       id="studentDropdown" role="button" 
                                       data-bs-toggle="dropdown">
                                        <i class="bi bi-briefcase"></i> Jobs
                                    </a>
                                    <ul class="dropdown-menu">
                                        <li><router-link class="dropdown-item" to="/student/drives">
                                            <i class="bi bi-briefcase"></i> Browse Jobs
                                        </router-link></li>
                                        <li><router-link class="dropdown-item" to="/student/applications">
                                            <i class="bi bi-file-earmark-text"></i> My Applications
                                        </router-link></li>
                                        <li><router-link class="dropdown-item" to="/student/history">
                                            <i class="bi bi-clock-history"></i> History
                                        </router-link></li>
                                    </ul>
                                </li>
                            </ul>
                            
                            <!-- Right Side - User Info & Logout -->
                            <div class="d-flex" v-if="isAuthenticated">
                                <span class="navbar-text me-3">
                                    <i class="bi bi-person-circle"></i> 
                                    Welcome, <strong>{{ userName }}</strong> 
                                    <span class="badge bg-secondary">{{ userRole }}</span>
                                </span>
                                <button @click="logout" class="btn btn-outline-light btn-sm">
                                    <i class="bi bi-box-arrow-right"></i> Logout
                                </button>
                            </div>
                        </div>
                    </div>
                </nav>
                
                <!-- Loading State -->
                <div v-if="isLoading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading...</p>
                </div>
                
                <!-- Main Content (flex: 1 pushes footer to bottom) -->
                <main v-else class="flex-grow-1">
                    <router-view :key="$route.fullPath"></router-view>
                </main>
                
                <!-- Footer (always at bottom) -->
                <footer class="bg-dark text-white text-center py-3 mt-auto">
                    <div class="container">
                        <p class="mb-0">© 2026 Placement Portal V2 | Milestone 8 Complete</p>
                    </div>
                </footer>
            </div>
        `
    });
    
    // Use router
    app.use(router);
    
    // Mount app
    app.mount('#app');
    
    console.log('Vue App Mounted Successfully - Milestone 7 Complete');
});