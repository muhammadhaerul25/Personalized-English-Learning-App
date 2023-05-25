const signUpButton = document.getElementById('switch-register');
const signInButton = document.getElementById('switch-login');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});



//REGISTER EVENT
const registerForm = document.getElementById("form-register");
const nameInput = document.querySelector("#name-register");
const emailInputRegister = document.querySelector("#email-register");
const passwordInputRegister = document.querySelector("#password-register");
const passwordConfirmationInput = document.querySelector("#password-confirmation-register");
const errorRegister = document.querySelector("#error-register");

const registerButton = document.getElementById("button-register");

registerForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const nameValue = nameInput.value.trim();
  const emailValue = emailInputRegister.value.trim();
  const passwordValue = passwordInputRegister.value.trim();
  const passwordConfirmationValue = passwordConfirmationInput.value.trim();

  if (!nameValue || !emailValue || !passwordValue || !passwordConfirmationValue) {
    errorRegister.innerText = "Please fill in all fields";
    errorRegister.style.display = "block";
    console.log("Please fill in all fields");
    return;
  }
  
  if (passwordValue !== passwordConfirmationValue) {
    errorRegister.innerText = "Passwords do not match";
    errorRegister.style.display = "block";
    console.log("Passwords do not match");
    return;
  }

  fetch("/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ name: nameValue, email: emailValue, password: passwordValue })
  })
  .then(response => {
    if (response.ok) {
      alert("Registration successful");
      window.location.href = "/registration"; // Redirect ke halaman login
    } else {
        return response.json();
    }
  })
  .then(data => {
    if (data) {
        errorRegister.innerText = data.message;
        errorRegister.style.display = "block";
        console.log(data);
      }
  })
  .catch(error => {
    alert("Registration failed");
    console.error(error);
  });

});

registerButton.addEventListener("click", () => {
  registerForm.submit();
});



//LOGIN EVENT
const formLogin = document.querySelector("#form-login");
const emailInputLogin = document.querySelector("#email-login");
const passwordInputLogin = document.querySelector("#password-login");
const errorLogin = document.querySelector("#error-login");

formLogin.addEventListener("submit", (event) => {
  event.preventDefault();

  const emailValue = emailInputLogin.value.trim();
  const passwordValue = passwordInputLogin.value.trim();

  if (!emailValue || !passwordValue) {
    errorLogin.innerText = "Please fill in all fields";
    errorLogin.style.display = "block";
    console.log("Please fill in all fields");
    return
  }

  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email: emailValue, password: passwordValue })
  })
  .then(response => {
    if (response.ok) {
      window.location.href = "/"; // Redirect ke halaman dashboard
    } else if (response.status === 404) {
      errorLogin.innerText = "Email not found";
      errorLogin.style.display = "block";
    } else if (response.status === 401) {
      errorLogin.innerText = "Invalid password";
      errorLogin.style.display = "block";
    } else {
      alert("Login failed then");
      console.log(response);
    }
  })
  .catch(error => {
    alert("Login failed");
    console.error(error);
  });

});

