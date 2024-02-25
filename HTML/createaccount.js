document.getElementById("createAccountForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var email = document.getElementById("email").value;

    fetch('/createAccount', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
            email: email
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("Account created successfully!");
            window.location.href = '/login.html'; // Redirect to login after account creation
        } else {
            alert("Error creating account: " + data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});