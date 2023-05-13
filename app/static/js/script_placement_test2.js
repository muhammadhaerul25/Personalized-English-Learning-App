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
  fetch('/section2')
    .then(response => response.json())
    .then(data => {
      console.log(data); // periksa apakah data sudah diterima dengan benar
      if (data.questions.length === 0) {
        setTimeout(() => {
          getData();
          removeLoader()
        }, 1000); // tunggu 1 detik sebelum mengambil data lagi
      } else {
        removeLoader()
        const questions = data.questions;
        questions.forEach((question, index) => {
          const bubble = document.createElement('div');
          bubble.classList.add('bubble');
          const bubbleText = document.createElement('p');
          bubbleText.innerHTML = question.replace(/\n/g, '<br>'); // Tambahkan tag br setelah setiap opsi
          bubble.appendChild(bubbleText);
          questionContainer.appendChild(bubble);
        });
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


getData(); // panggil fungsi untuk pertama kali saat halaman dimuat




//BUTTONS
const form = document.getElementById('answer-form');
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
  let answers = '';
  const inputs = form.querySelectorAll('.answer-input');
  inputs.forEach((input, index) => {
    answers += `${index + 1}. ${input.value}\n`;
  });
  console.log(answers);

  fetch('/submit-answer', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({answers: answers})
  })
  .then(response => response.text())
  .then(data => {
    console.log("Answers submitted!");
    console.log(data);
    // redirect ke halaman lain
    window.location.href = '/placement-test3';
    inputs.forEach((input) => {
      input.value = '';
    });
    alertDialog.classList.add('hide');
  })
  .catch(error => {
    console.error('Error submitting answers:', error);
  });
});



