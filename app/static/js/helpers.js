import { placementTestTime, breakTestTime, textSpanCountdown } from './config.js';


// Loaders
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


// Countdowns
function placementTestCountdown(timeDuration) {
  const timesupContainer = document.getElementById('timesup-container');
  const alertOk = document.querySelector('#alert-ok');
  const timerElement = document.getElementById("timer");

  var countDownDate = new Date().getTime() + timeDuration; 

  var countdownInterval = setInterval(function() {
    var now = new Date().getTime();
    var distance = countDownDate - now;
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    var formattedTime =
      ("0" + minutes).slice(-2) + ":" + ("0" + seconds).slice(-2);

    timerElement.textContent = formattedTime;

    if (distance < 0) {
      clearInterval(countdownInterval);
      // Time countdown is finished, perform further actions here
      timerElement.textContent = "00:00";
      timesupContainer.style.display = 'block';
      spanCountdown(textSpanCountdown);
    }
  }, 1000);
}

  
  function spanCountdown(textSpanCountdown) {
    // Menambahkan kelas 'disable-selection' ke elemen body
    var body = document.querySelector('body');
    body.classList.add('disable-selection');

    const alertOk = document.querySelector('#alert-ok');

    var countdownElement = document.getElementById("span-countdown");
    var countdownValue = textSpanCountdown
  
    var countdownInterval = setInterval(function() {
      countdownValue--;
      countdownElement.textContent = countdownValue;
  
      if (countdownValue <= 0) {
        //Time countdown is finished, perform further actions here
        clearInterval(countdownInterval);
        alertOk.click();
      }
    }, 1000);
  }


// Data Fetching
function getQuestions(route) {
  addLoader();
  fetch(route)
    .then(response => response.json())
    .then(data => {
      console.log(data);

      if (data.questions.length === 0) {
        setTimeout(() => getQuestions(route), 0);
      } else {
        const questions = data.questions;
        const questionContainer = document.querySelector('.question-container');

        for (const question of questions) {
          const bubble = document.createElement('div');
          bubble.classList.add('bubble');
          const bubbleText = document.createElement('p');
          bubbleText.innerHTML = question.replace(/\n/g, '<br>');
          bubble.appendChild(bubbleText);
          questionContainer.appendChild(bubble);
        }
        placementTestCountdown(placementTestTime);
      }
      removeLoader();
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      setTimeout(() => getQuestions(route), 0);
      removeLoader();
    });
}


  function submitAnswers(event, href) {
    event.preventDefault();
    const form = document.getElementById('answer-form');
    const inputs = form.querySelectorAll('.answer-input');
    let answers = '';
    
    inputs.forEach((input, index) => {
      answers += `${index + 1}. ${input.value}\n`;
    });
    
    console.log(answers);
  
    fetch('/submit-answer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ answers: answers })
    })
      .then(response => response.text())
      .then(data => {
        window.location.href = href; 
        inputs.forEach((input) => {
          input.value = '';
        });
        hideAlertDialog();
      })
      .catch(error => {
        console.error('Error submitting answers:', error);
      });
  }


  function getResult(route) {
    addLoader();
  
    fetch(route)
      .then(response => response.json())
      .then(data => {
        console.log(data);
  
        if (data.result.length === 0) {
          setTimeout(() => getResult(route), 0);
          removeLoader();
        } else {
          removeLoader();
          const questionContainer = document.querySelector('.question-container');
          const bubble = document.createElement('div');
          bubble.classList.add('bubble');
          const bubbleText = document.createElement('p');
          bubbleText.innerHTML = data.result.replace(/\n/g, '<br>');
          bubble.appendChild(bubbleText);
          questionContainer.appendChild(bubble);
        }
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setTimeout(() => getResult(route), 0);
        removeLoader();
      });
  }



//Export
export {getQuestions, submitAnswers, getResult, addLoader, removeLoader, placementTestCountdown, spanCountdown };

  