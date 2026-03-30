/**
 * API Configuration and Service Layer
 * Milestone 5: Student Dashboard and Job Application System
 */

// Axios instance with base configuration
const api = axios.create({
    baseURL: 'http://localhost:5000/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    },
    withCredentials: true  // Important for session cookies
});

// Request interceptor
api.interceptors.request.use(
    config => {
        console.log('📡 API Request:', config.method?.toUpperCase(), config.url);
        return config;
    },
    error => {
        console.error(' Request Error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    response => {
        console.log(' API Response:', response.status, response.config.url);
        return response;
    },
    error => {
        console.error(' API Error:', error.response?.status, error.response?.data);
        
        if (error.response && error.response.status === 401) {
            // Unauthorized - clear auth and redirect to login
            if (window.auth) {
                window.auth.clearUser();
            }
            window.location.hash = '#/login';
        }
        
        return Promise.reject(error);
    }
);

// Authentication API - FIXED to match backend /auth/register endpoint
const authAPI = {
    async login(username, password) {
        try {
            const response = await api.post('/auth/login', { username, password });
            return {
                success: true,
                user: response.data.user
            };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.error || 'Login failed. Please check credentials.'
            };
        }
    },
    
    async logout() {
        try {
            await api.post('/auth/logout');
        } catch (error) {
            console.error('Logout error:', error);
        }
    },
    
    async registerStudent(data) {
        try {
            // Prepare data for backend /auth/register endpoint
            const registerData = {
                username: data.username,
                email: data.email,
                password: data.password,
                role: 'student',
                student_data: {
                    full_name: data.full_name,
                    roll_number: data.roll_number,
                    branch: data.branch,
                    year_of_study: parseInt(data.year_of_study) || 4,
                    cgpa: parseFloat(data.cgpa) || 0.0,
                    phone: data.phone || '',
                    skills: data.skills || ''
                }
            };
            
            const response = await api.post('/auth/register', registerData);
            return {
                success: true,
                user: response.data.user,
                redirect_url: response.data.redirect_url || '/student/dashboard'
            };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.error || 'Registration failed'
            };
        }
    },
    
    async registerCompany(data) {
        try {
            // Prepare data for backend /auth/register endpoint
            const registerData = {
                username: data.username,
                email: data.email,
                password: data.password,
                role: 'company',
                company_data: {
                    company_name: data.company_name,
                    industry: data.industry,
                    location: data.location || '',
                    website: data.website || '',
                    hr_contact_name: data.hr_contact_name || '',
                    hr_contact_email: data.hr_contact_email || data.email,
                    hr_contact_phone: data.hr_contact_phone || '',
                    company_description: data.company_description || ''
                }
            };
            
            const response = await api.post('/auth/register', registerData);
            return {
                success: true,
                message: response.data.message || 'Registration successful. Pending admin approval.',
                redirect_url: response.data.redirect_url || '/login'
            };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.error || 'Registration failed'
            };
        }
    },
    
    async getCurrentUser() {
        try {
            const response = await api.get('/auth/me');
            return {
                success: true,
                user: response.data.user
            };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.error || 'Failed to get user info'
            };
        }
    }
};
// Admin API - Milestone 3 & 7
const adminAPI = {
    // Dashboard
    getDashboardStats: () => api.get('/admin/dashboard/stats'),
    
    // Companies
    getCompanies: (params) => api.get('/admin/companies', { params }),
    approveCompany: (id) => api.post(`/admin/companies/${id}/approve`),
    rejectCompany: (id) => api.post(`/admin/companies/${id}/reject`),
    blacklistCompany: (id) => api.post(`/admin/companies/${id}/blacklist`),
    unblacklistCompany: (id) => api.post(`/admin/companies/${id}/unblacklist`),
    
    // Students
    getStudents: (params) => api.get('/admin/students', { params }),
    blacklistStudent: (id) => api.post(`/admin/students/${id}/blacklist`),
    unblacklistStudent: (id) => api.post(`/admin/students/${id}/unblacklist`),
    
    // Drives
    getDrives: (params) => api.get('/admin/drives', { params }),
    approveDrive: (id) => api.post(`/admin/drives/${id}/approve`),
    rejectDrive: (id) => api.post(`/admin/drives/${id}/reject`),
    
    // Applications
    getApplications: (params) => api.get('/admin/applications', { params }),
    
    // Monthly Reports - Milestone 7
    getMonthlyReports: () => api.get('/admin/reports/monthly'),
    downloadMonthlyReport: (filename) => api.get(`/admin/reports/monthly/${filename}`, {
        responseType: 'blob'
    }),
    generateMonthlyReport: () => api.post('/admin/reports/monthly/generate'),

    // Cache Statistics - Milestone 8 
    getCacheStats: () => api.get('/admin/cache/stats'),
    clearCache: () => api.post('/admin/cache/clear'),
    invalidateJobListingsCache: () => api.post('/admin/cache/invalidate/job_listings')
};

