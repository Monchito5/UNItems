// Password toggle
const passwordInput = document.getElementById('passwordInput');
const passwordToggle = document.getElementById('passwordToggle');
const passwordInputR = document.getElementById('passwordInputR');
const passwordToggleR = document.getElementById('passwordToggleR');
// Login buttons
const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

passwordToggle.addEventListener('click', function() {
  passwordInput.type === 'password' ? passwordInput.type = 'text' : passwordInput.type = 'password';
  passwordToggle.firstElementChild.classList.toggle('fa-eye-slash');
  passwordToggle.firstElementChild.classList.toggle('fa-eye');
});

passwordToggleR.addEventListener('click', function() {
  passwordInputR.type === 'password' ? passwordInputR.type = 'text' : passwordInputR.type = 'password';
  passwordToggleR.firstElementChild.classList.toggle('fa-eye-slash');
  passwordToggleR.firstElementChild.classList.toggle('fa-eye');
});

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});
