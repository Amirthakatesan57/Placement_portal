const routes = [

    {
        path: '/',
        name: 'Home',
        meta: { 
            title: 'Placement Portal V2 - Home',
            requiresAuth: false 
        },
        component: {
            template: `
                <div class="text-center py-5">
                    <div class="jumbotron bg-light p-5 rounded shadow-sm">
                        <h1 class="display-4">
                            <i class="bi bi-mortarboard-fill text-primary"></i> 
                            Placement Portal V2
                        </h1>
                        <p class="lead">Connect Students, Companies, and Institutes</p>
                        <hr class="my-4">
                        <p class="mb-4">
                            Streamline your campus recruitment process with our comprehensive 
                            placement management system. Built with Flask + Vue.js
                        </p>
                        <div class="mt-4">
                            <router-link to="/login" class="btn btn-primary btn-lg me-2">
                                <i class="bi bi-box-arrow-in-right"></i> Login
                            </router-link>
                            <router-link to="/register" class="btn btn-success btn-lg">
                                <i class="bi bi-building"></i> Register
                            </router-link>
                        </div>
                    </div>
                    
                    <!-- Feature Cards -->
                    <div class="row mt-5 g-4">
                        <div class="col-md-4">
                            <div class="card h-100 shadow-sm border-0">
                                <div class="card-body text-center p-4">
                                    <i class="bi bi-shield-lock display-4 text-primary mb-3"></i>
                                    <h3 class="h4">Admin</h3>
                                    <p class="text-muted">Manage companies, students, and placement drives with full control</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card h-100 shadow-sm border-0">
                                <div class="card-body text-center p-4">
                                    <i class="bi bi-briefcase display-4 text-success mb-3"></i>
                                    <h3 class="h4">Company</h3>
                                    <p class="text-muted">Create drives, review applications, and hire top talent</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card h-100 shadow-sm border-0">
                                <div class="card-body text-center p-4">
                                    <i class="bi bi-mortarboard display-4 text-info mb-3"></i>
                                    <h3 class="h4">Student</h3>
                                    <p class="text-muted">Apply for jobs, track applications, and get placed</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Milestone Status -->
                    <div class="alert alert-info mt-5">
                        <p class="mb-0">
                            Admin Dashboard | Company Dashboard | Drive Management | Application Management | Interview Scheduling
                        </p>
                    </div>
                </div>
            `
        }
    },
 
 {
    path: '/login',
    name: 'Login',
    meta: { 
        title: 'Login - Placement Portal V2'
    },
    component: {
        template: `
            <div class="row justify-content-center mt-5">
                <div class="col-md-4">
                    <div class="card shadow">
                        <div class="card-header bg-primary text-white">
                            <h4 class="mb-0"><i class="bi bi-box-arrow-in-right"></i> Login</h4>
                        </div>
                        <div class="card-body">
                            <div v-if="error" class="alert alert-danger">
                                <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                            </div>
                            
                            <form @submit.prevent="login">
                                <div class="mb-3">
                                    <label class="form-label">Username</label>
                                    <input type="text" class="form-control" v-model="username" required 
                                           :disabled="loading" placeholder="Enter username">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Password</label>
                                    <input type="password" class="form-control" v-model="password" required 
                                           :disabled="loading" placeholder="Enter password">
                                </div>
                                <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                                    {{ loading ? 'Logging in...' : 'Login' }}
                                </button>
                            </form>
                            
                            <hr>
                            <p class="text-center mb-0">
                                Don't have an account? 
                                <router-link to="/register">Register here</router-link>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                username: '',
                password: '',
                loading: false,
                error: ''
            }
        },
        methods: {
            async login() {
                this.loading = true;
                this.error = '';
                
                try {
                    // Use authAPI from api.js
                    const result = await authAPI.login(this.username, this.password);
                    
                    if (result.success) {
                        // Set user data in auth helper
                        auth.setUser(result.user);
                        
                        // Redirect based on role
                        if (result.user.role === 'admin') {
                            this.$router.push('/admin/dashboard');
                        } else if (result.user.role === 'company') {
                            this.$router.push('/company/dashboard');
                        } else if (result.user.role === 'student') {
                            this.$router.push('/student/dashboard');
                        }
                    } else {
                        this.error = result.error || ' Login failed. Please check credentials.';
                    }
                } catch (err) {
                    console.error('Login error:', err);
                    this.error = ' Login failed. Please check credentials.';
                } finally {
                    this.loading = false;
                }
            }
        }
    }
},   

{
    path: '/register',
    name: 'RegisterSelection',
    meta: { 
        title: 'Register - Placement Portal V2'
    },
    component: {
        template: `
            <div class="row justify-content-center mt-5">
                <div class="col-md-8 col-lg-6">
                    <div class="card shadow">
                        <div class="card-header bg-primary text-white text-center">
                            <h4 class="mb-0">
                                <i class="bi bi-person-plus"></i> Create Your Account
                            </h4>
                        </div>
                        <div class="card-body p-5">
                            <p class="text-center text-muted mb-4">
                                Select your role to continue with registration
                            </p>
                            
                            <div class="row g-4">
                                <!-- Student Registration Card -->
                                <div class="col-md-6">
                                    <router-link to="/register/student" class="text-decoration-none">
                                        <div class="card h-100 border-success shadow-sm hover-card">
                                            <div class="card-body text-center p-4">
                                                <i class="bi bi-mortarboard display-4 text-success mb-3"></i>
                                                <h5 class="card-title text-success">Student</h5>
                                                <p class="card-text text-muted small">
                                                    Register as a student to browse and apply for job opportunities
                                                </p>
                                                <button class="btn btn-outline-success btn-sm mt-2">
                                                    Register as Student <i class="bi bi-arrow-right"></i>
                                                </button>
                                            </div>
                                        </div>
                                    </router-link>
                                </div>
                                
                                <!-- Company Registration Card -->
                                <div class="col-md-6">
                                    <router-link to="/register/company" class="text-decoration-none">
                                        <div class="card h-100 border-info shadow-sm hover-card">
                                            <div class="card-body text-center p-4">
                                                <i class="bi bi-building display-4 text-info mb-3"></i>
                                                <h5 class="card-title text-info">Company</h5>
                                                <p class="card-text text-muted small">
                                                    Register your company to post jobs and recruit students
                                                </p>
                                                <button class="btn btn-outline-info btn-sm mt-2">
                                                    Register as Company <i class="bi bi-arrow-right"></i>
                                                </button>
                                            </div>
                                        </div>
                                    </router-link>
                                </div>
                            </div>
                            
                            <hr class="my-4">
                            
                            <div class="text-center">
                                <p class="mb-0">
                                    Already have an account? 
                                    <router-link to="/login" class="text-primary fw-bold">Login here</router-link>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {}
        },
        methods: {}
    }
},

{
    path: '/register/student',
    name: 'StudentRegister',
    meta: { 
        title: 'Student Registration - Placement Portal V2',
        requiresAuth: false 
    },
    component: {
        template: `
            <div class="row justify-content-center">
                <div class="col-md-8 col-lg-6">
                    <div class="card shadow">
                        <div class="card-header bg-success text-white">
                            <h4 class="mb-0">
                                <i class="bi bi-mortarboard"></i> Student Registration
                            </h4>
                        </div>
                        <div class="card-body">
                            <div v-if="error" class="alert alert-danger">
                                <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                            </div>
                            <div v-if="errors.length" class="alert alert-danger">
                                <ul class="mb-0">
                                    <li v-for="err in errors" :key="err">{{ err }}</li>
                                </ul>
                            </div>
                            <div v-if="success" class="alert alert-success">
                                <i class="bi bi-check-circle-fill"></i> {{ success }}
                            </div>
                            <form @submit.prevent="handleRegister">
                                <h5 class="text-success mb-3">📋 Account Information</h5>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Username *</label>
                                        <input type="text" class="form-control" v-model="form.username" 
                                                required minlength="3" :disabled="loading">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Email *</label>
                                        <input type="email" class="form-control" v-model="form.email" 
                                                required :disabled="loading">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Password *</label>
                                        <input type="password" class="form-control" v-model="form.password" 
                                                required minlength="6" :disabled="loading">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Confirm Password *</label>
                                        <input type="password" class="form-control" v-model="form.confirmPassword" 
                                                required :disabled="loading">
                                    </div>
                                </div>
                                
                                <h5 class="text-success mb-3 mt-4">👤 Personal Information</h5>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Full Name *</label>
                                        <input type="text" class="form-control" v-model="form.full_name" 
                                                required :disabled="loading">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Roll Number *</label>
                                        <input type="text" class="form-control" v-model="form.roll_number" 
                                                required :disabled="loading">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Branch *</label>
                                        <input type="text" class="form-control" v-model="form.branch" 
                                                required :disabled="loading">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Year of Study</label>
                                        <select class="form-select" v-model="form.year_of_study" :disabled="loading">
                                            <option value="1">1st Year</option>
                                            <option value="2">2nd Year</option>
                                            <option value="3">3rd Year</option>
                                            <option value="4" selected>4th Year</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">CGPA *</label>
                                        <input type="number" step="0.01" min="0" max="10" 
                                                class="form-control" v-model="form.cgpa" 
                                                required :disabled="loading">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Phone</label>
                                        <input type="tel" class="form-control" v-model="form.phone" 
                                                :disabled="loading">
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Skills (comma-separated)</label>
                                    <input type="text" class="form-control" v-model="form.skills" 
                                            placeholder="Python, Java, JavaScript" :disabled="loading">
                                </div>
                                
                                <button type="submit" class="btn btn-success w-100" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                                    {{ loading ? 'Registering...' : 'Register' }}
                                </button>
                            </form>
                            <div class="mt-3 text-center">
                                <p>Already have an account?</p>
                                <router-link to="/login" class="text-primary">Login here</router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                form: {
                    username: '',
                    email: '',
                    password: '',
                    confirmPassword: '',
                    full_name: '',
                    roll_number: '',
                    branch: '',
                    year_of_study: '4',
                    cgpa: '',
                    phone: '',
                    skills: ''
                },
                error: '',
                errors: [],
                success: '',
                loading: false
            }
        },
        methods: {
            async handleRegister() {
                this.loading = true;
                this.error = '';
                this.errors = [];
                
                // Validate passwords match
                if (this.form.password !== this.form.confirmPassword) {
                    this.errors = ['Passwords do not match'];
                    this.loading = false;
                    return;
                }
                
                try {
                    const response = await authAPI.registerStudent(this.form);
                    
                    if (response.success) {
                        this.success = ' Registration successful! Redirecting to dashboard...';
                        auth.setUser(response.user);
                        setTimeout(() => {
                            this.$router.push(response.redirect_url || '/student/dashboard');
                        }, 1500);
                    } else {
                        this.error = response.error;
                    }
                } catch (err) {
                    const errorData = err.response?.data;
                    if (errorData?.errors) {
                        this.errors = errorData.errors;
                    } else {
                        this.error = errorData?.error || ' Registration failed';
                    }
                } finally {
                    this.loading = false;
                }
            }
        }    
}
},

{
    path: '/register/company',
    name: 'CompanyRegister',
    meta: { 
        title: 'Company Registration - Placement Portal V2',
        requiresAuth: false 
    },
    component: {
        template: `
            <div class="row justify-content-center">
                <div class="col-md-8 col-lg-6">
                    <div class="card shadow">
                        <div class="card-header bg-info text-white">
                            <h4 class="mb-0">
                                <i class="bi bi-building"></i> Company Registration
                            </h4>
                        </div>
                        <div class="card-body">
                            <div v-if="error" class="alert alert-danger">
                                <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                            </div>
                            <div v-if="errors.length" class="alert alert-danger">
                                <ul class="mb-0">
                                    <li v-for="err in errors" :key="err">{{ err }}</li>
                                </ul>
                            </div>
                            <div v-if="success" class="alert alert-success">
                                <i class="bi bi-check-circle-fill"></i> {{ success }}
                            </div>
                            <div v-if="pendingApproval" class="alert alert-warning">
                                <i class="bi bi-hourglass-split"></i> 
                                <strong>Pending Approval:</strong> Your company registration is pending admin approval. 
                                You will be able to login once approved by the admin.
                            </div>
                            <form @submit.prevent="handleRegister">
                                <h5 class="text-info mb-3">📋 Account Information</h5>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Username *</label>
                                        <input type="text" class="form-control" v-model="form.username" 
                                                required minlength="3" :disabled="loading || pendingApproval">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Email *</label>
                                        <input type="email" class="form-control" v-model="form.email" 
                                                required :disabled="loading || pendingApproval">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Password *</label>
                                        <input type="password" class="form-control" v-model="form.password" 
                                                required minlength="6" :disabled="loading || pendingApproval">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Confirm Password *</label>
                                        <input type="password" class="form-control" v-model="form.confirmPassword" 
                                                required :disabled="loading || pendingApproval">
                                    </div>
                                </div>
                                
                                <h5 class="text-info mb-3 mt-4">🏭 Company Information</h5>
                                <div class="mb-3">
                                    <label class="form-label">Company Name *</label>
                                    <input type="text" class="form-control" v-model="form.company_name" 
                                            required :disabled="loading || pendingApproval">
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Industry *</label>
                                        <input type="text" class="form-control" v-model="form.industry" 
                                                required :disabled="loading || pendingApproval">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Location</label>
                                        <input type="text" class="form-control" v-model="form.location" 
                                                :disabled="loading || pendingApproval">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Website</label>
                                        <input type="url" class="form-control" v-model="form.website" 
                                                :disabled="loading || pendingApproval">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">HR Contact Name</label>
                                        <input type="text" class="form-control" v-model="form.hr_contact_name" 
                                                :disabled="loading || pendingApproval">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">HR Contact Email</label>
                                        <input type="email" class="form-control" v-model="form.hr_contact_email" 
                                                :disabled="loading || pendingApproval">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">HR Contact Phone</label>
                                        <input type="tel" class="form-control" v-model="form.hr_contact_phone" 
                                                :disabled="loading || pendingApproval">
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Company Description</label>
                                    <textarea class="form-control" v-model="form.company_description" 
                                                rows="3" :disabled="loading || pendingApproval"></textarea>
                                </div>
                                
                                <button type="submit" class="btn btn-info w-100" 
                                        :disabled="loading || pendingApproval">
                                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                                    {{ loading ? 'Registering...' : 'Register' }}
                                </button>
                            </form>
                            <div class="mt-3 text-center">
                                <p>Already have an account?</p>
                                <router-link to="/login" class="text-primary">Login here</router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                form: {
                    username: '',
                    email: '',
                    password: '',
                    confirmPassword: '',
                    company_name: '',
                    industry: '',
                    location: '',
                    website: '',
                    hr_contact_name: '',
                    hr_contact_email: '',
                    hr_contact_phone: '',
                    company_description: ''
                },
                error: '',
                errors: [],
                success: '',
                pendingApproval: false,
                loading: false
            }
        },
        methods: {
            async handleRegister() {
                this.loading = true;
                this.error = '';
                this.errors = [];
                this.success = '';
                this.pendingApproval = false;
                
                // Validate passwords match
                if (this.form.password !== this.form.confirmPassword) {
                    this.errors = ['Passwords do not match'];
                    this.loading = false;
                    return;
                }
                
                try {
                    const response = await authAPI.registerCompany(this.form);
                    
                    if (response.success) {
                        this.success = response.message;
                        this.pendingApproval = true;
                    } else {
                        this.error = response.error;
                    }
                } catch (err) {
                    const errorData = err.response?.data;
                    if (errorData?.errors) {
                        this.errors = errorData.errors;
                    } else {
                        this.error = errorData?.error || ' Registration failed';
                    }
                } finally {
                    this.loading = false;
                }
            }
        }
    }
},

