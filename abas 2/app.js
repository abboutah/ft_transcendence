// app.js

// Check if the isLoggedIn status is stored in localStorage
let isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

// Function to handle user login
function loginUser(username, password) {
    // Perform login logic here (e.g., validate credentials, send request to server)
    // For simplicity, let's assume the login is successful
    // if (username === 'user' && password === 'password') {
    //     isLoggedIn = true;
    //     localStorage.setItem('isLoggedIn', 'true'); // Store the isLoggedIn status in localStorage
    //     alert('Login successful!');
    //     loadMainComponent(); // Load main component after successful login
    // } else {
    //     alert('Invalid username or password. Please try again.');
    // }
}

// Function to load the main component
function loadMainComponent() {
    if (isLoggedIn) {
        // Show the sidebar
        document.getElementById('sidebar').style.display = 'block';

        // Load the main component
        fetch('profile.html')
            .then(response => response.text())
            .then(html => {
                document.getElementById('main-content').innerHTML = html;
            })
            .catch(error => console.error('Error loading main page:', error));
            
    }
}

// Function to load the login component initially
function loadLoginComponent() {
    if (isLoggedIn) {
        loadMainComponent();
        return;
    }
    fetch('login.html') // Load login page
        .then(response => response.text())
        .then(html => {
            document.getElementById('main-content').innerHTML = html;
            document.getElementById('login-form').addEventListener('submit', function (event) {
                event.preventDefault();
                // const username = document.getElementById('username').value;
                // const password = document.getElementById('password').value;
                // loginUser(username, password);
                isLoggedIn = true;
                localStorage.setItem('isLoggedIn', 'true'); // Store the isLoggedIn status in localStorage
                alert('Login successful!');
                window.location.href = 'profile.html';
            });
        })
        .catch(error => console.error('Error loading login page:', error));
}

// Load the login component initially
loadLoginComponent();


