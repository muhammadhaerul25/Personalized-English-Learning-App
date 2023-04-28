//ALERT BUTTON
const submitButton = document.querySelector('.submit-button');
const alertDialog = document.querySelector('#alert-dialog');
const alertOk = document.querySelector('#alert-ok');
const alertCancel = document.querySelector('#alert-cancel');

submitButton.addEventListener('click', (event) => {
  event.preventDefault();
  alertDialog.classList.remove('hide');
});

alertCancel.addEventListener('click', () => {
  alertDialog.classList.add('hide');
});

alertOk.addEventListener('click', () => {
  window.location.href = "/placement-test1";
});
