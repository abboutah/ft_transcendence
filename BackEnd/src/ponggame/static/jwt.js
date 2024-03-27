


function getCookie(cookieName)
{
    const cookieString = document.cookie;
    const cookies = cookieString.split(';');

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(cookieName + '=')) {
            return cookie.substring(cookieName.length + 1);
        }
    }
    return null; // Retourne null si le cookie n'est pas trouvé
}



let token = getCookie(cookieName);


const formData = new FormData();
formData.append('username', 'valeur_username');
formData.append('password', 'valeur_password');
formData.append('token', 'valeur_token');


const response = fetch('http://another.com/', {
  credentials: "include",
body: {
    username: "",
    password: "",
},method: "POST"
});

response.json()















