// Global state tracking
let currentUser = null;
let currentRole = null;

// Mock login handler to switch dashboard interfaces
function loginUser(email, password) {
    // 1. Hit your backend to read users
    fetch('http://127.0.0.1:8000/users/')
        .then(res => res.json())
        .then(users => {
            // Find user matching credentials
            const user = users.find(u => u.email === email);
            if (user) {
                currentUser = user;
                currentRole = user.role; // 'admin', 'trainer', or 'member'
                renderDashboard();
            } else {
                alert("Invalid user credentials");
            }
        });
}

// Dynamically render sidebar items based on user role
function renderDashboard() {
    document.getElementById('login-container').classList.add('hidden');
    document.getElementById('dashboard-container').classList.remove('hidden');
    
    const sidebar = document.getElementById('sidebar-menu');
    sidebar.innerHTML = ''; // Clear previous items

    if (currentRole === 'admin') {
        sidebar.innerHTML = `
            <button onclick="showSection('users')">Manage Users</button>
            <button onclick="showSection('plans')">Membership Plans</button>
        `;
    } else if (currentRole === 'trainer') {
        sidebar.innerHTML = `
            <button onclick="showSection('workouts')">Assign Workouts</button>
            <button onclick="showSection('progress')">Track Biometrics</button>
        `;
    } else if (currentRole === 'member') {
        sidebar.innerHTML = `
            <button onclick="showSection('my-plan')">My Routine</button>
            <button onclick="showSection('attendance')">My Attendance</button>
        `;
    }
}