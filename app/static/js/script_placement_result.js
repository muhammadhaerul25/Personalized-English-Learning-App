import { getResult } from './helpers.js';


//MAIN EVENT
getResult('/result'); // panggil fungsi untuk pertama kali saat halaman dimuat


//EVENTS
const saveButton = document.getElementById('save-button');
const successMessage = document.getElementById('success-message');

saveButton.addEventListener('click', () => {
  const bubbleText = document.querySelector('.bubble p').innerHTML;
  const resultTest = { result_test: bubbleText };
  
  fetch('/save-result-test', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(resultTest)
  })
  .then(response => {
    if (response.ok) {
      successMessage.textContent = 'Result test saved successfully!';
      successMessage.style.display = 'block';
      setTimeout(() => {
        successMessage.style.display = 'none';
      }, 3000); // Hide the success message after 3 seconds
    } else {
      console.error('Failed to save result test.');
    }
  })
  .catch(error => {
    console.error('Error saving result test:', error);
  });
});




//BUTTONS
const submitButton = document.querySelector('.submit-button');
const alertDialog = document.querySelector('#alert-dialog');
const alertOk = document.querySelector('#alert-ok');
const alertCancel = document.querySelector('#alert-cancel');

submitButton.addEventListener('click', (event) => {
  event.preventDefault();
  alertDialog.classList.remove('hide');
});

alertCancel.addEventListener('click', (event) => {
  event.preventDefault();
  alertDialog.classList.add('hide');
});


alertOk.addEventListener('click', (event) => {
  event.preventDefault();
  window.location.href = '/';

});