{
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    meta: { 
        title: 'Admin Dashboard - Placement Portal V2',
        requiresAuth: true, 
        role: 'admin' 
    },
    component: {
        template: `
            <div>
                <!-- Dashboard Header -->
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-speedometer2"></i> Admin Dashboard
                    </h1>
                    <div class="d-flex gap-2">
                        <!-- Milestone 7: Monthly Reports Button -->
                        <button @click="$router.push('/admin/monthly_reports')" 
                                class="btn btn-outline-danger" 
                                title="View Monthly Placement Reports">
                            <i class="bi bi-file-earmark-bar-graph"></i> Monthly Reports
                        </button>
                        <button @click="loadStats" class="btn btn-primary" :disabled="loading">
                            <i class="bi bi-arrow-clockwise"></i> {{ loading ? 'Loading...' : 'Refresh' }}
                        </button>
                    </div>
                </div>
                
                <!-- Error Alert -->
                <div v-if="error" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                    <button @click="loadStats" class="btn btn-danger btn-sm ms-2">Retry</button>
                </div>
                
                <!-- Loading State -->
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading dashboard statistics...</p>
                </div>
                
                <!-- Dashboard Content -->
                <div v-else-if="stats.total_students !== undefined">
                    
                    <!-- Milestone 7: Quick Stats with Reports Link -->
                    <div class="row mb-4 g-4">
                        <div class="col-md-3 col-sm-6">
                            <div class="card bg-primary text-white h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-people display-6"></i>
                                    <h5 class="card-title mt-2">Total Students</h5>
                                    <h2 class="display-4">{{ stats.total_students || 0 }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <div class="card bg-success text-white h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-building display-6"></i>
                                    <h5 class="card-title mt-2">Total Companies</h5>
                                    <h2 class="display-4">{{ stats.total_companies || 0 }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <div class="card bg-info text-white h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-briefcase display-6"></i>
                                    <h5 class="card-title mt-2">Total Drives</h5>
                                    <h2 class="display-4">{{ stats.total_drives || 0 }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <div class="card bg-warning text-dark h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-file-earmark-text display-6"></i>
                                    <h5 class="card-title mt-2">Total Applications</h5>
                                    <h2 class="display-4">{{ stats.total_applications || 0 }}</h2>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Milestone 7: Placement Statistics with Reports Link -->
                    <div class="row mb-4 g-4">
                        <div class="col-md-4">
                            <div class="card bg-secondary text-white h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-check-circle display-5"></i>
                                    <h5 class="card-title mt-2">Total Placements</h5>
                                    <h2 class="display-4">{{ stats.total_placements || 0 }}</h2>
                                    <button @click="$router.push('/admin/monthly_reports')" 
                                            class="btn btn-sm btn-light mt-2">
                                        <i class="bi bi-file-earmark-bar-graph"></i> View Reports
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card bg-light text-dark h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-activity display-5"></i>
                                    <h5 class="card-title mt-2">Active Drives</h5>
                                    <h2 class="display-4">{{ stats.active_drives || 0 }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card bg-danger text-white h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-slash-circle display-5"></i>
                                    <h5 class="card-title mt-2">Blacklisted Users</h5>
                                    <h2 class="display-4">{{ stats.blacklisted_users || 0 }}</h2>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Pending Approvals -->
                    <div class="row mb-4 g-4">
                        <div class="col-md-6">
                            <div class="card border-warning h-100 shadow-sm">
                                <div class="card-header bg-warning text-dark">
                                    <h5 class="mb-0">
                                        <i class="bi bi-hourglass-split"></i> Pending Company Approvals
                                    </h5>
                                </div>
                                <div class="card-body text-center">
                                    <h2 class="display-4 text-warning">{{ stats.pending_companies || 0 }}</h2>
                                    <button @click="$router.push('/admin/companies')" 
                                            class="btn btn-warning mt-2">
                                        <i class="bi bi-building"></i> Review Companies
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card border-info h-100 shadow-sm">
                                <div class="card-header bg-info text-white">
                                    <h5 class="mb-0">
                                        <i class="bi bi-hourglass-split"></i> Pending Drive Approvals
                                    </h5>
                                </div>
                                <div class="card-body text-center">
                                    <h2 class="display-4 text-info">{{ stats.pending_drives || 0 }}</h2>
                                    <button @click="$router.push('/admin/drives')" 
                                            class="btn btn-info mt-2">
                                        <i class="bi bi-briefcase"></i> Review Drives
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Milestone 7: Celery Jobs Status -->
                    <div class="card mb-4 shadow-sm border-success">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-cpu"></i> Backend Jobs Status (Milestone 7)
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <div class="p-3 bg-light rounded">
                                        <h6><i class="bi bi-calendar-event"></i> Daily Interview Reminders</h6>
                                        <p class="mb-0 text-muted">Runs daily at 9:00 AM</p>
                                        <small class="text-success"><i class="bi bi-check-circle"></i> Active</small>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="p-3 bg-light rounded">
                                        <h6><i class="bi bi-file-earmark-bar-graph"></i> Monthly Reports</h6>
                                        <p class="mb-0 text-muted">1st of every month at 10:00 AM</p>
                                        <small class="text-success"><i class="bi bi-check-circle"></i> Active</small>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="p-3 bg-light rounded">
                                        <h6><i class="bi bi-trash"></i> Cleanup Old Exports</h6>
                                        <p class="mb-0 text-muted">Daily at 2:00 AM</p>
                                        <small class="text-success"><i class="bi bi-check-circle"></i> Active</small>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-3 text-center">
                                <button @click="$router.push('/admin/monthly_reports')" 
                                        class="btn btn-success">
                                    <i class="bi bi-file-earmark-bar-graph"></i> View & Generate Reports
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Quick Actions -->
                    <div class="card mb-4 shadow-sm">
                        <div class="card-header bg-dark text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-lightning-charge-fill"></i> Quick Actions
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row g-3">
                                <div class="col-md-3 col-sm-6">
                                    <button @click="$router.push('/admin/companies')" 
                                            class="btn btn-outline-primary w-100">
                                        <i class="bi bi-building"></i> Companies
                                    </button>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <button @click="$router.push('/admin/students')" 
                                            class="btn btn-outline-success w-100">
                                        <i class="bi bi-people"></i> Students
                                    </button>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <button @click="$router.push('/admin/drives')" 
                                            class="btn btn-outline-info w-100">
                                        <i class="bi bi-briefcase"></i> Drives
                                    </button>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <button @click="$router.push('/admin/applications')" 
                                            class="btn btn-outline-warning w-100">
                                        <i class="bi bi-file-earmark-text"></i> Applications
                                    </button>
                                </div>
                                <!-- Milestone 7: Monthly Reports in Quick Actions -->
                                <div class="col-md-3 col-sm-6">
                                    <button @click="$router.push('/admin/monthly_reports')" 
                                            class="btn btn-outline-danger w-100">
                                        <i class="bi bi-file-earmark-bar-graph"></i> Monthly Reports
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Milestone 7: Recent Activity -->
                    <div class="card mb-4 shadow-sm">
                        <div class="card-header bg-primary text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-clock-history"></i> Recent Activity (Milestone 7)
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>Activity</th>
                                            <th>Type</th>
                                            <th>Status</th>
                                            <th>Last Run</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td><i class="bi bi-calendar-event"></i> Interview Reminders</td>
                                            <td><span class="badge bg-info">Scheduled</span></td>
                                            <td><span class="badge bg-success">Active</span></td>
                                            <td>Daily at 9:00 AM</td>
                                        </tr>
                                        <tr>
                                            <td><i class="bi bi-file-earmark-bar-graph"></i> Monthly Reports</td>
                                            <td><span class="badge bg-info">Scheduled</span></td>
                                            <td><span class="badge bg-success">Active</span></td>
                                            <td>1st of month at 10:00 AM</td>
                                        </tr>
                                        <tr>
                                            <td><i class="bi bi-trash"></i> Cleanup Exports</td>
                                            <td><span class="badge bg-info">Scheduled</span></td>
                                            <td><span class="badge bg-success">Active</span></td>
                                            <td>Daily at 2:00 AM</td>
                                        </tr>
                                        <tr>
                                            <td><i class="bi bi-file-earmark-spreadsheet"></i> CSV Exports</td>
                                            <td><span class="badge bg-warning">User-Triggered</span></td>
                                            <td><span class="badge bg-success">Available</span></td>
                                            <td>On-demand</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                stats: {},
                loading: false,
                error: ''
            }
        },
        created() {
            this.loadStats();
        },
        methods: {
            async loadStats() {
                this.loading = true;
                this.error = '';
                try {
                    const response = await adminAPI.getDashboardStats();
                    this.stats = response.data;
                } catch (err) {
                    console.error('Stats error:', err);
                    this.error = err.response?.data?.error || 'Failed to load dashboard statistics';
                } finally {
                    this.loading = false;
                }
            }
        }
    }
},

{
    path: '/admin/companies',
    name: 'AdminCompanies',
    meta: { 
        title: 'Company Management - Placement Portal V2',
        requiresAuth: true, 
        role: 'admin' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-building"></i> Company Management
                    </h1>
                    <div>
                        <input type="text" class="form-control d-inline-block me-2" 
                               v-model="searchQuery" 
                               placeholder="Search companies..." 
                               style="width: 250px;"
                               @keyup.enter="loadCompanies">
                        <button @click="loadCompanies" class="btn btn-primary" :disabled="loading">
                            <i class="bi bi-search"></i> Search
                        </button>
                    </div>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading companies...</p>
                </div>
                
                <div v-else-if="companies.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No companies found</p>
                </div>
                
                <div v-else class="card shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-building"></i> Registered Companies ({{ companies.length }})
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead class="table-light">
                                    <tr>
                                        <th>Company Name</th>
                                        <th>Industry</th>
                                        <th>Location</th>
                                        <th>Email</th>
                                        <th>Status</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="company in companies" :key="company.id">
                                        <td><strong>{{ company.company_name }}</strong></td>
                                        <td>{{ company.industry }}</td>
                                        <td>{{ company.location }}</td>
                                        <td>{{ company.email }}</td>
                                        <td>
                                            <span :class="getStatusBadge(company.approval_status)">
                                                {{ company.approval_status }}
                                            </span>
                                        </td>
                                        <td>
                                            <div class="btn-group btn-group-sm">
                                                <button @click="viewCompany(company.id)" 
                                                        class="btn btn-info" 
                                                        title="View Details">
                                                    <i class="bi bi-eye"></i> View
                                                </button>
                                                <button v-if="company.approval_status === 'pending'" 
                                                        @click="approveCompany(company.id)" 
                                                        class="btn btn-success" 
                                                        title="Approve">
                                                    <i class="bi bi-check-circle"></i> Approve
                                                </button>
                                                <button v-if="company.approval_status !== 'blacklisted'" 
                                                        @click="blacklistCompany(company.id)" 
                                                        class="btn btn-danger" 
                                                        title="Blacklist">
                                                    <i class="bi bi-slash-circle"></i> Blacklist
                                                </button>
                                                <button v-if="company.approval_status === 'blacklisted'" 
                                                        @click="unblacklistCompany(company.id)" 
                                                        class="btn btn-warning" 
                                                        title="Unblacklist">
                                                    <i class="bi bi-check-circle"></i> Restore
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                
                <!-- Company Details Modal -->
                <div v-if="showCompanyModal" class="modal fade show d-block" tabindex="-1" 
                     style="background-color: rgba(0,0,0,0.5);">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header bg-primary text-white">
                                <h5 class="modal-title">
                                    <i class="bi bi-building"></i> Company Details
                                </h5>
                                <button type="button" class="btn-close btn-close-white" 
                                        @click="closeCompanyModal"></button>
                            </div>
                            <div class="modal-body">
                                <div v-if="selectedCompany">
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <h6><strong>Company Name:</strong></h6>
                                            <p>{{ selectedCompany.company_name }}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <h6><strong>Industry:</strong></h6>
                                            <p>{{ selectedCompany.industry }}</p>
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <h6><strong>Location:</strong></h6>
                                            <p>{{ selectedCompany.location }}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <h6><strong>Website:</strong></h6>
                                            <p><a :href="selectedCompany.website" target="_blank">{{ selectedCompany.website }}</a></p>
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <h6><strong>HR Contact Name:</strong></h6>
                                            <p>{{ selectedCompany.hr_contact_name }}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <h6><strong>HR Contact Email:</strong></h6>
                                            <p>{{ selectedCompany.hr_contact_email }}</p>
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <h6><strong>HR Contact Phone:</strong></h6>
                                            <p>{{ selectedCompany.hr_contact_phone }}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <h6><strong>Approval Status:</strong></h6>
                                            <p>
                                                <span :class="getStatusBadge(selectedCompany.approval_status)">
                                                    {{ selectedCompany.approval_status }}
                                                </span>
                                            </p>
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <h6><strong>Registered On:</strong></h6>
                                            <p>{{ formatDate(selectedCompany.created_at) }}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <h6><strong>Approved On:</strong></h6>
                                            <p>{{ formatDate(selectedCompany.approved_at) }}</p>
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <h6><strong>Company Description:</strong></h6>
                                        <p>{{ selectedCompany.company_description || 'No description provided' }}</p>
                                    </div>
                                    <div class="mb-3">
                                        <h6><strong>User Account:</strong></h6>
                                        <p>Username: {{ selectedCompany.username }} | Email: {{ selectedCompany.email }}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="closeCompanyModal">
                                    <i class="bi bi-x-lg"></i> Close
                                </button>
                                <button v-if="selectedCompany && selectedCompany.approval_status === 'pending'" 
                                        type="button" class="btn btn-success" 
                                        @click="approveCompany(selectedCompany.id); closeCompanyModal()">
                                    <i class="bi bi-check-circle"></i> Approve Company
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                companies: [],
                loading: false,
                searchQuery: '',
                showCompanyModal: false,
                selectedCompany: null
            }
        },
        created() {
            this.loadCompanies();
        },
        methods: {
            async loadCompanies() {
                this.loading = true;
                try {
                    const response = await adminAPI.getCompanies({
                        search: this.searchQuery
                    });
                    this.companies = response.data.companies;
                } catch (err) {
                    console.error('Error loading companies:', err);
                    alert('Failed to load companies');
                } finally {
                    this.loading = false;
                }
            },
            viewCompany(companyId) {
                const company = this.companies.find(c => c.id === companyId);
                if (company) {
                    this.selectedCompany = company;
                    this.showCompanyModal = true;
                }
            },
            closeCompanyModal() {
                this.showCompanyModal = false;
                this.selectedCompany = null;
            },
            async approveCompany(companyId) {
                if (!confirm('Are you sure you want to approve this company?')) return;
                try {
                    await adminAPI.approveCompany(companyId);
                    alert('✅ Company approved successfully');
                    // FORCE RELOAD - Clear cache and reload
                    await this.clearCacheAndReload();
                } catch (err) {
                    alert(err.response?.data?.error || 'Failed to approve company');
                }
            },
            async blacklistCompany(companyId) {
                if (!confirm('Are you sure you want to blacklist this company?')) return;
                try {
                    await adminAPI.blacklistCompany(companyId);
                    alert('✅ Company blacklisted successfully');
                    // FORCE RELOAD - Clear cache and reload
                    await this.clearCacheAndReload();
                } catch (err) {
                    alert(err.response?.data?.error || 'Failed to blacklist company');
                }
            },
            async unblacklistCompany(companyId) {
                if (!confirm('Are you sure you want to restore this company?')) return;
                try {
                    await adminAPI.unblacklistCompany(companyId);
                    alert('✅ Company restored successfully');
                    // FORCE RELOAD - Clear cache and reload
                    await this.clearCacheAndReload();
                } catch (err) {
                    alert(err.response?.data?.error || 'Failed to restore company');
                }
            },
            // ADD THIS METHOD - Clear cache and reload data
            async clearCacheAndReload() {
                try {
                    // Clear admin cache
                    await adminAPI.clearCache();
                } catch (err) {
                    console.error('Cache clear error:', err);
                } finally {
                    // Always reload companies regardless of cache clear success
                    await this.loadCompanies();
                }
            },
            getStatusBadge(status) {
                const badges = {
                    'pending': 'badge bg-warning text-dark',
                    'approved': 'badge bg-success',
                    'rejected': 'badge bg-danger',
                    'blacklisted': 'badge bg-dark'
                };
                return badges[status] || 'badge bg-secondary';
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            }
        }    
    }
},
    
{
    path: '/admin/students',
    name: 'AdminStudents',
    meta: { 
        title: 'Student Management - Placement Portal V2',
        requiresAuth: true, 
        role: 'admin' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-people"></i> Student Management
                    </h1>
                    <div>
                        <input type="text" class="form-control d-inline-block me-2" 
                               v-model="searchQuery" 
                               placeholder="Search students..." 
                               style="width: 250px;"
                               @keyup.enter="loadStudents">
                        <button @click="loadStudents" class="btn btn-primary" :disabled="loading">
                            <i class="bi bi-search"></i> Search
                        </button>
                    </div>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading students...</p>
                </div>
                
                <div v-else-if="students.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No students found</p>
                </div>
                
                <div v-else class="card shadow-sm">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-people"></i> Registered Students ({{ students.length }})
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead class="table-light">
                                    <tr>
                                        <th>Student Name</th>
                                        <th>Roll Number</th>
                                        <th>Branch</th>
                                        <th>CGPA</th>
                                        <th>Email</th>
                                        <th>Status</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="student in students" :key="student.id">
                                        <td><strong>{{ student.full_name }}</strong></td>
                                        <td>{{ student.roll_number }}</td>
                                        <td>{{ student.branch }}</td>
                                        <td>{{ student.cgpa }}</td>
                                        <td>{{ student.email }}</td>
                                        <td>
                                            <span :class="student.is_blacklisted ? 'badge bg-danger' : 'badge bg-success'">
                                                {{ student.is_blacklisted ? 'Blacklisted' : 'Active' }}
                                            </span>
                                        </td>
                                        <td>
                                            <div class="btn-group btn-group-sm">
                                                <button @click="viewStudent(student.id)" 
                                                        class="btn btn-info" 
                                                        title="View Details">
                                                    <i class="bi bi-eye"></i> View
                                                </button>
                                                <button v-if="!student.is_blacklisted" 
                                                        @click="blacklistStudent(student.id)" 
                                                        class="btn btn-danger" 
                                                        title="Blacklist">
                                                    <i class="bi bi-slash-circle"></i> Blacklist
                                                </button>
                                                <button v-if="student.is_blacklisted" 
                                                        @click="unblacklistStudent(student.id)" 
                                                        class="btn btn-warning" 
                                                        title="Restore">
                                                    <i class="bi bi-check-circle"></i> Restore
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                
                <!-- Student Details Modal -->
                <div v-if="showStudentModal" class="modal fade show d-block" tabindex="-1" 
                     style="background-color: rgba(0,0,0,0.5);">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header bg-success text-white">
                                <h5 class="modal-title">
                                    <i class="bi bi-person"></i> Student Details
                                </h5>
                                <button type="button" class="btn-close btn-close-white" 
                                        @click="closeStudentModal"></button>
                            </div>
                            <div class="modal-body">
                                <div v-if="selectedStudent">
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <h6><strong>Full Name:</strong></h6>
                                            <p>{{ selectedStudent.full_name }}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <h6><strong>Roll Number:</strong></h6>
                                            <p>{{ selectedStudent.roll_number }}</p>
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <h6><strong>Branch:</strong></h6>
                                            <p>{{ selectedStudent.branch }}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <h6><strong>Year of Study:</strong></h6>
                                            <p>{{ selectedStudent.year_of_study }}</p>
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <h6><strong>CGPA:</strong></h6>
                                            <p>{{ selectedStudent.cgpa }}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <h6><strong>Email:</strong></h6>
                                            <p>{{ selectedStudent.email }}</p>
                                        </div>
                                    </div>
                                    <div class="row mb-3">
                                        <div class="col-md-6">
                                            <h6><strong>Phone:</strong></h6>
                                            <p>{{ selectedStudent.phone }}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <h6><strong>Account Status:</strong></h6>
                                            <p>
                                                <span :class="selectedStudent.is_blacklisted ? 'badge bg-danger' : 'badge bg-success'">
                                                    {{ selectedStudent.is_blacklisted ? 'Blacklisted' : 'Active' }}
                                                </span>
                                            </p>
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <h6><strong>Skills:</strong></h6>
                                        <p>{{ selectedStudent.skills || 'No skills listed' }}</p>
                                    </div>
                                    <div class="mb-3">
                                        <h6><strong>Education Details:</strong></h6>
                                        <p>{{ selectedStudent.education_details || 'No education details provided' }}</p>
                                    </div>
                                    <div class="mb-3">
                                        <h6><strong>Experience Details:</strong></h6>
                                        <p>{{ selectedStudent.experience_details || 'No experience details provided' }}</p>
                                    </div>
                                    <div class="mb-3">
                                        <h6><strong>Registered On:</strong></h6>
                                        <p>{{ formatDate(selectedStudent.created_at) }}</p>
                                    </div>
                                    <div v-if="selectedStudent.resume_path" class="mb-3">
                                        <h6><strong>Resume:</strong></h6>
                                        <a :href="selectedStudent.resume_path" target="_blank" class="btn btn-sm btn-outline-primary">
                                            <i class="bi bi-file-earmark-pdf"></i> View Resume
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="closeStudentModal">
                                    <i class="bi bi-x-lg"></i> Close
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                students: [],
                loading: false,
                searchQuery: '',
                showStudentModal: false,
                selectedStudent: null
            }
        },
        created() {
            this.loadStudents();
        },
        methods: {
            async loadStudents() {
                this.loading = true;
                try {
                    const response = await adminAPI.getStudents({
                        search: this.searchQuery
                    });
                    this.students = response.data.students;
                } catch (err) {
                    console.error('Error loading students:', err);
                    alert('Failed to load students');
                } finally {
                    this.loading = false;
                }
            },
            viewStudent(studentId) {
                const student = this.students.find(s => s.id === studentId);
                if (student) {
                    this.selectedStudent = student;
                    this.showStudentModal = true;
                }
            },
            closeStudentModal() {
                this.showStudentModal = false;
                this.selectedStudent = null;
            },
            async blacklistStudent(studentId) {
                if (!confirm('Are you sure you want to blacklist this student?')) return;
                try {
                    await adminAPI.blacklistStudent(studentId);
                    alert(' Student blacklisted successfully');
                    this.loadStudents();
                } catch (err) {
                    alert(err.response?.data?.error || 'Failed to blacklist student');
                }
            },
            async unblacklistStudent(studentId) {
                if (!confirm('Are you sure you want to restore this student?')) return;
                try {
                    await adminAPI.unblacklistStudent(studentId);
                    alert(' Student restored successfully');
                    this.loadStudents();
                } catch (err) {
                    alert(err.response?.data?.error || 'Failed to restore student');
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            }
        }
    }
},
    
    {
        path: '/admin/drives',
        name: 'AdminDrives',
        meta: { 
            title: 'Drive Management - Placement Portal V2',
            requiresAuth: true, 
            role: 'admin' 
        },
        component: {
            template: `
                <div>
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h1>
                            <i class="bi bi-briefcase"></i> Placement Drive Management
                        </h1>
                        <button @click="loadDrives" class="btn btn-primary" :disabled="loading">
                            <i class="bi bi-arrow-clockwise"></i> Refresh
                        </button>
                    </div>
                    
                    <!-- Search and Filters -->
                    <div class="card mb-4 shadow-sm">
                        <div class="card-body">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <input type="text" class="form-control" v-model="search" 
                                           placeholder="Search by job title..." 
                                           @keyup.enter="loadDrives" :disabled="loading">
                                </div>
                                <div class="col-md-3">
                                    <select class="form-select" v-model="status" @change="loadDrives" 
                                            :disabled="loading">
                                        <option value="">All Status</option>
                                        <option value="pending">Pending</option>
                                        <option value="approved">Approved</option>
                                        <option value="active">Active</option>
                                        <option value="closed">Closed</option>
                                        <option value="rejected">Rejected</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <button @click="loadDrives" class="btn btn-primary w-100" 
                                            :disabled="loading">
                                        <i class="bi bi-search"></i> Search
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Drives Table -->
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <div v-if="loading" class="text-center py-5">
                                <div class="spinner-border text-primary" role="status"></div>
                                <p class="mt-2">Loading drives...</p>
                            </div>
                            <table v-else class="table table-hover">
                                <thead class="table-light">
                                    <tr>
                                        <th>Job Title</th>
                                        <th>Company</th>
                                        <th>Salary</th>
                                        <th>Location</th>
                                        <th>Status</th>
                                        <th>Applications</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="drive in drives" :key="drive.id">
                                        <td><strong>{{ drive.job_title }}</strong></td>
                                        <td>{{ drive.company_name }}</td>
                                        <td>₹{{ drive.salary.toLocaleString() }}</td>
                                        <td>{{ drive.location }}</td>
                                        <td>
                                            <span :class="getDriveStatusBadge(drive.status)">
                                                {{ drive.status }}
                                            </span>
                                        </td>
                                        <td>{{ drive.application_count }}</td>
                                        <td>
                                            <div class="btn-group btn-group-sm">
                                                <button v-if="drive.status === 'pending'" 
                                                        @click="approveDrive(drive.id)" 
                                                        class="btn btn-success" title="Approve">
                                                    <i class="bi bi-check-lg"></i>
                                                </button>
                                                <button v-if="drive.status === 'pending'" 
                                                        @click="rejectDrive(drive.id)" 
                                                        class="btn btn-danger" title="Reject">
                                                    <i class="bi bi-x-lg"></i>
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            `,
            data() {
                return {
                    drives: [],
                    loading: false,
                    search: '',
                    status: '',
                    currentPage: 1,
                    totalPages: 1
                }
            },
            created() {
                this.loadDrives();
            },
            methods: {
                async loadDrives() {
                    this.loading = true;
                    try {
                        const response = await adminAPI.getDrives({
                            page: this.currentPage,
                            search: this.search,
                            status: this.status
                        });
                        this.drives = response.data.drives;
                        this.totalPages = response.data.pages;
                    } catch (err) {
                        console.error('Error loading drives:', err);
                        alert('Failed to load drives');
                    } finally {
                        this.loading = false;
                    }
                },
                async approveDrive(id) {
                    if (!confirm(' Approve this placement drive?')) return;
                    try {
                        await adminAPI.approveDrive(id);
                        alert(' Drive approved successfully');
                        this.loadDrives();
                    } catch (err) {
                        alert(err.response?.data?.error || 'Failed to approve drive');
                    }
                },
                async rejectDrive(id) {
                    if (!confirm(' Reject this placement drive?')) return;
                    try {
                        await adminAPI.rejectDrive(id);
                        alert('Drive rejected');
                        this.loadDrives();
                    } catch (err) {
                        alert('Failed to reject drive');
                    }
                },
                getDriveStatusBadge(status) {
                    const badges = {
                        'pending': 'badge bg-warning text-dark',
                        'approved': 'badge bg-success',
                        'active': 'badge bg-info',
                        'closed': 'badge bg-secondary',
                        'rejected': 'badge bg-danger'
                    };
                    return badges[status] || 'badge bg-secondary';
                }
            }
        }
    },
    
{
    path: '/admin/applications',
    name: 'AdminApplications',
    meta: { 
        title: 'Application Management - Placement Portal V2',
        requiresAuth: true, 
        role: 'admin' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1><i class="bi bi-file-earmark-text"></i> All Applications</h1>
                    <button @click="loadApplications" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <div class="card mb-4 shadow-sm">
                    <div class="card-body">
                        <div class="row g-3">
                            <div class="col-md-4">
                                <select class="form-select" v-model="status" @change="loadApplications" :disabled="loading">
                                    <option value="">All Status</option>
                                    <option value="applied">Applied</option>
                                    <option value="shortlisted">Shortlisted</option>
                                    <option value="interview">Interview</option>
                                    <option value="selected">Selected</option>
                                    <option value="rejected">Rejected</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <button @click="loadApplications" class="btn btn-primary w-100" :disabled="loading">
                                    <i class="bi bi-search"></i> Filter
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading applications...</p>
                </div>
                
                <div v-else-if="applications.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No applications found</p>
                    <p class="text-muted">Applications will appear here when students apply to drives</p>
                </div>
                
                <div v-else class="card shadow-sm">
                    <div class="card-body">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Student</th>
                                    <th>Roll No</th>
                                    <th>Job Title</th>
                                    <th>Company</th>
                                    <th>Status</th>
                                    <th>Applied Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="app in applications" :key="app.id">
                                    <td>{{ app.student_name }}</td>
                                    <td>{{ app.student_roll }}</td>
                                    <td>{{ app.drive_title }}</td>
                                    <td>{{ app.company_name }}</td>
                                    <td>
                                        <span :class="getStatusBadge(app.status)">
                                            {{ app.status }}
                                        </span>
                                    </td>
                                    <td>{{ formatDate(app.application_date) }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                applications: [],
                loading: false,
                status: '',
                currentPage: 1,
                totalPages: 1
            }
        },
        created() {
            this.loadApplications();
        },
        methods: {
            async loadApplications() {
                this.loading = true;
                try {
                    const response = await adminAPI.getApplications({
                        page: this.currentPage,
                        status: this.status
                    });
                    this.applications = response.data.applications;
                    this.totalPages = response.data.pages;
                } catch (err) {
                    console.error('Error loading applications:', err);
                    alert('Failed to load applications: ' + (err.response?.data?.error || 'Unknown error'));
                } finally {
                    this.loading = false;
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                const badges = {
                    'applied': 'badge bg-primary',
                    'shortlisted': 'badge bg-warning text-dark',
                    'interview': 'badge bg-info',
                    'selected': 'badge bg-success',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},
    
    // ========================================================================
    // COMPANY ROUTES (Milestone 4)
    // ========================================================================
    
    {
        path: '/company/dashboard',
        name: 'CompanyDashboard',
        meta: { 
            title: 'Company Dashboard - Placement Portal V2',
            requiresAuth: true, 
            role: 'company' 
        },
        component: {
            template: `
                <div>
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h1>
                            <i class="bi bi-briefcase"></i> Company Dashboard
                        </h1>
                        <button @click="loadStats" class="btn btn-primary" :disabled="loading">
                            <i class="bi bi-arrow-clockwise"></i> {{ loading ? 'Loading...' : 'Refresh' }}
                        </button>
                    </div>
                    
                    <div v-if="error" class="alert alert-danger">
                        <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                        <button @click="loadStats" class="btn btn-danger btn-sm ms-2">Retry</button>
                    </div>
                    
                    <div v-if="loading" class="text-center py-5">
                        <div class="spinner-border text-primary" role="status"></div>
                        <p class="mt-2">Loading dashboard statistics...</p>
                    </div>
                    
                    <div v-else-if="stats.company_name !== undefined">
                        <!-- Company Info -->
                        <div class="card mb-4 shadow-sm">
                            <div class="card-header bg-primary text-white">
                                <h5 class="mb-0">
                                    <i class="bi bi-building"></i> {{ stats.company_name }}
                                </h5>
                            </div>
                            <div class="card-body">
                                <span class="badge" :class="stats.approval_status === 'approved' ? 'bg-success' : 'bg-warning'">
                                    {{ stats.approval_status }}
                                </span>
                                <span class="badge bg-info ms-2">{{ stats.industry }}</span>
                            </div>
                        </div>
                        
                        <!-- Stats Cards -->
                        <div class="row mb-4 g-4">
                            <div class="col-md-3 col-sm-6">
                                <div class="card bg-primary text-white h-100 shadow-sm">
                                    <div class="card-body text-center">
                                        <i class="bi bi-briefcase display-6"></i>
                                        <h5 class="card-title mt-2">Total Drives</h5>
                                        <h2 class="display-4">{{ stats.total_drives || 0 }}</h2>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-sm-6">
                                <div class="card bg-success text-white h-100 shadow-sm">
                                    <div class="card-body text-center">
                                        <i class="bi bi-check-circle display-6"></i>
                                        <h5 class="card-title mt-2">Active Drives</h5>
                                        <h2 class="display-4">{{ stats.active_drives || 0 }}</h2>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-sm-6">
                                <div class="card bg-info text-white h-100 shadow-sm">
                                    <div class="card-body text-center">
                                        <i class="bi bi-people display-6"></i>
                                        <h5 class="card-title mt-2">Total Applications</h5>
                                        <h2 class="display-4">{{ stats.total_applications || 0 }}</h2>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-sm-6">
                                <div class="card bg-warning text-dark h-100 shadow-sm">
                                    <div class="card-body text-center">
                                        <i class="bi bi-star display-6"></i>
                                        <h5 class="card-title mt-2">Placements</h5>
                                        <h2 class="display-4">{{ stats.total_placements || 0 }}</h2>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Quick Actions -->
                        <div class="card mb-4 shadow-sm">
                            <div class="card-header bg-dark text-white">
                                <h5 class="mb-0">
                                    <i class="bi bi-lightning-charge-fill"></i> Quick Actions
                                </h5>
                            </div>
                            <div class="card-body">
                                <div class="row g-3">
                                    <div class="col-md-3 col-sm-6">
                                        <button @click="$router.push('/company/drives')" 
                                                class="btn btn-outline-primary w-100">
                                            <i class="bi bi-briefcase"></i> Manage Drives
                                        </button>
                                    </div>
                                    <div class="col-md-3 col-sm-6">
                                        <button @click="$router.push('/company/applications')" 
                                                class="btn btn-outline-success w-100">
                                            <i class="bi bi-people"></i> Applications
                                        </button>
                                    </div>
                                    <div class="col-md-3 col-sm-6">
                                        <button @click="$router.push('/company/placements')" 
                                                class="btn btn-outline-info w-100">
                                            <i class="bi bi-file-earmark-check"></i> Placements
                                        </button>
                                    </div>
                                    <div class="col-md-3 col-sm-6">
                                        <button @click="$router.push('/company/profile')" 
                                                class="btn btn-outline-secondary w-100">
                                            <i class="bi bi-person"></i> Profile
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `,
            data() {
                return {
                    stats: {},
                    loading: false,
                    error: ''
                }
            },
            created() {
                this.loadStats();
            },
            methods: {
                async loadStats() {
                    this.loading = true;
                    this.error = '';
                    try {
                        const response = await companyAPI.getDashboardStats();
                        this.stats = response.data;
                    } catch (err) {
                        console.error('Stats error:', err);
                        this.error = err.response?.data?.error || 'Failed to load dashboard statistics';
                    } finally {
                        this.loading = false;
                    }
                }
            }
        }
    },
    
    {
        path: '/company/drives',
        name: 'CompanyDrives',
        meta: { 
            title: 'Placement Drives - Placement Portal V2',
            requiresAuth: true, 
            role: 'company' 
        },
        component: {
            template: `
                <div>
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h1>
                            <i class="bi bi-briefcase"></i> Placement Drives
                        </h1>
                        <div>
                            <button @click="$router.push('/company/drives/create')" 
                                    class="btn btn-success me-2">
                                <i class="bi bi-plus-lg"></i> Create Drive
                            </button>
                            <button @click="loadDrives" class="btn btn-primary" :disabled="loading">
                                <i class="bi bi-arrow-clockwise"></i> Refresh
                            </button>
                        </div>
                    </div>
                    
                    <!-- Search and Filters -->
                    <div class="card mb-4 shadow-sm">
                        <div class="card-body">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <select class="form-select" v-model="status" @change="loadDrives" 
                                            :disabled="loading">
                                        <option value="">All Status</option>
                                        <option value="pending">Pending</option>
                                        <option value="approved">Approved</option>
                                        <option value="active">Active</option>
                                        <option value="closed">Closed</option>
                                        <option value="rejected">Rejected</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <button @click="loadDrives" class="btn btn-primary w-100" 
                                            :disabled="loading">
                                        <i class="bi bi-search"></i> Search
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Drives Table -->
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <div v-if="loading" class="text-center py-5">
                                <div class="spinner-border text-primary" role="status"></div>
                                <p class="mt-2">Loading drives...</p>
                            </div>
                            <div v-else-if="drives.length === 0" class="text-center py-5">
                                <i class="bi bi-inbox display-4 text-muted"></i>
                                <p class="text-muted mt-2">No drives found</p>
                                <button @click="$router.push('/company/drives/create')" 
                                        class="btn btn-success mt-2">
                                    <i class="bi bi-plus-lg"></i> Create Your First Drive
                                </button>
                            </div>
                            <table v-else class="table table-hover">
                                <thead class="table-light">
                                    <tr>
                                        <th>Job Title</th>
                                        <th>Location</th>
                                        <th>Salary</th>
                                        <th>Deadline</th>
                                        <th>Status</th>
                                        <th>Applications</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="drive in drives" :key="drive.id">
                                        <td><strong>{{ drive.job_title }}</strong></td>
                                        <td>{{ drive.location }}</td>
                                        <td>₹{{ drive.salary.toLocaleString() }}</td>
                                        <td>{{ formatDate(drive.application_deadline) }}</td>
                                        <td>
                                            <span :class="getDriveStatusBadge(drive.status)">
                                                {{ drive.status }}
                                            </span>
                                        </td>
                                        <td>{{ drive.application_count }}</td>
                                        <td>
                                            <div class="btn-group btn-group-sm">
                                                <button @click="viewDriveDetails(drive.id)" 
                                                        class="btn btn-info" title="View Details">
                                                    <i class="bi bi-eye"></i>
                                                </button>
                                                <button @click="viewApplications(drive.id)" 
                                                        class="btn btn-success" title="View Applications">
                                                    <i class="bi bi-people"></i>
                                                </button>
                                                <button v-if="drive.status === 'approved'" 
                                                        @click="updateDriveStatus(drive.id, 'closed')" 
                                                        class="btn btn-warning" title="Close Drive">
                                                    <i class="bi bi-x-circle"></i>
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            `,
            data() {
                return {
                    drives: [],
                    loading: false,
                    status: '',
                    currentPage: 1,
                    totalPages: 1
                }
            },
            created() {
                this.loadDrives();
            },
            methods: {
                async loadDrives() {
                    this.loading = true;
                    try {
                        const response = await companyAPI.getDrives({
                            page: this.currentPage,
                            status: this.status
                        });
                        this.drives = response.data.drives;
                        this.totalPages = response.data.pages;
                    } catch (err) {
                        console.error('Error loading drives:', err);
                        alert('Failed to load drives');
                    } finally {
                        this.loading = false;
                    }
                },
                async updateDriveStatus(driveId, status) {
                    if (!confirm('Are you sure you want to mark this drive as ' + status + '?')) return;
                    try {
                        await companyAPI.updateDriveStatus(driveId, { status: status });
                        alert('Drive marked as ' + status);
                        this.loadDrives();
                    } catch (err) {
                        alert(err.response?.data?.error || 'Failed to update status');
                    }
                },
                viewDriveDetails: function(driveId) {
                    this.$router.push('/company/drives/' + driveId);
                },
                viewApplications: function(driveId) {
                    this.$router.push('/company/drives/' + driveId + '/applications');
                },
                formatDate: function(dateString) {
                    if (!dateString) return 'N/A';
                    return new Date(dateString).toLocaleDateString();
                },
                getDriveStatusBadge: function(status) {
                    var badges = {
                        'pending': 'badge bg-warning text-dark',
                        'approved': 'badge bg-success',
                        'active': 'badge bg-info',
                        'closed': 'badge bg-secondary',
                        'rejected': 'badge bg-danger'
                    };
                    return badges[status] || 'badge bg-secondary';
                }
            }
        }
    },
    
    {
    path: '/company/drives/create',
    name: 'CompanyCreateDrive',
    meta: { 
        title: 'Create Drive - Placement Portal V2',
        requiresAuth: true, 
        role: 'company' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-plus-lg"></i> Create Placement Drive
                    </h1>
                    <button @click="$router.push('/company/drives')" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Back
                    </button>
                </div>
                
                <div class="card shadow-sm">
                    <div class="card-body">
                        <form @submit.prevent="createDrive">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Job Title *</label>
                                    <input type="text" class="form-control" v-model="form.job_title" 
                                           required :disabled="loading">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Location *</label>
                                    <input type="text" class="form-control" v-model="form.location" 
                                           required :disabled="loading">
                                </div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Job Description *</label>
                                <textarea class="form-control" v-model="form.job_description" 
                                          rows="4" required :disabled="loading"></textarea>
                            </div>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Salary (₹) *</label>
                                    <input type="number" class="form-control" v-model="form.salary" 
                                           required min="0" :disabled="loading">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Application Deadline *</label>
                                    <input type="datetime-local" class="form-control" 
                                           v-model="form.application_deadline" required :disabled="loading">
                                    <small class="text-muted">Select date and time for application deadline</small>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Eligibility Criteria *</label>
                                <textarea class="form-control" v-model="form.eligibility_criteria" 
                                          rows="3" required :disabled="loading" 
                                          placeholder="e.g., CGPA >= 7.0, Branch: CS/IT"></textarea>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Skills Required</label>
                                <input type="text" class="form-control" v-model="form.skills_required" 
                                       placeholder="e.g., Python, Java, JavaScript" :disabled="loading">
                            </div>
                            <div v-if="error" class="alert alert-danger">
                                <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                            </div>
                            <button type="submit" class="btn btn-success" :disabled="loading">
                                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                                {{ loading ? 'Creating...' : 'Create Drive' }}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                form: {
                    job_title: '',
                    job_description: '',
                    salary: '',
                    location: '',
                    eligibility_criteria: '',
                    skills_required: '',
                    application_deadline: ''
                },
                error: '',
                loading: false
            }
        },
        methods: {
            async createDrive() {
                this.loading = true;
                this.error = '';
                
                // Validate deadline is set
                if (!this.form.application_deadline) {
                    this.error = 'Application deadline is required';
                    this.loading = false;
                    return;
                }
                
                // Convert datetime-local value to ISO 8601 format
                // datetime-local returns: "2024-03-15T10:30"
                // Backend expects: "2024-03-15T10:30:00" or "2024-03-15T10:30:00Z"
                const deadlineDate = new Date(this.form.application_deadline);
                
                if (isNaN(deadlineDate.getTime())) {
                    this.error = 'Invalid deadline date format';
                    this.loading = false;
                    return;
                }
                
                // Convert to ISO 8601 format with timezone
                const isoDeadline = deadlineDate.toISOString();
                
                // Prepare data for API
                const submitData = {
                    job_title: this.form.job_title,
                    job_description: this.form.job_description,
                    salary: this.form.salary,
                    location: this.form.location,
                    eligibility_criteria: this.form.eligibility_criteria,
                    skills_required: this.form.skills_required,
                    application_deadline: isoDeadline  // Send ISO format to backend
                };
                
                try {
                    const response = await companyAPI.createDrive(submitData);
                    alert(' Drive created successfully! Pending admin approval.');
                    this.$router.push('/company/drives');
                } catch (err) {
                    this.error = err.response?.data?.error || 'Failed to create drive';
                } finally {
                    this.loading = false;
                }
            }
        }
    }
},

    {
        path: '/company/drives/:driveId/applications',
        name: 'CompanyDriveApplications',
        meta: { 
            title: 'Drive Applications - Placement Portal V2',
            requiresAuth: true, 
            role: 'company' 
        },
        component: {
            template: `
                <div>
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h1>
                            <i class="bi bi-people"></i> Applications
                        </h1>
                        <button @click="$router.push('/company/drives')" class="btn btn-secondary">
                            <i class="bi bi-arrow-left"></i> Back
                        </button>
                    </div>
                    
                    <!-- Filter by Status -->
                    <div class="card mb-4 shadow-sm">
                        <div class="card-body">
                            <div class="row g-3">
                                <div class="col-md-4">
                                    <select class="form-select" v-model="status" @change="loadApplications" 
                                            :disabled="loading">
                                        <option value="">All Status</option>
                                        <option value="applied">Applied</option>
                                        <option value="shortlisted">Shortlisted</option>
                                        <option value="interview">Interview</option>
                                        <option value="selected">Selected</option>
                                        <option value="rejected">Rejected</option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <button @click="loadApplications" class="btn btn-primary w-100" 
                                            :disabled="loading">
                                        <i class="bi bi-search"></i> Filter
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Applications Table -->
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <div v-if="loading" class="text-center py-5">
                                <div class="spinner-border text-primary" role="status"></div>
                                <p class="mt-2">Loading applications...</p>
                            </div>
                            <table v-else class="table table-hover">
                                <thead class="table-light">
                                    <tr>
                                        <th>Student Name</th>
                                        <th>Roll Number</th>
                                        <th>Branch</th>
                                        <th>CGPA</th>
                                        <th>Status</th>
                                        <th>Applied Date</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="app in applications" :key="app.id">
                                        <td>{{ app.student_name }}</td>
                                        <td>{{ app.student_roll }}</td>
                                        <td>{{ app.student_branch }}</td>
                                        <td>{{ app.student_cgpa }}</td>
                                        <td>
                                            <span :class="getStatusBadge(app.status)">
                                                {{ app.status }}
                                            </span>
                                        </td>
                                        <td>{{ formatDate(app.application_date) }}</td>
                                        <td>
                                            <div class="btn-group btn-group-sm">
                                                <button @click="viewApplication(app.id)" 
                                                        class="btn btn-info" title="View Details">
                                                    <i class="bi bi-eye"></i>
                                                </button>
                                                <button @click="updateStatus(app.id)" 
                                                        class="btn btn-success" title="Update Status">
                                                    <i class="bi bi-pencil"></i>
                                                </button>
                                                <button @click="scheduleInterview(app.id)" 
                                                        class="btn btn-warning" title="Schedule Interview">
                                                    <i class="bi bi-calendar"></i>
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            `,
            data() {
                return {
                    applications: [],
                    loading: false,
                    status: '',
                    driveId: ''
                }
            },
            created() {
                this.driveId = this.$route.params.driveId;
                this.loadApplications();
            },
            methods: {
                async loadApplications() {
                    this.loading = true;
                    try {
                        const response = await companyAPI.getDriveApplications(this.driveId, {
                            status: this.status
                        });
                        this.applications = response.data.applications;
                    } catch (err) {
                        console.error('Error loading applications:', err);
                        alert('Failed to load applications');
                    } finally {
                        this.loading = false;
                    }
                },
                viewApplication: function(appId) {
                    this.$router.push('/company/applications/' + appId);
                },
                updateStatus: function(appId) {
                    this.$router.push('/company/applications/' + appId + '/update-status');
                },
                scheduleInterview: function(appId) {
                    var date = prompt('Enter interview date (YYYY-MM-DD HH:MM):');
                    if (!date) return;
                    this.$router.push('/company/applications/' + appId + '/schedule-interview?date=' + date);
                },
                formatDate: function(dateString) {
                    if (!dateString) return 'N/A';
                    return new Date(dateString).toLocaleDateString();
                },
                getStatusBadge: function(status) {
                    var badges = {
                        'applied': 'badge bg-primary',
                        'shortlisted': 'badge bg-warning text-dark',
                        'interview': 'badge bg-info',
                        'selected': 'badge bg-success',
                        'rejected': 'badge bg-danger'
                    };
                    return badges[status] || 'badge bg-secondary';
                }
            }
        }
    },
    
{
    path: '/company/applications/:applicationId',
    name: 'CompanyApplicationDetails',
    meta: { 
        title: 'Application Details - Placement Portal V2',
        requiresAuth: true, 
        role: 'company' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-file-earmark-text"></i> Application Details
                    </h1>
                    <button @click="$router.back()" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Back
                    </button>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading application details...</p>
                </div>
                
                <div v-else-if="error" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                    <button @click="loadApplication" class="btn btn-danger btn-sm ms-2">Retry</button>
                </div>
                
                <div v-else-if="application.id">
                    <!-- Student Information -->
                    <div class="card shadow-sm mb-4">
                        <div class="card-header bg-primary text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-person"></i> Student Information
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <p><strong>Name:</strong> {{ application.student.full_name }}</p>
                                    <p><strong>Roll Number:</strong> {{ application.student.roll_number }}</p>
                                    <p><strong>Branch:</strong> {{ application.student.branch }}</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>Email:</strong> {{ application.student.email }}</p>
                                    <p><strong>Phone:</strong> {{ application.student.phone }}</p>
                                    <p><strong>CGPA:</strong> {{ application.student.cgpa }}</p>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <p><strong>Skills:</strong> {{ application.student.skills }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Job Information -->
                    <div class="card shadow-sm mb-4">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-briefcase"></i> Job Information
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <p><strong>Job Title:</strong> {{ application.drive.job_title }}</p>
                                    <p><strong>Company:</strong> {{ application.drive.company_name }}</p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>Salary:</strong> ₹{{ application.drive.salary.toLocaleString() }}</p>
                                    <p><strong>Location:</strong> {{ application.drive.location }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Application Status -->
                    <div class="card shadow-sm mb-4">
                        <div class="card-header bg-info text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-clock-history"></i> Application Status
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <p><strong>Current Status:</strong></p>
                                    <span :class="getStatusBadge(application.status)" class="badge fs-6">
                                        {{ application.status }}
                                    </span>
                                </div>
                                <div class="col-md-4">
                                    <p><strong>Applied Date:</strong></p>
                                    <p>{{ formatDate(application.application_date) }}</p>
                                </div>
                                <div class="col-md-4">
                                    <p><strong>Interview Date:</strong></p>
                                    <p>{{ formatDate(application.interview_date) }}</p>
                                </div>
                            </div>
                            
                            <div v-if="application.feedback" class="mt-3">
                                <p><strong>Feedback:</strong></p>
                                <div class="alert alert-light border">
                                    {{ application.feedback }}
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Action Buttons -->
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-4">
                                    <button @click="updateStatus" class="btn btn-success w-100">
                                        <i class="bi bi-pencil"></i> Update Status
                                    </button>
                                </div>
                                <div class="col-md-4">
                                    <button @click="scheduleInterview" class="btn btn-warning w-100">
                                        <i class="bi bi-calendar"></i> Schedule Interview
                                    </button>
                                </div>
                                <div class="col-md-4">
                                    <button @click="$router.back()" class="btn btn-secondary w-100">
                                        <i class="bi bi-arrow-left"></i> Back
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                application: {},
                loading: false,
                error: '',
                applicationId: ''
            }
        },
        created() {
            this.applicationId = this.$route.params.applicationId;
            this.loadApplication();
        },
        methods: {
            async loadApplication() {
                this.loading = true;
                this.error = '';
                try {
                    const response = await companyAPI.getApplicationDetails(this.applicationId);
                    this.application = response.data;
                } catch (err) {
                    console.error('Load application details error:', err);
                    this.error = err.response?.data?.error || 'Failed to load application details';
                } finally {
                    this.loading = false;
                }
            },
            updateStatus() {
                this.$router.push('/company/applications/' + this.applicationId + '/update-status');
            },
            scheduleInterview() {
                this.$router.push('/company/applications/' + this.applicationId + '/schedule-interview');
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                const badges = {
                    'applied': 'badge bg-primary',
                    'shortlisted': 'badge bg-warning text-dark',
                    'interview': 'badge bg-info',
                    'selected': 'badge bg-success',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

    {
        path: '/company/applications/:applicationId/update-status',
        name: 'CompanyUpdateApplicationStatus',
        meta: { 
            title: 'Update Application Status - Placement Portal V2',
            requiresAuth: true, 
            role: 'company' 
        },
        component: {
            template: `
                <div>
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h1>
                            <i class="bi bi-pencil"></i> Update Application Status
                        </h1>
                        <button @click="$router.back()" class="btn btn-secondary">
                            <i class="bi bi-arrow-left"></i> Back
                        </button>
                    </div>
                    
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <div v-if="loading" class="text-center py-5">
                                <div class="spinner-border text-primary" role="status"></div>
                            </div>
                            <form v-else @submit.prevent="updateStatus">
                                <div class="mb-3">
                                    <label class="form-label">Student Name</label>
                                    <input type="text" class="form-control" :value="application.student_name" 
                                           disabled>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Current Status</label>
                                    <input type="text" class="form-control" :value="application.status" 
                                           disabled>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">New Status *</label>
                                    <select class="form-select" v-model="form.status" required 
                                            :disabled="loading">
                                        <option value="applied">Applied</option>
                                        <option value="shortlisted">Shortlisted</option>
                                        <option value="interview">Interview</option>
                                        <option value="selected">Selected</option>
                                        <option value="rejected">Rejected</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Feedback</label>
                                    <textarea class="form-control" v-model="form.feedback" rows="3" 
                                              placeholder="Add feedback for the student" 
                                              :disabled="loading"></textarea>
                                </div>
                                <div v-if="error" class="alert alert-danger">
                                    <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                                </div>
                                <button type="submit" class="btn btn-success" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                                    {{ loading ? 'Updating...' : 'Update Status' }}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            `,
            data() {
                return {
                    application: {},
                    form: {
                        status: '',
                        feedback: ''
                    },
                    error: '',
                    loading: false,
                    applicationId: ''
                }
            },
            created() {
                this.applicationId = this.$route.params.applicationId;
                this.loadApplication();
            },
            methods: {
                async loadApplication() {
                    this.loading = true;
                    try {
                        const response = await companyAPI.getApplicationDetails(this.applicationId);
                        this.application = response.data;
                        this.form.status = response.data.status;
                        this.form.feedback = response.data.feedback || '';
                    } catch (err) {
                        this.error = 'Failed to load application';
                    } finally {
                        this.loading = false;
                    }
                },
                async updateStatus() {
                    this.loading = true;
                    this.error = '';
                    try {
                        await companyAPI.updateApplicationStatus(this.applicationId, this.form);
                        alert(' Application status updated successfully');
                        this.$router.back();
                    } catch (err) {
                        this.error = err.response?.data?.error || 'Failed to update status';
                    } finally {
                        this.loading = false;
                    }
                }
            }
        }
    },
    
    {
        path: '/company/applications/:applicationId/schedule-interview',
        name: 'CompanyScheduleInterview',
        meta: { 
            title: 'Schedule Interview - Placement Portal V2',
            requiresAuth: true, 
            role: 'company' 
        },
        component: {
            template: `
                <div>
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h1>
                            <i class="bi bi-calendar"></i> Schedule Interview
                        </h1>
                        <button @click="$router.back()" class="btn btn-secondary">
                            <i class="bi bi-arrow-left"></i> Back
                        </button>
                    </div>
                    
                    <div class="card shadow-sm">
                        <div class="card-body">
                            <div v-if="loading" class="text-center py-5">
                                <div class="spinner-border text-primary" role="status"></div>
                            </div>
                            <form v-else @submit.prevent="scheduleInterview">
                                <div class="mb-3">
                                    <label class="form-label">Student Name</label>
                                    <input type="text" class="form-control" :value="application.student_name" 
                                           disabled>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Interview Date & Time *</label>
                                    <input type="datetime-local" class="form-control" v-model="form.interview_date" 
                                           required :disabled="loading">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Interview Type</label>
                                    <select class="form-select" v-model="form.interview_type" :disabled="loading">
                                        <option value="In-Person">In-Person</option>
                                        <option value="Video Call">Video Call</option>
                                        <option value="Phone">Phone</option>
                                        <option value="Online Test">Online Test</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Interview Location</label>
                                    <input type="text" class="form-control" v-model="form.interview_location" 
                                           placeholder="e.g., Conference Room A or Zoom Link" :disabled="loading">
                                </div>
                                <div v-if="error" class="alert alert-danger">
                                    <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                                </div>
                                <button type="submit" class="btn btn-warning" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                                    {{ loading ? 'Scheduling...' : 'Schedule Interview' }}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            `,
            data() {
                return {
                    application: {},
                    form: {
                        interview_date: '',
                        interview_type: 'In-Person',
                        interview_location: ''
                    },
                    error: '',
                    loading: false,
                    applicationId: ''
                }
            },
            created() {
                this.applicationId = this.$route.params.applicationId;
                this.loadApplication();
                
                // Pre-fill date from query param if available
                const dateParam = this.$route.query.date;
                if (dateParam) {
                    this.form.interview_date = dateParam;
                }
            },
            methods: {
                async loadApplication() {
                    this.loading = true;
                    try {
                        const response = await companyAPI.getApplicationDetails(this.applicationId);
                        this.application = response.data;
                    } catch (err) {
                        this.error = 'Failed to load application';
                    } finally {
                        this.loading = false;
                    }
                },
                async scheduleInterview() {
                    this.loading = true;
                    this.error = '';
                    try {
                        await companyAPI.scheduleInterview(this.applicationId, this.form);
                        alert(' Interview scheduled successfully');
                        this.$router.back();
                    } catch (err) {
                        this.error = err.response?.data?.error || 'Failed to schedule interview';
                    } finally {
                        this.loading = false;
                    }
                }
            }
        }
    },

{
    path: '/company/applications/:applicationId/schedule-interview',
    name: 'CompanyScheduleInterview',
    meta: { 
        title: 'Schedule Interview - Placement Portal V2',
        requiresAuth: true, 
        role: 'company' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-calendar"></i> Schedule Interview
                    </h1>
                    <button @click="$router.back()" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Back
                    </button>
                </div>
                
                <div class="card shadow-sm">
                    <div class="card-body">
                        <div v-if="loading" class="text-center py-5">
                            <div class="spinner-border text-primary" role="status"></div>
                        </div>
                        <form v-else @submit.prevent="scheduleInterview">
                            <div class="mb-3">
                                <label class="form-label">Student Name</label>
                                <input type="text" class="form-control" :value="application.student_name" disabled>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Interview Date & Time *</label>
                                <input type="datetime-local" class="form-control" v-model="form.interview_date" 
                                       required :disabled="loading">
                                <small class="text-muted">Select date and time for the interview</small>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Interview Type</label>
                                <select class="form-select" v-model="form.interview_type" :disabled="loading">
                                    <option value="In-Person">In-Person</option>
                                    <option value="Video Call">Video Call</option>
                                    <option value="Phone">Phone</option>
                                    <option value="Online Test">Online Test</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Interview Location</label>
                                <input type="text" class="form-control" v-model="form.interview_location" 
                                       placeholder="e.g., Conference Room A or Zoom Link" :disabled="loading">
                            </div>
                            <div v-if="error" class="alert alert-danger">
                                <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                            </div>
                            <button type="submit" class="btn btn-warning" :disabled="loading">
                                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                                {{ loading ? 'Scheduling...' : 'Schedule Interview' }}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                application: {},
                form: {
                    interview_date: '',
                    interview_type: 'In-Person',
                    interview_location: ''
                },
                error: '',
                loading: false,
                applicationId: ''
            }
        },
        created() {
            this.applicationId = this.$route.params.applicationId;
            this.loadApplication();
            
            // Pre-fill date from query param if available
            const dateParam = this.$route.query.date;
            if (dateParam) {
                // Convert to datetime-local format (YYYY-MM-DDTHH:MM)
                const date = new Date(dateParam);
                const year = date.getFullYear();
                const month = String(date.getMonth() + 1).padStart(2, '0');
                const day = String(date.getDate()).padStart(2, '0');
                const hours = String(date.getHours()).padStart(2, '0');
                const minutes = String(date.getMinutes()).padStart(2, '0');
                this.form.interview_date = `${year}-${month}-${day}T${hours}:${minutes}`;
            }
        },
        methods: {
            async loadApplication() {
                this.loading = true;
                try {
                    const response = await companyAPI.getApplicationDetails(this.applicationId);
                    this.application = response.data;
                } catch (err) {
                    this.error = 'Failed to load application';
                } finally {
                    this.loading = false;
                }
            },
            async scheduleInterview() {
                this.loading = true;
                this.error = '';
                
                try {
                    // FIX: Convert datetime-local value to ISO 8601 format with timezone
                    const interviewDateLocal = this.form.interview_date;
                    
                    if (!interviewDateLocal) {
                        this.error = 'Interview date is required';
                        this.loading = false;
                        return;
                    }
                    
                    // Create Date object from datetime-local value
                    const interviewDate = new Date(interviewDateLocal);
                    
                    // Check if date is valid
                    if (isNaN(interviewDate.getTime())) {
                        this.error = 'Invalid interview date format';
                        this.loading = false;
                        return;
                    }
                    
                    // Check if date is in the future
                    const now = new Date();
                    if (interviewDate <= now) {
                        this.error = 'Interview date must be in the future';
                        this.loading = false;
                        return;
                    }
                    
                    // Convert to ISO 8601 format with timezone
                    const interviewDateISO = interviewDate.toISOString();
                    
                    // Prepare data for API
                    const submitData = {
                        interview_date: interviewDateISO,
                        interview_type: this.form.interview_type,
                        interview_location: this.form.interview_location
                    };
                    
                    await companyAPI.scheduleInterview(this.applicationId, submitData);
                    alert(' Interview scheduled successfully');
                    this.$router.back();
                } catch (err) {
                    console.error('Schedule interview error:', err);
                    this.error = err.response?.data?.error || 'Failed to schedule interview';
                } finally {
                    this.loading = false;
                }
            }
        }
    }
},
    
    {
    path: '/company/profile',
    name: 'CompanyProfile',
    meta: { 
        title: 'Company Profile - Placement Portal V2',
        requiresAuth: true, 
        role: 'company' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-person"></i> Company Profile
                    </h1>
                    <button @click="loadProfile" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <div v-if="error" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                </div>
                
                <div v-if="success" class="alert alert-success">
                    <i class="bi bi-check-circle-fill"></i> {{ success }}
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading profile...</p>
                </div>
                
                <div v-else-if="profile.id">
                    <div class="card shadow-sm">
                        <div class="card-header bg-primary text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-building"></i> {{ profile.company_name }}
                            </h5>
                        </div>
                        <div class="card-body">
                            <form @submit.prevent="updateProfile">
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Company Name *</label>
                                        <input type="text" class="form-control" v-model="profile.company_name" required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Industry *</label>
                                        <input type="text" class="form-control" v-model="profile.industry" required>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Location</label>
                                        <input type="text" class="form-control" v-model="profile.location">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Website</label>
                                        <input type="url" class="form-control" v-model="profile.website">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">HR Contact Name</label>
                                        <input type="text" class="form-control" v-model="profile.hr_contact_name">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">HR Contact Email</label>
                                        <input type="email" class="form-control" v-model="profile.hr_contact_email">
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">HR Contact Phone</label>
                                    <input type="tel" class="form-control" v-model="profile.hr_contact_phone">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Company Description</label>
                                    <textarea class="form-control" v-model="profile.company_description" rows="4"></textarea>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Approval Status</label>
                                    <input type="text" class="form-control" :value="profile.approval_status" disabled>
                                </div>
                                
                                <div v-if="updateError" class="alert alert-danger">
                                    <i class="bi bi-exclamation-triangle-fill"></i> {{ updateError }}
                                </div>
                                
                                <button type="submit" class="btn btn-success" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                                    {{ loading ? 'Updating...' : 'Update Profile' }}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                profile: {},
                loading: false,
                error: '',
                success: '',
                updateError: ''
            }
        },
        created() {
            this.loadProfile();
        },
        methods: {
            async loadProfile() {
                this.loading = true;
                this.error = '';
                try {
                    const response = await companyAPI.getProfile();
                    this.profile = response.data;
                } catch (err) {
                    this.error = err.response?.data?.error || 'Failed to load profile';
                } finally {
                    this.loading = false;
                }
            },
            async updateProfile() {
                this.loading = true;
                this.updateError = '';
                this.success = '';
                try {
                    const updateData = {
                        company_name: this.profile.company_name,
                        industry: this.profile.industry,
                        location: this.profile.location,
                        website: this.profile.website,
                        hr_contact_name: this.profile.hr_contact_name,
                        hr_contact_email: this.profile.hr_contact_email,
                        hr_contact_phone: this.profile.hr_contact_phone,
                        company_description: this.profile.company_description
                    };
                    await companyAPI.updateProfile(updateData);
                    this.success = ' Profile updated successfully';
                    setTimeout(() => {
                        this.success = '';
                    }, 3000);
                } catch (err) {
                    this.updateError = err.response?.data?.error || 'Failed to update profile';
                } finally {
                    this.loading = false;
                }
            }
        }
    }
},

{
    path: '/company/placements',
    name: 'CompanyPlacements',
    meta: { 
        title: 'Placements - Placement Portal V2',
        requiresAuth: true, 
        role: 'company' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-file-earmark-check"></i> Placements
                    </h1>
                    <div>
                        <button @click="exportPlacements" class="btn btn-success me-2" :disabled="exporting">
                            <i class="bi bi-file-earmark-spreadsheet"></i> 
                            {{ exporting ? 'Exporting...' : 'Export Placements CSV' }}
                        </button>
                        <button @click="loadPlacements" class="btn btn-primary" :disabled="loading">
                            <i class="bi bi-arrow-clockwise"></i> Refresh
                        </button>
                    </div>
                </div>
                
                <div v-if="exportSuccess" class="alert alert-success">
                    <i class="bi bi-check-circle-fill"></i> {{ exportSuccess }}
                </div>
                
                <div v-if="exportError" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill"></i> {{ exportError }}
                </div>
                
                <p class="text-muted">View placement records and export to CSV</p>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading placements...</p>
                </div>
                
                <div v-else-if="placements.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No placement records found</p>
                    <p class="text-muted">Placements will appear here when you select students</p>
                </div>
                
                <div v-else class="card shadow-sm">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-check-circle"></i> Total Placements: {{ total }}
                        </h5>
                    </div>
                    <div class="card-body">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Student Name</th>
                                    <th>Roll Number</th>
                                    <th>Branch</th>
                                    <th>Position</th>
                                    <th>Salary</th>
                                    <th>Placement Date</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="placement in placements" :key="placement.id">
                                    <td>{{ placement.student_name }}</td>
                                    <td>{{ placement.student_roll }}</td>
                                    <td>{{ placement.student_branch }}</td>
                                    <td>{{ placement.position }}</td>
                                    <td>₹{{ placement.salary.toLocaleString() }}</td>
                                    <td>{{ formatDate(placement.placement_date) }}</td>
                                    <td>
                                        <span :class="getPlacementBadge(placement.status)">
                                            {{ placement.status }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                placements: [],
                loading: false,
                exporting: false,
                exportSuccess: '',
                exportError: '',
                total: 0,
                currentPage: 1,
                totalPages: 1
            }
        },
        created() {
            this.loadPlacements();
        },
        methods: {
            async loadPlacements() {
                this.loading = true;
                try {
                    const response = await companyAPI.getPlacements({
                        page: this.currentPage
                    });
                    this.placements = response.data.placements;
                    this.total = response.data.total;
                    this.totalPages = response.data.pages;
                } catch (err) {
                    console.error('Error loading placements:', err);
                    this.exportError = 'Failed to load placements';
                } finally {
                    this.loading = false;
                }
            },
            async exportPlacements() {
                this.exporting = true;
                this.exportSuccess = '';
                this.exportError = '';
                try {
                    const response = await companyAPI.exportPlacements();
                    this.exportSuccess = '✅ ' + response.data.message;
                    setTimeout(() => {
                        this.exportSuccess = '';
                    }, 5000);
                } catch (err) {
                    console.error('Export placements error:', err);
                    this.exportError = err.response?.data?.error || 'Failed to export placements';
                } finally {
                    this.exporting = false;
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getPlacementBadge(status) {
                const badges = {
                    'offered': 'badge bg-success',
                    'joined': 'badge bg-primary',
                    'declined': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

// Company Applications Route
{
    path: '/company/applications',
    name: 'CompanyApplications',
    meta: { 
        title: 'All Applications - Placement Portal V2',
        requiresAuth: true, 
        role: 'company' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1><i class="bi bi-people"></i> All Applications</h1>
                    <button @click="loadApplications" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <div v-if="error" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                    <button @click="loadApplications" class="btn btn-danger btn-sm ms-2">Retry</button>
                </div>
                
                <div class="card mb-4 shadow-sm">
                    <div class="card-body">
                        <div class="row g-3">
                            <div class="col-md-4">
                                <select class="form-select" v-model="status" @change="loadApplications" :disabled="loading">
                                    <option value="">All Status</option>
                                    <option value="applied">Applied</option>
                                    <option value="shortlisted">Shortlisted</option>
                                    <option value="interview">Interview</option>
                                    <option value="selected">Selected</option>
                                    <option value="rejected">Rejected</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <button @click="loadApplications" class="btn btn-primary w-100" :disabled="loading">
                                    <i class="bi bi-search"></i> Filter
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading applications...</p>
                </div>
                
                <div v-else-if="applications.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No applications found</p>
                    <p class="text-muted">Applications will appear here when students apply to your drives</p>
                    <router-link to="/company/drives/create" class="btn btn-success mt-2">
                        <i class="bi bi-plus-lg"></i> Create a Drive
                    </router-link>
                </div>
                
                <div v-else class="card shadow-sm">
                    <div class="card-body">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Student Name</th>
                                    <th>Roll Number</th>
                                    <th>Branch</th>
                                    <th>Job Title</th>
                                    <th>Status</th>
                                    <th>Applied Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="app in applications" :key="app.id">
                                    <td>{{ app.student_name }}</td>
                                    <td>{{ app.student_roll }}</td>
                                    <td>{{ app.student_branch }}</td>
                                    <td>{{ app.drive_title }}</td>
                                    <td>
                                        <span :class="getStatusBadge(app.status)">
                                            {{ app.status }}
                                        </span>
                                    </td>
                                    <td>{{ formatDate(app.application_date) }}</td>
                                    <td>
                                        <div class="btn-group btn-group-sm">
                                            <button @click="viewApplication(app.id)" class="btn btn-info" title="View Details">
                                                <i class="bi bi-eye"></i>
                                            </button>
                                            <button @click="updateStatus(app.id)" class="btn btn-success" title="Update Status">
                                                <i class="bi bi-pencil"></i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                applications: [],
                loading: false,
                error: '',
                status: '',
                currentPage: 1,
                totalPages: 1
            }
        },
        created() {
            this.loadApplications();
        },
        methods: {
            async loadApplications() {
                this.loading = true;
                this.error = '';
                try {
                    const response = await companyAPI.getApplications({
                        page: this.currentPage,
                        status: this.status
                    });
                    this.applications = response.data.applications;
                    this.totalPages = response.data.pages;
                } catch (err) {
                    console.error('Error loading applications:', err);
                    this.error = err.response?.data?.error || 'Failed to load applications';
                } finally {
                    this.loading = false;
                }
            },
            viewApplication(appId) {
                this.$router.push('/company/applications/' + appId);
            },
            updateStatus(appId) {
                this.$router.push('/company/applications/' + appId + '/update-status');
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                const badges = {
                    'applied': 'badge bg-primary',
                    'shortlisted': 'badge bg-warning text-dark',
                    'interview': 'badge bg-info',
                    'selected': 'badge bg-success',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

{
    path: '/student/applications',
    name: 'StudentApplications',
    meta: { 
        title: 'My Applications - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-file-earmark-text"></i> My Applications
                    </h1>
                    <button @click="loadApplications" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <!-- Filter by Status -->
                <div class="card mb-4 shadow-sm">
                    <div class="card-body">
                        <div class="row g-3">
                            <div class="col-md-4">
                                <select class="form-select" v-model="status" @change="loadApplications" 
                                        :disabled="loading">
                                    <option value="">All Status</option>
                                    <option value="applied">Applied</option>
                                    <option value="shortlisted">Shortlisted</option>
                                    <option value="interview">Interview</option>
                                    <option value="selected">Selected</option>
                                    <option value="rejected">Rejected</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <button @click="loadApplications" class="btn btn-primary w-100" 
                                        :disabled="loading">
                                    <i class="bi bi-search"></i> Filter
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading applications...</p>
                </div>
                
                <div v-else-if="applications.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No applications found</p>
                </div>
                
                <div v-else class="card shadow-sm">
                    <div class="card-body">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Job Title</th>
                                    <th>Company</th>
                                    <th>Location</th>
                                    <th>Status</th>
                                    <th>Applied Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="app in applications" :key="app.id">
                                    <td>{{ app.job_title }}</td>
                                    <td>{{ app.company_name }}</td>
                                    <td>{{ app.location }}</td>
                                    <td>
                                        <span :class="getStatusBadge(app.status)">
                                            {{ app.status }}
                                        </span>
                                    </td>
                                    <td>{{ formatDate(app.application_date) }}</td>
                                    <td>
                                        <button @click="viewApplication(app.id)" class="btn btn-info btn-sm">
                                            <i class="bi bi-eye"></i> View
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                applications: [],
                loading: false,
                status: '',
                currentPage: 1,
                totalPages: 1
            }
        },
        created() {
            this.loadApplications();
        },
        methods: {
            async loadApplications() {
                this.loading = true;
                try {
                    const response = await studentAPI.getApplications({
                        page: this.currentPage,
                        status: this.status
                    });
                    this.applications = response.data.applications;
                    this.totalPages = response.data.pages;
                } catch (err) {
                    console.error('Error loading applications:', err);
                    alert('Failed to load applications');
                } finally {
                    this.loading = false;
                }
            },
            viewApplication(appId) {
                this.$router.push('/student/applications/' + appId);
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                var badges = {
                    'applied': 'badge bg-primary',
                    'shortlisted': 'badge bg-warning text-dark',
                    'interview': 'badge bg-info',
                    'selected': 'badge bg-success',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

{
    path: '/student/drives',
    name: 'StudentDrives',
    meta: { 
        title: 'Browse Jobs - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1><i class="bi bi-briefcase"></i> Browse Job Postings</h1>
                    <button @click="loadDrives" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <div class="card mb-4 shadow-sm">
                    <div class="card-body">
                        <div class="row g-3">
                            <div class="col-md-4">
                                <input type="text" class="form-control" v-model="search" 
                                       placeholder="Search by job title or company..." 
                                       @keyup.enter="loadDrives" :disabled="loading">
                            </div>
                            <div class="col-md-3">
                                <input type="text" class="form-control" v-model="skills" 
                                       placeholder="Filter by skills..." 
                                       @keyup.enter="loadDrives" :disabled="loading">
                            </div>
                            <div class="col-md-3">
                                <button @click="loadDrives" class="btn btn-primary w-100" :disabled="loading">
                                    <i class="bi bi-search"></i> Search
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading job postings...</p>
                </div>
                
                <div v-else-if="drives.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No job postings found</p>
                </div>
                
                <div v-else class="row g-4">
                    <div class="col-md-6" v-for="drive in drives" :key="drive.id">
                        <div class="card h-100 shadow-sm">
                            <div class="card-body">
                                <h5 class="card-title">{{ drive.job_title }}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">{{ drive.company_name }}</h6>
                                <p class="card-text">
                                    <i class="bi bi-geo-alt"></i> {{ drive.location }} | 
                                    <i class="bi bi-currency-rupee"></i> {{ drive.salary.toLocaleString() }}
                                </p>
                                <p class="card-text">
                                    <small class="text-muted">
                                        <i class="bi bi-calendar"></i> Deadline: {{ formatDate(drive.application_deadline) }}
                                    </small>
                                    <span v-if="drive.is_expired" class="badge bg-danger ms-2">Expired</span>
                                </p>
                                <div class="mb-2">
                                    <span class="badge bg-info">{{ drive.skills_required }}</span>
                                </div>
                            </div>
                            <div class="card-footer bg-white">
                                <div class="d-flex justify-content-between">
                                    <button @click="viewDriveDetails(drive.id)" class="btn btn-outline-info btn-sm">
                                        <i class="bi bi-eye"></i> View Details
                                    </button>
                                    <button v-if="!drive.already_applied && !drive.is_expired" 
                                            @click="applyToDrive(drive.id)" 
                                            class="btn btn-success btn-sm"
                                            :disabled="loading">
                                        <i class="bi bi-plus-lg"></i> Apply
                                    </button>
                                    <span v-else-if="drive.already_applied" class="badge" :class="getStatusBadge(drive.application_status)">
                                        {{ drive.application_status }}
                                    </span>
                                    <span v-else class="badge bg-danger">Expired</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                drives: [],
                loading: false,
                search: '',
                skills: '',
                currentPage: 1,
                totalPages: 1
            }
        },
        created() {
            this.loadDrives();
        },
        // ADD THIS HOOK - Fixes back button loading issue
        beforeRouteUpdate(to, from, next) {
            this.loadDrives();
            next();
        },
        // ADD THIS HOOK - Fixes back button loading issue (alternative)
        activated() {
            this.loadDrives();
        },
        methods: {
            async loadDrives() {
                this.loading = true;
                try {
                    const response = await studentAPI.getDrives({
                        page: this.currentPage,
                        search: this.search,
                        skills: this.skills
                    });
                    this.drives = response.data.drives;
                    this.totalPages = response.data.pages;
                } catch (err) {
                    console.error('Error loading drives:', err);
                    alert('Failed to load job postings: ' + (err.response?.data?.error || 'Unknown error'));
                } finally {
                    this.loading = false;
                }
            },
            async applyToDrive(driveId) {
                if (!confirm('Are you sure you want to apply to this drive?')) return;
                try {
                    await studentAPI.applyToDrive(driveId);
                    alert(' Application submitted successfully!');
                    this.loadDrives();
                } catch (err) {
                    console.error('Apply error:', err);
                    alert('Failed to apply: ' + (err.response?.data?.error || 'Unknown error'));
                }
            },
            viewDriveDetails(driveId) {
                this.$router.push('/student/drives/' + driveId);
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                var badges = {
                    'applied': 'badge bg-primary',
                    'shortlisted': 'badge bg-warning text-dark',
                    'interview': 'badge bg-info',
                    'selected': 'badge bg-success',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

{
    path: '/student/drives/:driveId',
    name: 'StudentDriveDetails',
    meta: { 
        title: 'Drive Details - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1><i class="bi bi-briefcase"></i> Job Details</h1>
                    <button @click="$router.push('/student/drives')" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Back
                    </button>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading drive details...</p>
                </div>
                
                <div v-else-if="error" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                    <button @click="loadDriveDetails" class="btn btn-danger btn-sm ms-2">Retry</button>
                </div>
                
                <div v-else-if="drive.id">
                    <div class="card shadow-sm">
                        <div class="card-header bg-primary text-white">
                            <h4 class="mb-0">{{ drive.job_title }}</h4>
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">{{ drive.company.name }}</h5>
                            <p class="card-text">
                                <i class="bi bi-geo-alt"></i> {{ drive.location }} | 
                                <i class="bi bi-currency-rupee"></i> {{ drive.salary.toLocaleString() }}
                            </p>
                            <hr>
                            <h6>Job Description:</h6>
                            <p>{{ drive.job_description }}</p>
                            <h6>Eligibility Criteria:</h6>
                            <p>{{ drive.eligibility_criteria }}</p>
                            <h6>Skills Required:</h6>
                            <p>{{ drive.skills_required }}</p>
                            <p class="text-muted">
                                <i class="bi bi-calendar"></i> Application Deadline: {{ formatDate(drive.application_deadline) }}
                            </p>
                            
                            <div v-if="drive.is_expired" class="alert alert-danger">
                                <i class="bi bi-exclamation-triangle-fill"></i> 
                                Application deadline has passed
                            </div>
                            
                            <div v-else-if="drive.already_applied" class="alert alert-info">
                                <i class="bi bi-info-circle-fill"></i> 
                                You have already applied to this drive. Status: {{ drive.application_status }}
                            </div>
                            
                            <button v-if="!drive.already_applied && !drive.is_expired" 
                                    @click="applyToDrive" 
                                    class="btn btn-success btn-lg"
                                    :disabled="loading">
                                <i class="bi bi-plus-lg"></i> Apply Now
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                drive: {},
                loading: false,
                error: '',
                driveId: ''
            }
        },
        created() {
            this.driveId = this.$route.params.driveId;
            this.loadDriveDetails();
        },
        methods: {
            async loadDriveDetails() {
                this.loading = true;
                this.error = '';
                try {
                    const response = await studentAPI.getDriveDetails(this.driveId);
                    this.drive = response.data;
                } catch (err) {
                    console.error('Load drive details error:', err);
                    this.error = err.response?.data?.error || 'Failed to load drive details';
                } finally {
                    this.loading = false;
                }
            },
            async applyToDrive() {
                if (!confirm('Are you sure you want to apply to this drive?')) return;
                try {
                    await studentAPI.applyToDrive(this.driveId);
                    alert(' Application submitted successfully!');
                    this.loadDriveDetails();
                } catch (err) {
                    console.error('Apply error:', err);
                    alert('Failed to apply: ' + (err.response?.data?.error || 'Unknown error'));
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            }
        }
    }
},

{
    path: '/student/applications',
    name: 'StudentApplications',
    meta: { 
        title: 'My Applications - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1><i class="bi bi-file-earmark-text"></i> My Applications</h1>
                    <button @click="loadApplications" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <div class="card mb-4 shadow-sm">
                    <div class="card-body">
                        <div class="row g-3">
                            <div class="col-md-4">
                                <select class="form-select" v-model="status" @change="loadApplications" :disabled="loading">
                                    <option value="">All Status</option>
                                    <option value="applied">Applied</option>
                                    <option value="shortlisted">Shortlisted</option>
                                    <option value="interview">Interview</option>
                                    <option value="selected">Selected</option>
                                    <option value="rejected">Rejected</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <button @click="loadApplications" class="btn btn-primary w-100" :disabled="loading">
                                    <i class="bi bi-search"></i> Filter
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading applications...</p>
                </div>
                
                <div v-else-if="applications.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No applications found</p>
                </div>
                
                <div v-else class="card shadow-sm">
                    <div class="card-body">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Job Title</th>
                                    <th>Company</th>
                                    <th>Location</th>
                                    <th>Status</th>
                                    <th>Applied Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="app in applications" :key="app.id">
                                    <td>{{ app.job_title }}</td>
                                    <td>{{ app.company_name }}</td>
                                    <td>{{ app.location }}</td>
                                    <td>
                                        <span :class="getStatusBadge(app.status)">
                                            {{ app.status }}
                                        </span>
                                    </td>
                                    <td>{{ formatDate(app.application_date) }}</td>
                                    <td>
                                        <button @click="viewApplication(app.id)" class="btn btn-info btn-sm">
                                            <i class="bi bi-eye"></i> View
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                applications: [],
                loading: false,
                status: '',
                currentPage: 1,
                totalPages: 1
            }
        },
        created() {
            this.loadApplications();
        },
        methods: {
            async loadApplications() {
                this.loading = true;
                try {
                    const response = await studentAPI.getApplications({
                        page: this.currentPage,
                        status: this.status
                    });
                    this.applications = response.data.applications;
                    this.totalPages = response.data.pages;
                } catch (err) {
                    console.error('Error loading applications:', err);
                    alert('Failed to load applications');
                } finally {
                    this.loading = false;
                }
            },
            viewApplication(appId) {
                this.$router.push('/student/applications/' + appId);
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                var badges = {
                    'applied': 'badge bg-primary',
                    'shortlisted': 'badge bg-warning text-dark',
                    'interview': 'badge bg-info',
                    'selected': 'badge bg-success',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

{
    path: '/student/applications/:applicationId',
    name: 'StudentApplicationDetails',
    meta: { 
        title: 'Application Details - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1><i class="bi bi-file-earmark-text"></i> Application Details</h1>
                    <button @click="$router.back()" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Back
                    </button>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                </div>
                
                <div v-else-if="application.id">
                    <div class="card shadow-sm">
                        <div class="card-header bg-info text-white">
                            <h4 class="mb-0">{{ application.drive.job_title }}</h4>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <h5>Company</h5>
                                    <p>{{ application.company.name }}</p>
                                    <p><i class="bi bi-geo-alt"></i> {{ application.drive.location }}</p>
                                    <p><i class="bi bi-currency-rupee"></i> {{ application.drive.salary.toLocaleString() }}</p>
                                </div>
                                <div class="col-md-6">
                                    <h5>Application Status</h5>
                                    <p>
                                        <span :class="getStatusBadge(application.status)" class="badge fs-6">
                                            {{ application.status }}
                                        </span>
                                    </p>
                                    <p><i class="bi bi-calendar"></i> Applied: {{ formatDate(application.application_date) }}</p>
                                    <p v-if="application.interview_date">
                                        <i class="bi bi-calendar-check"></i> Interview: {{ formatDate(application.interview_date) }}
                                    </p>
                                </div>
                            </div>
                            <hr>
                            <div v-if="application.feedback">
                                <h5>Feedback from Company:</h5>
                                <div class="alert alert-light border">
                                    {{ application.feedback }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                application: {},
                loading: false,
                applicationId: ''
            }
        },
        created() {
            this.applicationId = this.$route.params.applicationId;
            this.loadApplication();
        },
        methods: {
            async loadApplication() {
                this.loading = true;
                try {
                    const response = await studentAPI.getApplicationDetails(this.applicationId);
                    this.application = response.data;
                } catch (err) {
                    alert(err.response?.data?.error || 'Failed to load application details');
                } finally {
                    this.loading = false;
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                var badges = {
                    'applied': 'badge bg-primary',
                    'shortlisted': 'badge bg-warning text-dark',
                    'interview': 'badge bg-info',
                    'selected': 'badge bg-success',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

{
    path: '/student/profile',
    name: 'StudentProfile',
    meta: { 
        title: 'Student Profile - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-person"></i> Student Profile
                    </h1>
                    <button @click="loadProfile" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <div v-if="error" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                </div>
                
                <div v-if="success" class="alert alert-success">
                    <i class="bi bi-check-circle-fill"></i> {{ success }}
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading profile...</p>
                </div>
                
                <div v-else-if="profile.id">
                    <div class="card shadow-sm">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-person"></i> {{ profile.full_name }}
                            </h5>
                        </div>
                        <div class="card-body">
                            <form @submit.prevent="updateProfile">
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Roll Number</label>
                                        <input type="text" class="form-control" :value="profile.roll_number" disabled>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Branch</label>
                                        <input type="text" class="form-control" :value="profile.branch" disabled>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">CGPA</label>
                                        <input type="text" class="form-control" :value="profile.cgpa" disabled>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Email</label>
                                        <input type="email" class="form-control" :value="profile.email" disabled>
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Phone</label>
                                    <input type="tel" class="form-control" v-model="profile.phone">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Skills (comma-separated)</label>
                                    <textarea class="form-control" v-model="profile.skills" rows="2"></textarea>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Education Details</label>
                                    <textarea class="form-control" v-model="profile.education_details" rows="3"></textarea>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Experience Details</label>
                                    <textarea class="form-control" v-model="profile.experience_details" rows="3"></textarea>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Resume</label>
                                    <input type="file" class="form-control" @change="handleResumeUpload" accept=".pdf,.doc,.docx">
                                    <small class="text-muted" v-if="profile.resume_path">Current: {{ profile.resume_path }}</small>
                                </div>
                                
                                <div v-if="updateError" class="alert alert-danger">
                                    <i class="bi bi-exclamation-triangle-fill"></i> {{ updateError }}
                                </div>
                                
                                <button type="submit" class="btn btn-success" :disabled="loading">
                                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                                    {{ loading ? 'Updating...' : 'Update Profile' }}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                profile: {},
                loading: false,
                error: '',
                success: '',
                updateError: ''
            }
        },
        created() {
            this.loadProfile();
        },
        methods: {
            async loadProfile() {
                this.loading = true;
                this.error = '';
                try {
                    const response = await studentAPI.getProfile();
                    this.profile = response.data;
                } catch (err) {
                    this.error = err.response?.data?.error || 'Failed to load profile';
                } finally {
                    this.loading = false;
                }
            },
            async updateProfile() {
                this.loading = true;
                this.updateError = '';
                this.success = '';
                try {
                    const updateData = {
                        phone: this.profile.phone,
                        skills: this.profile.skills,
                        education_details: this.profile.education_details,
                        experience_details: this.profile.experience_details
                    };
                    await studentAPI.updateProfile(updateData);
                    this.success = ' Profile updated successfully';
                    setTimeout(() => {
                        this.success = '';
                    }, 3000);
                } catch (err) {
                    this.updateError = err.response?.data?.error || 'Failed to update profile';
                } finally {
                    this.loading = false;
                }
            },
            async handleResumeUpload(event) {
                const file = event.target.files[0];
                if (!file) return;
                
                this.loading = true;
                this.updateError = '';
                
                const formData = new FormData();
                formData.append('resume', file);
                
                try {
                    await studentAPI.uploadResume(formData);
                    this.success = ' Resume uploaded successfully';
                    this.loadProfile();
                } catch (err) {
                    this.updateError = err.response?.data?.error || 'Failed to upload resume';
                } finally {
                    this.loading = false;
                }
            }
        }
    }
},

{
    path: '/student/interviews',
    name: 'StudentInterviews',
    meta: { 
        title: 'Interview Schedules - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-calendar"></i> Interview Schedules
                    </h1>
                    <button @click="loadInterviews" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading interviews...</p>
                </div>
                
                <div v-else-if="interviews.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No scheduled interviews</p>
                </div>
                
                <div v-else class="row g-4">
                    <div class="col-md-6" v-for="interview in interviews" :key="interview.application_id">
                        <div class="card shadow-sm">
                            <div class="card-body">
                                <h5 class="card-title">{{ interview.job_title }}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">{{ interview.company_name }}</h6>
                                <p class="card-text">
                                    <i class="bi bi-calendar"></i> 
                                    {{ formatDate(interview.interview_date) }}
                                </p>
                                <p class="card-text" v-if="interview.feedback">
                                    <i class="bi bi-chat-left-text"></i> 
                                    <strong>Feedback:</strong> {{ interview.feedback }}
                                </p>
                            </div>
                            <div class="card-footer bg-white">
                                <span class="badge bg-info">{{ interview.status }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                interviews: [],
                loading: false
            }
        },
        created() {
            this.loadInterviews();
        },
        methods: {
            async loadInterviews() {
                this.loading = true;
                try {
                    const response = await studentAPI.getInterviews();
                    this.interviews = response.data.interviews;
                } catch (err) {
                    console.error('Error loading interviews:', err);
                    alert('Failed to load interviews');
                } finally {
                    this.loading = false;
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleString();
            }
        }
    }
},

{
    path: '/student/placements',
    name: 'StudentPlacements',
    meta: { 
        title: 'Placement History - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-file-earmark-check"></i> Placement History
                    </h1>
                    <button @click="loadPlacements" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading placements...</p>
                </div>
                
                <div v-else-if="placements.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No placement records found</p>
                </div>
                
                <div v-else class="card shadow-sm">
                    <div class="card-body">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Company</th>
                                    <th>Position</th>
                                    <th>Salary</th>
                                    <th>Joining Date</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="placement in placements" :key="placement.id">
                                    <td>{{ placement.company_name }}</td>
                                    <td>{{ placement.position }}</td>
                                    <td>₹{{ placement.salary.toLocaleString() }}</td>
                                    <td>{{ formatDate(placement.joining_date) }}</td>
                                    <td>
                                        <span :class="getStatusBadge(placement.status)">
                                            {{ placement.status }}
                                        </span>
                                    </td>
                                    <td>
                                        <button @click="downloadOfferLetter(placement.id)" class="btn btn-success btn-sm">
                                            <i class="bi bi-download"></i> Offer Letter
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                placements: [],
                loading: false
            }
        },
        created() {
            this.loadPlacements();
        },
        methods: {
            async loadPlacements() {
                this.loading = true;
                try {
                    const response = await studentAPI.getPlacements();
                    this.placements = response.data.placements;
                } catch (err) {
                    console.error('Error loading placements:', err);
                    alert('Failed to load placements');
                } finally {
                    this.loading = false;
                }
            },
            async downloadOfferLetter(placementId) {
                try {
                    const response = await studentAPI.downloadOfferLetter(placementId);
                    alert(' Offer letter generated! Check download.');
                    console.log('Offer Letter:', response.data.offer_letter);
                } catch (err) {
                    alert(err.response?.data?.error || 'Failed to download offer letter');
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                var badges = {
                    'offered': 'badge bg-success',
                    'joined': 'badge bg-primary',
                    'declined': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

// ========================================================================
// STUDENT ROUTES (Milestone 5 & 6) - COMPLETE WITH HISTORY TRACKING
// ========================================================================

{
    path: '/student/dashboard',
    name: 'StudentDashboard',
    meta: { 
        title: 'Student Dashboard - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-mortarboard"></i> Student Dashboard
                    </h1>
                    <button @click="loadStats" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> {{ loading ? 'Loading...' : 'Refresh' }}
                    </button>
                </div>
                
                <div v-if="error" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
                    <button @click="loadStats" class="btn btn-danger btn-sm ms-2">Retry</button>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading dashboard statistics...</p>
                </div>
                
                <div v-else-if="stats.student_name !== undefined">
                    <!-- Student Info -->
                    <div class="card mb-4 shadow-sm">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-person"></i> {{ stats.student_name }}
                            </h5>
                        </div>
                        <div class="card-body">
                            <span class="badge bg-info me-2">{{ stats.branch }}</span>
                            <span class="badge bg-secondary">{{ stats.roll_number }}</span>
                            <span class="badge" :class="stats.is_eligible ? 'bg-success' : 'bg-danger'">
                                {{ stats.is_eligible ? 'Eligible' : 'Not Eligible' }}
                            </span>
                            <span v-if="stats.has_placement" class="badge bg-success ms-2">
                                <i class="bi bi-check-circle"></i> Placed
                            </span>
                        </div>
                    </div>
                    
                    <!-- Stats Cards -->
                    <div class="row mb-4 g-4">
                        <div class="col-md-3 col-sm-6">
                            <div class="card bg-primary text-white h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-file-earmark-text display-6"></i>
                                    <h5 class="card-title mt-2">Total Applications</h5>
                                    <h2 class="display-4">{{ stats.total_applications || 0 }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <div class="card bg-info text-white h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-star display-6"></i>
                                    <h5 class="card-title mt-2">Shortlisted</h5>
                                    <h2 class="display-4">{{ stats.shortlisted || 0 }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <div class="card bg-warning text-dark h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-calendar display-6"></i>
                                    <h5 class="card-title mt-2">Interviews</h5>
                                    <h2 class="display-4">{{ stats.interview_scheduled || 0 }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3 col-sm-6">
                            <div class="card bg-success text-white h-100 shadow-sm">
                                <div class="card-body text-center">
                                    <i class="bi bi-check-circle display-6"></i>
                                    <h5 class="card-title mt-2">Placed</h5>
                                    <h2 class="display-4">{{ stats.placed || 0 }}</h2>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Placement Status Alert -->
                    <div v-if="stats.has_placement" class="alert alert-success">
                        <i class="bi bi-check-circle-fill"></i> 
                        <strong>Congratulations!</strong> You have been placed!
                        <span v-if="stats.placement_status">Status: {{ stats.placement_status }}</span>
                    </div>
                    
                    <!-- Quick Actions -->
                    <div class="card mb-4 shadow-sm">
                        <div class="card-header bg-dark text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-lightning-charge-fill"></i> Quick Actions
                            </h5>
                        </div>
                        <div class="card-body">
                            <div class="row g-3">
                                <div class="col-md-3 col-sm-6">
                                    <button @click="$router.push('/student/drives')" 
                                            class="btn btn-outline-primary w-100">
                                        <i class="bi bi-briefcase"></i> Browse Jobs
                                    </button>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <button @click="$router.push('/student/applications')" 
                                            class="btn btn-outline-success w-100">
                                        <i class="bi bi-file-earmark-text"></i> My Applications
                                    </button>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <button @click="$router.push('/student/interviews')" 
                                            class="btn btn-outline-warning w-100">
                                        <i class="bi bi-calendar"></i> Interviews
                                    </button>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <button @click="$router.push('/student/history')" 
                                            class="btn btn-outline-info w-100">
                                        <i class="bi bi-clock-history"></i> History
                                    </button>
                                </div>
                                <div class="col-md-3 col-sm-6">
                                    <button @click="$router.push('/student/profile')" 
                                            class="btn btn-outline-info w-100">
                                        <i class="bi bi-person"></i> My Profile
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                stats: {},
                loading: false,
                error: ''
            }
        },
        created() {
            this.loadStats();
        },
        methods: {
            async loadStats() {
                this.loading = true;
                this.error = '';
                try {
                    const response = await studentAPI.getDashboardStats();
                    this.stats = response.data;
                } catch (err) {
                    console.error('Stats error:', err);
                    this.error = err.response?.data?.error || 'Failed to load dashboard statistics';
                } finally {
                    this.loading = false;
                }
            }
        }
    }
},

{
    path: '/student/history',
    name: 'StudentHistory',
    meta: { 
        title: 'Application History - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-clock-history"></i> Application & Placement History
                    </h1>
                    <div>
                        <button @click="exportApplications" class="btn btn-success me-2" :disabled="exporting">
                            <i class="bi bi-file-earmark-spreadsheet"></i> 
                            {{ exporting ? 'Exporting...' : 'Export Applications CSV' }}
                        </button>
                        <button @click="exportPlacements" class="btn btn-info me-2" :disabled="exporting">
                            <i class="bi bi-file-earmark-spreadsheet"></i> 
                            {{ exporting ? 'Exporting...' : 'Export Placements CSV' }}
                        </button>
                        <button @click="loadHistory" class="btn btn-primary" :disabled="loading">
                            <i class="bi bi-arrow-clockwise"></i> Refresh
                        </button>
                    </div>
                </div>
                
                <div v-if="exportSuccess" class="alert alert-success">
                    <i class="bi bi-check-circle-fill"></i> {{ exportSuccess }}
                </div>
                
                <div v-if="exportError" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill"></i> {{ exportError }}
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading history...</p>
                </div>
                
                <div v-else-if="history.applications">
                    <!-- Application History -->
                    <div class="card shadow-sm mb-4">
                        <div class="card-header bg-primary text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-file-earmark-text"></i> Application History ({{ history.total_applications }})
                            </h5>
                        </div>
                        <div class="card-body">
                            <div v-if="history.applications.length === 0" class="text-center py-4">
                                <i class="bi bi-inbox display-4 text-muted"></i>
                                <p class="text-muted mt-2">No applications yet</p>
                            </div>
                            <table v-else class="table table-hover">
                                <thead class="table-light">
                                    <tr>
                                        <th>Job Title</th>
                                        <th>Company</th>
                                        <th>Status</th>
                                        <th>Applied Date</th>
                                        <th>Feedback</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="app in history.applications" :key="app.id">
                                        <td>{{ app.job_title }}</td>
                                        <td>{{ app.company_name }}</td>
                                        <td>
                                            <span :class="getStatusBadge(app.status)">
                                                {{ app.status }}
                                            </span>
                                        </td>
                                        <td>{{ formatDate(app.application_date) }}</td>
                                        <td>{{ app.feedback || 'N/A' }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <!-- Placement History -->
                    <div class="card shadow-sm mb-4">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-check-circle"></i> Placement History ({{ history.total_placements }})
                            </h5>
                        </div>
                        <div class="card-body">
                            <div v-if="history.placements.length === 0" class="text-center py-4">
                                <i class="bi bi-inbox display-4 text-muted"></i>
                                <p class="text-muted mt-2">No placements yet</p>
                            </div>
                            <table v-else class="table table-hover">
                                <thead class="table-light">
                                    <tr>
                                        <th>Company</th>
                                        <th>Position</th>
                                        <th>Salary</th>
                                        <th>Joining Date</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="placement in history.placements" :key="placement.id">
                                        <td>{{ placement.company_name }}</td>
                                        <td>{{ placement.position }}</td>
                                        <td>₹{{ placement.salary.toLocaleString() }}</td>
                                        <td>{{ formatDate(placement.joining_date) }}</td>
                                        <td>
                                            <span :class="getPlacementBadge(placement.status)">
                                                {{ placement.status }}
                                            </span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                history: {
                    applications: [],
                    placements: []
                },
                loading: false,
                exporting: false,
                exportSuccess: '',
                exportError: '',
                total_applications: 0,
                total_placements: 0
            }
        },
        created() {
            this.loadHistory();
        },
        methods: {
            async loadHistory() {
                this.loading = true;
                try {
                    const response = await studentAPI.getHistory();
                    this.history = response.data.history;
                    this.total_applications = response.data.total_applications;
                    this.total_placements = response.data.total_placements;
                } catch (err) {
                    console.error('Error loading history:', err);
                    this.exportError = 'Failed to load history';
                } finally {
                    this.loading = false;
                }
            },
            async exportApplications() {
                this.exporting = true;
                this.exportSuccess = '';
                this.exportError = '';
                try {
                    const response = await studentAPI.exportApplications();
                    this.exportSuccess = '✅ ' + response.data.message;
                    setTimeout(() => {
                        this.exportSuccess = '';
                    }, 5000);
                } catch (err) {
                    console.error('Export applications error:', err);
                    this.exportError = err.response?.data?.error || 'Failed to export applications';
                } finally {
                    this.exporting = false;
                }
            },
            async exportPlacements() {
                this.exporting = true;
                this.exportSuccess = '';
                this.exportError = '';
                try {
                    const response = await studentAPI.exportPlacements();
                    this.exportSuccess = '✅ ' + response.data.message;
                    setTimeout(() => {
                        this.exportSuccess = '';
                    }, 5000);
                } catch (err) {
                    console.error('Export placements error:', err);
                    this.exportError = err.response?.data?.error || 'Failed to export placements';
                } finally {
                    this.exporting = false;
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                const badges = {
                    'applied': 'badge bg-primary',
                    'shortlisted': 'badge bg-warning text-dark',
                    'interview': 'badge bg-info',
                    'selected': 'badge bg-success',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            },
            getPlacementBadge(status) {
                const badges = {
                    'offered': 'badge bg-success',
                    'joined': 'badge bg-primary',
                    'declined': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

{
    path: '/student/drives',
    name: 'StudentDrives',
    meta: { 
        title: 'Browse Jobs - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1><i class="bi bi-briefcase"></i> Browse Job Postings</h1>
                    <button @click="loadDrives" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <div class="card mb-4 shadow-sm">
                    <div class="card-body">
                        <div class="row g-3">
                            <div class="col-md-4">
                                <input type="text" class="form-control" v-model="search" 
                                       placeholder="Search by job title or company..." 
                                       @keyup.enter="loadDrives" :disabled="loading">
                            </div>
                            <div class="col-md-3">
                                <input type="text" class="form-control" v-model="skills" 
                                       placeholder="Filter by skills..." 
                                       @keyup.enter="loadDrives" :disabled="loading">
                            </div>
                            <div class="col-md-3">
                                <button @click="loadDrives" class="btn btn-primary w-100" :disabled="loading">
                                    <i class="bi bi-search"></i> Search
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading job postings...</p>
                </div>
                
                <div v-else-if="drives.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No job postings found</p>
                </div>
                
                <div v-else class="row g-4">
                    <div class="col-md-6" v-for="drive in drives" :key="drive.id">
                        <div class="card h-100 shadow-sm">
                            <div class="card-body">
                                <h5 class="card-title">{{ drive.job_title }}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">{{ drive.company_name }}</h6>
                                <p class="card-text">
                                    <i class="bi bi-geo-alt"></i> {{ drive.location }} | 
                                    <i class="bi bi-currency-rupee"></i> {{ drive.salary.toLocaleString() }}
                                </p>
                                <p class="card-text">
                                    <small class="text-muted">
                                        <i class="bi bi-calendar"></i> Deadline: {{ formatDate(drive.application_deadline) }}
                                    </small>
                                </p>
                                <div class="mb-2">
                                    <span class="badge bg-info">{{ drive.skills_required }}</span>
                                </div>
                            </div>
                            <div class="card-footer bg-white">
                                <div class="d-flex justify-content-between">
                                    <button @click="viewDriveDetails(drive.id)" class="btn btn-outline-info btn-sm">
                                        <i class="bi bi-eye"></i> View Details
                                    </button>
                                    <button v-if="!drive.already_applied" 
                                            @click="applyToDrive(drive.id)" 
                                            class="btn btn-success btn-sm"
                                            :disabled="loading">
                                        <i class="bi bi-plus-lg"></i> Apply
                                    </button>
                                    <span v-else class="badge" :class="getStatusBadge(drive.application_status)">
                                        {{ drive.application_status }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                drives: [],
                loading: false,
                search: '',
                skills: '',
                currentPage: 1,
                totalPages: 1
            }
        },
        created() {
            this.loadDrives();
        },
        methods: {
            async loadDrives() {
                this.loading = true;
                try {
                    const response = await studentAPI.getDrives({
                        page: this.currentPage,
                        search: this.search,
                        skills: this.skills
                    });
                    this.drives = response.data.drives;
                    this.totalPages = response.data.pages;
                } catch (err) {
                    console.error('Error loading drives:', err);
                    alert('Failed to load job postings: ' + (err.response?.data?.error || 'Unknown error'));
                } finally {
                    this.loading = false;
                }
            },
            async applyToDrive(driveId) {
                if (!confirm('Are you sure you want to apply to this drive?')) return;
                try {
                    await studentAPI.applyToDrive(driveId);
                    alert(' Application submitted successfully!');
                    this.loadDrives();
                } catch (err) {
                    console.error('Apply error:', err);
                    const errorMsg = err.response?.data?.error || 'Failed to apply';
                    const isDuplicate = err.response?.data?.duplicate;
                    if (isDuplicate) {
                        alert('You have already applied to this drive');
                    } else {
                        alert(errorMsg);
                    }
                }
            },
            viewDriveDetails(driveId) {
                this.$router.push('/student/drives/' + driveId);
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                const badges = {
                    'applied': 'badge bg-primary',
                    'shortlisted': 'badge bg-warning text-dark',
                    'interview': 'badge bg-info',
                    'selected': 'badge bg-success',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

{
    path: '/student/applications',
    name: 'StudentApplications',
    meta: { 
        title: 'My Applications - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1><i class="bi bi-file-earmark-text"></i> My Applications</h1>
                    <button @click="loadApplications" class="btn btn-primary" :disabled="loading">
                        <i class="bi bi-arrow-clockwise"></i> Refresh
                    </button>
                </div>
                
                <div class="card mb-4 shadow-sm">
                    <div class="card-body">
                        <div class="row g-3">
                            <div class="col-md-4">
                                <select class="form-select" v-model="status" @change="loadApplications" :disabled="loading">
                                    <option value="">All Status</option>
                                    <option value="applied">Applied</option>
                                    <option value="shortlisted">Shortlisted</option>
                                    <option value="interview">Interview</option>
                                    <option value="selected">Selected</option>
                                    <option value="rejected">Rejected</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <button @click="loadApplications" class="btn btn-primary w-100" :disabled="loading">
                                    <i class="bi bi-search"></i> Filter
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading applications...</p>
                </div>
                
                <div v-else-if="applications.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No applications found</p>
                </div>
                
                <div v-else class="card shadow-sm">
                    <div class="card-body">
                        <table class="table table-hover">
                            <thead class="table-light">
                                <tr>
                                    <th>Job Title</th>
                                    <th>Company</th>
                                    <th>Location</th>
                                    <th>Status</th>
                                    <th>Applied Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="app in applications" :key="app.id">
                                    <td>{{ app.job_title }}</td>
                                    <td>{{ app.company_name }}</td>
                                    <td>{{ app.location }}</td>
                                    <td>
                                        <span :class="getStatusBadge(app.status)">
                                            {{ app.status }}
                                        </span>
                                    </td>
                                    <td>{{ formatDate(app.application_date) }}</td>
                                    <td>
                                        <button @click="viewApplication(app.id)" class="btn btn-info btn-sm">
                                            <i class="bi bi-eye"></i> View
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                applications: [],
                loading: false,
                status: '',
                currentPage: 1,
                totalPages: 1
            }
        },
        created() {
            this.loadApplications();
        },
        methods: {
            async loadApplications() {
                this.loading = true;
                try {
                    const response = await studentAPI.getApplications({
                        page: this.currentPage,
                        status: this.status
                    });
                    this.applications = response.data.applications;
                    this.totalPages = response.data.pages;
                } catch (err) {
                    console.error('Error loading applications:', err);
                    alert('Failed to load applications');
                } finally {
                    this.loading = false;
                }
            },
            viewApplication(appId) {
                this.$router.push('/student/applications/' + appId);
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getStatusBadge(status) {
                const badges = {
                    'applied': 'badge bg-primary',
                    'shortlisted': 'badge bg-warning text-dark',
                    'interview': 'badge bg-info',
                    'selected': 'badge bg-success',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

// ========================================================================
// COMPANY ROUTES - ADD DRIVE DETAIL ROUTE (FIXES 404)
// ========================================================================

{
    path: '/company/drives/:driveId',
    name: 'CompanyDriveDetails',
    meta: { 
        title: 'Drive Details - Placement Portal V2',
        requiresAuth: true, 
        role: 'company' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-briefcase"></i> Drive Details
                    </h1>
                    <button @click="$router.push('/company/drives')" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Back
                    </button>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading drive details...</p>
                </div>
                
                <div v-else-if="drive.id">
                    <div class="card shadow-sm">
                        <div class="card-header bg-primary text-white">
                            <h4 class="mb-0">{{ drive.job_title }}</h4>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <p><strong>Location:</strong> {{ drive.location }}</p>
                                    <p><strong>Salary:</strong> ₹{{ drive.salary.toLocaleString() }}</p>
                                    <p><strong>Status:</strong> 
                                        <span :class="getDriveStatusBadge(drive.status)">
                                            {{ drive.status }}
                                        </span>
                                    </p>
                                </div>
                                <div class="col-md-6">
                                    <p><strong>Applications:</strong> {{ drive.application_count }}</p>
                                    <p><strong>Shortlisted:</strong> {{ drive.shortlisted_count }}</p>
                                    <p><strong>Selected:</strong> {{ drive.selected_count }}</p>
                                </div>
                            </div>
                            <hr>
                            <h6>Job Description:</h6>
                            <p>{{ drive.job_description }}</p>
                            <h6>Eligibility Criteria:</h6>
                            <p>{{ drive.eligibility_criteria }}</p>
                            <h6>Skills Required:</h6>
                            <p>{{ drive.skills_required }}</p>
                            <p class="text-muted">
                                <i class="bi bi-calendar"></i> Application Deadline: {{ formatDate(drive.application_deadline) }}
                            </p>
                        </div>
                        <div class="card-footer bg-white">
                            <button @click="viewApplications" class="btn btn-success">
                                <i class="bi bi-people"></i> View Applications
                            </button>
                            <button v-if="drive.status === 'approved'" 
                                    @click="closeDrive" 
                                    class="btn btn-warning ms-2">
                                <i class="bi bi-x-circle"></i> Close Drive
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                drive: {},
                loading: false,
                driveId: ''
            }
        },
        created() {
            this.driveId = this.$route.params.driveId;
            this.loadDriveDetails();
        },
        methods: {
            async loadDriveDetails() {
                this.loading = true;
                try {
                    const response = await companyAPI.getDriveDetails(this.driveId);
                    this.drive = response.data;
                } catch (err) {
                    console.error('Load drive details error:', err);
                    alert('Failed to load drive details');
                } finally {
                    this.loading = false;
                }
            },
            viewApplications() {
                this.$router.push('/company/drives/' + this.driveId + '/applications');
            },
            async closeDrive() {
                if (!confirm('Are you sure you want to close this drive?')) return;
                try {
                    await companyAPI.updateDriveStatus(this.driveId, { status: 'closed' });
                    alert('Drive closed successfully');
                    this.loadDriveDetails();
                } catch (err) {
                    alert(err.response?.data?.error || 'Failed to close drive');
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            },
            getDriveStatusBadge(status) {
                const badges = {
                    'pending': 'badge bg-warning text-dark',
                    'approved': 'badge bg-success',
                    'active': 'badge bg-info',
                    'closed': 'badge bg-secondary',
                    'rejected': 'badge bg-danger'
                };
                return badges[status] || 'badge bg-secondary';
            }
        }
    }
},

// ========================================================================
// STUDENT ROUTES - ADD DRIVE DETAIL ROUTE (FIXES 404)
// ========================================================================

{
    path: '/student/drives/:driveId',
    name: 'StudentDriveDetails',
    meta: { 
        title: 'Drive Details - Placement Portal V2',
        requiresAuth: true, 
        role: 'student' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-briefcase"></i> Job Details
                    </h1>
                    <button @click="$router.push('/student/drives')" class="btn btn-secondary">
                        <i class="bi bi-arrow-left"></i> Back
                    </button>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading drive details...</p>
                </div>
                
                <div v-else-if="drive.id">
                    <div class="card shadow-sm">
                        <div class="card-header bg-primary text-white">
                            <h4 class="mb-0">{{ drive.job_title }}</h4>
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">{{ drive.company.name }}</h5>
                            <p class="card-text">
                                <i class="bi bi-geo-alt"></i> {{ drive.location }} | 
                                <i class="bi bi-currency-rupee"></i> {{ drive.salary.toLocaleString() }}
                            </p>
                            <hr>
                            <h6>Job Description:</h6>
                            <p>{{ drive.job_description }}</p>
                            <h6>Eligibility Criteria:</h6>
                            <p>{{ drive.eligibility_criteria }}</p>
                            <h6>Skills Required:</h6>
                            <p>{{ drive.skills_required }}</p>
                            <p class="text-muted">
                                <i class="bi bi-calendar"></i> Application Deadline: {{ formatDate(drive.application_deadline) }}
                            </p>
                            
                            <div v-if="drive.is_expired" class="alert alert-danger">
                                <i class="bi bi-exclamation-triangle-fill"></i> 
                                Application deadline has passed
                            </div>
                            
                            <div v-else-if="drive.already_applied" class="alert alert-info">
                                <i class="bi bi-info-circle-fill"></i> 
                                You have already applied to this drive. Status: {{ drive.application_status }}
                            </div>
                            
                            <button v-if="!drive.already_applied && !drive.is_expired" 
                                    @click="applyToDrive" 
                                    class="btn btn-success btn-lg"
                                    :disabled="loading">
                                <i class="bi bi-plus-lg"></i> Apply Now
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                drive: {},
                loading: false,
                error: '',
                driveId: ''
            }
        },
        created() {
            this.driveId = this.$route.params.driveId;
            this.loadDriveDetails();
        },
        methods: {
            async loadDriveDetails() {
                this.loading = true;
                this.error = '';
                try {
                    const response = await studentAPI.getDriveDetails(this.driveId);
                    this.drive = response.data;
                } catch (err) {
                    console.error('Load drive details error:', err);
                    this.error = err.response?.data?.error || 'Failed to load drive details';
                } finally {
                    this.loading = false;
                }
            },
            async applyToDrive() {
                if (!confirm('Are you sure you want to apply to this drive?')) return;
                try {
                    await studentAPI.applyToDrive(this.driveId);
                    alert(' Application submitted successfully!');
                    this.loadDriveDetails();
                } catch (err) {
                    console.error('Apply error:', err);
                    alert('Failed to apply: ' + (err.response?.data?.error || 'Unknown error'));
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString();
            }
        }
    }
},

{
    path: '/admin/monthly_reports',
    name: 'AdminMonthlyReports',
    meta: { 
        title: 'Monthly Reports - Placement Portal V2',
        requiresAuth: true, 
        role: 'admin' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-file-earmark-bar-graph"></i> Monthly Placement Reports
                    </h1>
                    <div>
                        <button @click="generateReport" class="btn btn-success me-2" :disabled="generating">
                            <i class="bi bi-arrow-clockwise"></i> 
                            {{ generating ? 'Generating...' : 'Generate Report' }}
                        </button>
                        <button @click="loadReports" class="btn btn-primary" :disabled="loading">
                            <i class="bi bi-arrow-clockwise"></i> Refresh
                        </button>
                    </div>
                </div>
                
                <div v-if="generateSuccess" class="alert alert-success">
                    <i class="bi bi-check-circle-fill"></i> {{ generateSuccess }}
                </div>
                
                <div v-if="generateError" class="alert alert-danger">
                    <i class="bi bi-exclamation-triangle-fill"></i> {{ generateError }}
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading reports...</p>
                </div>
                
                <div v-else-if="reports.length === 0" class="text-center py-5">
                    <i class="bi bi-inbox display-4 text-muted"></i>
                    <p class="text-muted mt-2">No monthly reports found</p>
                    <p class="text-muted">Click "Generate Report" to create monthly reports</p>
                    <button @click="generateReport" class="btn btn-success mt-2" :disabled="generating">
                        <i class="bi bi-plus-lg"></i> Generate Report
                    </button>
                </div>
                
                <div v-else class="card shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-file-earmark-bar-graph"></i> Available Reports ({{ reports.length }})
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead class="table-light">
                                    <tr>
                                        <th>Company</th>
                                        <th>Report Period</th>
                                        <th>Generated Date</th>
                                        <th>File Size</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="report in reports" :key="report.filename">
                                        <td><strong>{{ report.company_name }}</strong></td>
                                        <td>
                                            <span class="badge bg-info">{{ report.period }}</span>
                                        </td>
                                        <td>{{ formatDate(report.created_at) }}</td>
                                        <td>{{ formatFileSize(report.file_size) }}</td>
                                        <td>
                                            <div class="btn-group btn-group-sm">
                                                <button @click="viewReport(report)" class="btn btn-info" title="View Report">
                                                    <i class="bi bi-eye"></i> View
                                                </button>
                                                <button @click="downloadReport(report)" class="btn btn-success" title="Download Report">
                                                    <i class="bi bi-download"></i> Download
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                
                <!-- Report Preview Modal -->
                <div v-if="showPreview" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
                    <div class="modal-dialog modal-xl">
                        <div class="modal-content">
                            <div class="modal-header bg-primary text-white">
                                <h5 class="modal-title">
                                    <i class="bi bi-file-earmark-bar-graph"></i> {{ selectedReport?.company_name }} - {{ selectedReport?.period }}
                                </h5>
                                <button type="button" class="btn-close btn-close-white" @click="closePreview"></button>
                            </div>
                            <div class="modal-body" style="height: 600px; overflow-y: auto;">
                                <iframe :src="previewUrl" width="100%" height="100%" style="border: none;"></iframe>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="closePreview">
                                    <i class="bi bi-x-lg"></i> Close
                                </button>
                                <button type="button" class="btn btn-success" @click="downloadReport(selectedReport)">
                                    <i class="bi bi-download"></i> Download
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                reports: [],
                loading: false,
                generating: false,
                generateSuccess: '',
                generateError: '',
                showPreview: false,
                selectedReport: null,
                previewUrl: ''
            }
        },
        created() {
            this.loadReports();
        },
        methods: {
            async loadReports() {
                this.loading = true;
                this.generateError = '';
                try {
                    const response = await adminAPI.getMonthlyReports();
                    this.reports = response.data.reports;
                } catch (err) {
                    console.error('Error loading reports:', err);
                    this.generateError = err.response?.data?.error || 'Failed to load reports';
                } finally {
                    this.loading = false;
                }
            },
            async generateReport() {
                this.generating = true;
                this.generateSuccess = '';
                this.generateError = '';
                try {
                    const response = await adminAPI.generateMonthlyReport();
                    this.generateSuccess = '✅ ' + response.data.message;
                    setTimeout(() => {
                        this.generateSuccess = '';
                        this.loadReports();
                    }, 3000);
                } catch (err) {
                    console.error('Error generating report:', err);
                    this.generateError = err.response?.data?.error || 'Failed to generate report';
                } finally {
                    this.generating = false;
                }
            },
            viewReport(report) {
                this.selectedReport = report;
                this.previewUrl = report.download_url;
                this.showPreview = true;
            },
            closePreview() {
                this.showPreview = false;
                this.selectedReport = null;
                this.previewUrl = '';
            },
            async downloadReport(report) {
                try {
                    const response = await adminAPI.downloadMonthlyReport(report.filename);
                    
                    // Create download link
                    const blob = new Blob([response.data], { type: 'text/html' });
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = report.filename;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    window.URL.revokeObjectURL(url);
                    
                    console.log('Report downloaded:', report.filename);
                } catch (err) {
                    console.error('Error downloading report:', err);
                    alert('Failed to download report');
                }
            },
            formatDate(dateString) {
                if (!dateString) return 'N/A';
                return new Date(dateString).toLocaleDateString() + ' ' + new Date(dateString).toLocaleTimeString();
            },
            formatFileSize(bytes) {
                if (!bytes) return '0 B';
                const k = 1024;
                const sizes = ['B', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
            }
        }
    }
},

{
    path: '/admin/cache_stats',
    name: 'AdminCacheStats',
    meta: { 
        title: 'Cache Statistics - Placement Portal V2',
        requiresAuth: true, 
        role: 'admin' 
    },
    component: {
        template: `
            <div>
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h1>
                        <i class="bi bi-speedometer2"></i> Cache Statistics
                    </h1>
                    <div>
                        <button @click="clearCache" class="btn btn-danger me-2" :disabled="loading">
                            <i class="bi bi-trash"></i> Clear All Cache
                        </button>
                        <button @click="loadStats" class="btn btn-primary" :disabled="loading">
                            <i class="bi bi-arrow-clockwise"></i> {{ loading ? 'Loading...' : 'Refresh' }}
                        </button>
                    </div>
                </div>
                
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="mt-2">Loading cache statistics...</p>
                </div>
                
                <div v-else-if="stats.cache_stats" class="row g-4">
                    <!-- Cache Status -->
                    <div class="col-md-3">
                        <div class="card" :class="stats.cache_stats.enabled ? 'bg-success text-white' : 'bg-danger text-white'">
                            <div class="card-body text-center">
                                <i class="bi bi-hdd-network display-4"></i>
                                <h5 class="card-title mt-2">Cache Status</h5>
                                <h2 class="display-4">{{ stats.cache_stats.enabled ? 'Enabled' : 'Disabled' }}</h2>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Keys Count -->
                    <div class="col-md-3">
                        <div class="card bg-primary text-white">
                            <div class="card-body text-center">
                                <i class="bi bi-key display-4"></i>
                                <h5 class="card-title mt-2">Cached Keys</h5>
                                <h2 class="display-4">{{ stats.cache_stats.keys_count || 0 }}</h2>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Hit Rate -->
                    <div class="col-md-3">
                        <div class="card bg-info text-white">
                            <div class="card-body text-center">
                                <i class="bi bi-graph-up display-4"></i>
                                <h5 class="card-title mt-2">Hit Rate</h5>
                                <h2 class="display-4">{{ stats.cache_stats.hit_rate || 0 }}%</h2>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Memory Used -->
                    <div class="col-md-3">
                        <div class="card bg-warning text-dark">
                            <div class="card-body text-center">
                                <i class="bi bi-memory display-4"></i>
                                <h5 class="card-title mt-2">Memory Used</h5>
                                <h2 class="display-4">{{ stats.cache_stats.memory_used || 0 }} MB</h2>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Cache Hits -->
                    <div class="col-md-6">
                        <div class="card shadow-sm">
                            <div class="card-header bg-success text-white">
                                <h5 class="mb-0"><i class="bi bi-check-circle"></i> Cache Hits</h5>
                            </div>
                            <div class="card-body text-center">
                                <h2 class="display-4">{{ stats.cache_stats.hits || 0 }}</h2>
                                <p class="text-muted">Requests served from cache</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Cache Misses -->
                    <div class="col-md-6">
                        <div class="card shadow-sm">
                            <div class="card-header bg-danger text-white">
                                <h5 class="mb-0"><i class="bi bi-x-circle"></i> Cache Misses</h5>
                            </div>
                            <div class="card-body text-center">
                                <h2 class="display-4">{{ stats.cache_stats.misses || 0 }}</h2>
                                <p class="text-muted">Requests requiring database query</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Cache Expiry Config -->
                    <div class="col-12">
                        <div class="card shadow-sm">
                            <div class="card-header bg-dark text-white">
                                <h5 class="mb-0"><i class="bi bi-clock"></i> Cache Expiry Configuration</h5>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    <table class="table table-hover">
                                        <thead>
                                            <tr>
                                                <th>Cache Type</th>
                                                <th>Expiry Time</th>
                                                <th>Description</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(expiry, key) in stats.cache_expiry_config" :key="key">
                                                <td><code>{{ key }}</code></td>
                                                <td>{{ formatExpiry(expiry) }}</td>
                                                <td>{{ getExpiryDescription(key) }}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `,
        data() {
            return {
                stats: {},
                loading: false
            }
        },
        created() {
            this.loadStats();
        },
        methods: {
            async loadStats() {
                this.loading = true;
                try {
                    const response = await adminAPI.getCacheStats();
                    this.stats = response.data;
                } catch (err) {
                    console.error('Error loading cache stats:', err);
                    alert('Failed to load cache statistics');
                } finally {
                    this.loading = false;
                }
            },
            async clearCache() {
                if (!confirm('Are you sure you want to clear all cache? This may temporarily slow down the application.')) {
                    return;
                }
                
                try {
                    await adminAPI.clearCache();
                    alert(' Cache cleared successfully');
                    this.loadStats();
                } catch (err) {
                    console.error('Error clearing cache:', err);
                    alert('Failed to clear cache');
                }
            },
            formatExpiry(seconds) {
                if (seconds >= 3600) {
                    return `${seconds / 3600} hour(s)`;
                } else if (seconds >= 60) {
                    return `${seconds / 60} minute(s)`;
                } else {
                    return `${seconds} second(s)`;
                }
            },
            getExpiryDescription(key) {
                const descriptions = {
                    'default': 'Default cache expiry for most endpoints',
                    'job_listings': 'Job/drive listings viewed by students',
                    'company_search': 'Company search results',
                    'student_search': 'Student search results',
                    'dashboard_stats': 'Dashboard statistics for all roles',
                    'user_profile': 'User profile data',
                    'placement_stats': 'Placement statistics and reports',
                    'admin_stats': 'Admin dashboard statistics'
                };
                return descriptions[key] || 'Custom cache expiry';
            }
        }
    }
},
    
    // ========================================================================
    // 404 ROUTE
    // ========================================================================
    
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        meta: { 
            title: '404 - Page Not Found',
            requiresAuth: false 
        },
        component: {
            template: `
                <div class="text-center py-5">
                    <h1 class="display-1">404</h1>
                    <h2>Page Not Found</h2>
                    <p class="lead">The page you're looking for doesn't exist.</p>
                    <router-link to="/" class="btn btn-primary btn-lg">
                        <i class="bi bi-house"></i> Go Home
                    </router-link>
                </div>
            `
        }
    }
];


const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes
});

router.beforeEach(function(to, from, next) {
    // Update page title
    if (to.meta && to.meta.title) {
        document.title = to.meta.title;
    } else {
        document.title = 'Placement Portal V2';
    }
    
    const isLoggedIn = auth.isLoggedIn();
    const userRole = auth.getRole();
    
    // Check authentication
    if (to.meta && to.meta.requiresAuth && !isLoggedIn) {
        next('/login');
        return;
    }
    
    // Check role-based access
    if (to.meta && to.meta.role && userRole !== to.meta.role) {
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
        return;
    }
    
    // Redirect logged-in users from login/register pages
    if (isLoggedIn && (to.path === '/login' || to.path.startsWith('/register'))) {
        if (userRole === 'admin') {
            next('/admin/dashboard');
        } else if (userRole === 'company') {
            next('/company/dashboard');
        } else if (userRole === 'student') {
            next('/student/dashboard');
        } else {
            next();
        }
        return;
    }
    
    next();
});


window.appRoutes = routes;

console.log('Router Initialized - Milestone 4 Complete');
console.log('Total Routes:', routes.length);
console.log('Auth Guards: Enabled');
console.log('RBAC: Admin/Company/Student');