// exit button
const exitButton = document.getElementById('exit-button');
const alertExitDialog = document.getElementById('alert-exit-dialog');
const alertExitOkButton = document.getElementById('alert-exit-ok');
const alertExitCancelButton = document.getElementById('alert-exit-cancel');

exitButton.addEventListener('click', function() {
  alertExitDialog.classList.remove('hide');
});

alertExitOkButton.addEventListener('click', function() {
  window.location.href = "/";
});

alertExitCancelButton.addEventListener('click', function() {
  alertExitDialog.classList.add('hide');
});