// Check if user is logged in
function isLoggedIn() {
    return localStorage.getItem('authToken') !== null;
}

// Get the current user's token
function getToken() {
    return localStorage.getItem('authToken');
}

// Get the current user's ID
function getUserId() {
    return localStorage.getItem('userId');
}

// Get the current user's username
function getUsername() {
    return localStorage.getItem('username');
}

// Logout function
function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    window.location.href = 'homepage.html';
}

// Add authentication headers to fetch requests
function authenticatedFetch(url, options = {}) {
    const token = getToken();
    if (!token) {
        return Promise.reject(new Error('No authentication token found'));
    }

    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`
    };

    return fetch(url, {
        ...options,
        headers
    });
}

// Update UI based on authentication status
function updateAuthUI() {
    const loggedIn = isLoggedIn();
    const authButtons = document.querySelectorAll('.auth-dependent');
    
    authButtons.forEach(button => {
        if (button.classList.contains('logged-in-only')) {
            button.style.display = loggedIn ? 'block' : 'none';
        } else if (button.classList.contains('logged-out-only')) {
            button.style.display = loggedIn ? 'none' : 'block';
        }
    });

    // If there's a username display element, update it
    const usernameElement = document.getElementById('username-display');
    if (usernameElement && loggedIn) {
        usernameElement.textContent = getUsername();
    }
}

// Call this when the page loads
document.addEventListener('DOMContentLoaded', updateAuthUI); 