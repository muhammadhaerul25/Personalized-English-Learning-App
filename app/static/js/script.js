const logoutButton = document.getElementById('logout-button');
const alertDialog = document.getElementById('alert-dialog');
const alertOkButton = document.getElementById('alert-ok');
const alertCancelButton = document.getElementById('alert-cancel');

logoutButton.addEventListener('click', function() {
  alertDialog.classList.remove('hide');
});

alertOkButton.addEventListener('click', function() {
  window.location.href = "/logout";
});

alertCancelButton.addEventListener('click', function() {
  alertDialog.classList.add('hide');
});

