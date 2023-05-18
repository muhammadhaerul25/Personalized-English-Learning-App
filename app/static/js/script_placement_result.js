const questionContainer = document.querySelector('.question-container');

// FUNCTIONS
function addLoader() {
  const loaderContainer = document.querySelector('.loader-container');
  const loader = document.createElement('div');
  loader.classList.add('loader');
  loaderContainer.appendChild(loader);
}

function removeLoader() {
  const loader = document.querySelector('.loader');
  if (loader) {
    loader.remove();
  }
}

function getData() {
  addLoader();
  fetch('/result')
    .then(response => response.json())
    .then(data => {
      console.log(data); // periksa apakah data sudah diterima dengan benar
      if (data.result.length === 0) {
        setTimeout(() => {
          getData();
          removeLoader()
        }, 0); // tunggu 1 detik sebelum mengambil data lagi
      } else {

        removeLoader()
        const result = data.result;
        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        const bubbleText = document.createElement('p');
        bubbleText.innerHTML = result.replace(/\n/g, '<br>'); // Tambahkan tag br setelah setiap opsi
        bubble.appendChild(bubbleText);
        questionContainer.appendChild(bubble);

      }

    })
    .catch(error => {
      console.error('Error fetching data:', error);
      setTimeout(() => {
        getData();
        removeLoader()
      }, 0); // tunggu 1 detik sebelum mengambil data lagi
    });
}

//MAIN EVENT
getData(); // panggil fungsi untuk pertama kali saat halaman dimuat

//EVENTS
const saveButton = document.getElementById('save-button');
const successMessage = document.getElementById('success-message');

saveButton.addEventListener('click', () => {
  const bubbleText = document.querySelector('.bubble p').innerHTML;
  const resultData = { result: bubbleText };
  
  fetch('/save-result', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(resultData)
  })
  .then(response => {
    if (response.ok) {
      successMessage.textContent = 'Result saved successfully!';
      successMessage.style.display = 'block';
      setTimeout(() => {
        successMessage.style.display = 'none';
      }, 3000); // Hide the success message after 3 seconds
    } else {
      console.error('Failed to save result.');
    }
  })
  .catch(error => {
    console.error('Error saving result:', error);
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
  // redirect ke halaman lain
  window.location.href = '/';

});