// Company API - Milestone 4 & 7
const companyAPI = {
    // Dashboard
    getDashboardStats: () => api.get('/company/dashboard/stats'),
    
    // Profile
    getProfile: () => api.get('/company/profile'),
    updateProfile: (data) => api.put('/company/profile', data),
    
    // Drives
    getDrives: (params) => api.get('/company/drives', { params }),
    getDriveDetails: (id) => api.get(`/company/drives/${id}`),
    createDrive: (data) => api.post('/company/drives', data),
    updateDrive: (id, data) => api.put(`/company/drives/${id}`, data),
    updateDriveStatus: (id, data) => api.put(`/company/drives/${id}/status`, data),
    deleteDrive: (id) => api.delete(`/company/drives/${id}`),
    
    // Applications
    getApplications: (params) => api.get('/company/applications', { params }),
    getDriveApplications: (driveId, params) => api.get(`/company/drives/${driveId}/applications`, { params }),
    getApplicationDetails: (id) => api.get(`/company/applications/${id}`),
    updateApplicationStatus: (id, data) => api.put(`/company/applications/${id}/status`, data),
    scheduleInterview: (id, data) => api.post(`/company/applications/${id}/interview`, data),
    
    // Placements
    createPlacement: (applicationId, data) => api.post(`/company/applications/${applicationId}/placement`, data),
    getPlacements: (params) => api.get('/company/placements', { params }),

    // Export - Milestone 7
    exportApplications: () => api.post('/company/export/applications'),
    exportPlacements: () => api.post('/company/export/placements')
};

// Student API - Milestone 5 & 7
const studentAPI = {
    // Dashboard
    getDashboardStats: () => api.get('/student/dashboard/stats'),
    
    // Profile
    getProfile: () => api.get('/student/profile'),
    updateProfile: (data) => api.put('/student/profile', data),
    uploadResume: (formData) => api.post('/student/profile/resume', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    }),
    downloadResume: () => api.get('/student/profile/resume'),
    
    // Drives/Jobs
    getDrives: (params) => api.get('/student/drives', { params }),
    getDriveDetails: (id) => api.get(`/student/drives/${id}`),
    applyToDrive: (driveId) => api.post(`/student/drives/${driveId}/apply`),
    
    // Applications
    getApplications: (params) => api.get('/student/applications', { params }),
    getApplicationDetails: (id) => api.get(`/student/applications/${id}`),
    
    // Interviews
    getInterviews: () => api.get('/student/interviews'),
    
    // Placements
    getPlacements: () => api.get('/student/placements'),
    downloadOfferLetter: (placementId) => api.get(`/student/placements/${placementId}/offer-letter`),
    
    // History
    getHistory: () => api.get('/student/history'),

    // Export - Milestone 7
    exportApplications: () => api.post('/student/export/applications'),
    exportPlacements: () => api.post('/student/export/placements')
};

// Export for use in Vue components
window.authAPI = authAPI;
window.adminAPI = adminAPI;
window.companyAPI = companyAPI;
window.studentAPI = studentAPI;
window.api = api;

console.log(' API Module Loaded - Milestone 7');