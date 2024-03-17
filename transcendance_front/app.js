// app.js

// Check if the isLoggedIn status is stored in localStorage
let isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

// Function to handle user login

function setItemToLocalStorage2() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Stocker le nom d'utilisateur et le mot de passe dans le localStorage
    localStorage.setItem('username', username);
    localStorage.setItem('password', password);

    // Rediriger vers la page de profil
    // window.location.href = 'profile.html';
}

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
        // document.getElementById('sidebar').style.display = 'block';

        // Load the main component
        fetch('profile.html')
            .then(response => response.text()) //: C'est une chaîne de promesses. Lorsque la requête fetch réussit, elle convertit la réponse en texte brut.
            .then(html => {
                document.getElementById('main-content').innerHTML = html;
            }) //C'est une autre chaîne de promesses. Elle prend le texte brut de la réponse précédente et l'insère en tant que HTML interne de l'élément ayant l'identifiant "main-content".
            .catch(error => console.error('Error loading main page:', error)); // Cela attrape les erreurs qui surviennent pendant la requête fetch ou le traitement de la réponse, et les journalise dans la console.
            
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
                localStorage.setItem('userName', 'aachaq');
                setItemToLocalStorage2();
                alert('Login successful!');
                window.location.href = 'profile.html';
            });
        })
        .catch(error => console.error('Error loading login page:', error));
}

// Load the login component initially
loadLoginComponent();








// get the password and email from the form and store them in the local storage.
// send a Post request with the values of email and password to the endpoint /login .



