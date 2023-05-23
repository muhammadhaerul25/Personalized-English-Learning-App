// function getData() {
//   addLoader();
//   fetch('/section1')
//     .then(response => response.json())
//     .then(data => {
//       console.log(data); // periksa apakah data sudah diterima dengan benar
//       if (data.questions.length === 0) {
//         setTimeout(() => {
//           getData();
//           removeLoader()
//         }, 0); // tunggu 1 detik sebelum mengambil data lagi
//       } else {
//         removeLoader()
//         const questions = data.questions;
//         questions.forEach((question, index) => {
//           const bubble = document.createElement('div');
//           bubble.classList.add('bubble');
//           const bubbleText = document.createElement('p');
//           bubbleText.innerHTML = question.replace(/\n/g, '<br>'); // Tambahkan tag br setelah setiap opsi
//           bubble.appendChild(bubbleText);
//           questionContainer.appendChild(bubble);
//         });
//         startCountdown();
//       }
//     })
//     .catch(error => {
//       console.error('Error fetching data:', error);
//       setTimeout(() => {
//         getData();
//         removeLoader()
//       }, 0); // tunggu 1 detik sebelum mengambil data lagi
//     });
// }



// function startCountdown() {
//   setTimeout(function() {
//     const timesupContainer = document.getElementById('timesup-container');
//     const alertOk = document.querySelector('#alert-ok');

//     var countDownDate = new Date().getTime() + 10* 60 * 1000; // 10 minutes from now
//     var timerElement = document.getElementById("timer");

//     var countdownInterval = setInterval(function() {
//       var now = new Date().getTime();
//       var distance = countDownDate - now;

//       var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
//       var seconds = Math.floor((distance % (1000 * 60)) / 1000);

//       var formattedTime =
//         ("0" + minutes).slice(-2) + ":" + ("0" + seconds).slice(-2);

//       timerElement.textContent = formattedTime;

//       if (distance < 0) {
//         clearInterval(countdownInterval);
//         // Time countdown is finished, perform further actions here
//         timerElement.textContent = "00.00";
//         timesupContainer.style.display = 'block';
//         spanCountdown();
//         setTimeout(function() {
//           alertOk.click(); // Click the alertOk button after a 3-second delay
//         }, 5000);
        
//       }
//     }, 1000);
//   }, 0); // 5-second delay before starting the countdown
// }


//BUTTONS
// const form = document.getElementById('answer-form');
// const submitButton = document.querySelector('.submit-button');
// const alertDialog = document.querySelector('#alert-dialog');
// const alertOk = document.querySelector('#alert-ok');
// const alertCancel = document.querySelector('#alert-cancel');

// submitButton.addEventListener('click', (event) => {
//   event.preventDefault();
//   alertDialog.classList.remove('hide');
// });

// alertCancel.addEventListener('click', (event) => {
//   event.preventDefault();
//   alertDialog.classList.add('hide');
// });


// alertOk.addEventListener('click', (event) => {
//   event.preventDefault();
//   let answers = '';
//   const inputs = form.querySelectorAll('.answer-input');
//   inputs.forEach((input, index) => {
//     answers += `${index + 1}. ${input.value}\n`;
//   });
//   console.log(answers);

//   fetch('/submit-answer', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({answers: answers})
//   })
//   .then(response => response.text())
//   .then(data => {
//     console.log("Answers submitted!");
//     console.log(data);
//     // redirect ke halaman lain
//     window.location.href = '/placement-test2';
//     inputs.forEach((input) => {
//       input.value = '';
//     });
//     alertDialog.classList.add('hide');
//   })
//   .catch(error => {
//     console.error('Error submitting answers:', error);
//   });
// });