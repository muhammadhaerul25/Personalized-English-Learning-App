import { getResult } from './helpers.js';


//MAIN EVENT
getResult('/get-result-test'); 


//EVENTS
// Event pada saat tombol save button diklik
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
      window.scrollTo(0, 0);
      successMessage.textContent = 'Success to save result test!';
      successMessage.style.display = 'block';
      setTimeout(() => {
        successMessage.style.display = 'none';
      }, 3000); // Hide the success message after 3 seconds
    } else {
      window.scrollTo(0, 0);
      successMessage.textContent = 'Failed to save result test!';
      successMessage.style.display = 'block';
      setTimeout(() => {
        successMessage.style.display = 'none';
      }, 3000); // Hide the success message after 3 seconds
    }
  })
  .catch(error => {
    console.error('Error saving result test:', error);
  });
});





