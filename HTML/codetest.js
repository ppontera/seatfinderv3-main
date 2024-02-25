document.getElementById("login").addEventListener("submit", function(event) {
    event.preventDefault();
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;




fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        }),
    })
    .then(response => {
        if (response.ok) {
            // Check if user is admin
            return response.json();
        } else {
            return response.json().then(data => {
                throw new Error(data.error);
            });
        }
    })
    .then(data => {
        // Check if user is admin
        if (data && data.isAdmin) {
            window.location.href = "/adminhome.html";
        } else {
            window.location.href = "/userhome.html";
        }
    })
    .catch(error => {
        console.error('Error during login:', error.message);
    });
});


