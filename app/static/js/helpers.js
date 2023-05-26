import { placementTestTime, breakTestTime, textSpanCountdown } from './config.js';
import { pronunciationDropdownOptions, contextDropdownOptions, readingDropdownOptions } from './config.js';


// Bubbles
function createBubble(sender, message) {
  const bubble = document.createElement('div');
  bubble.classList.add('message', sender);
  bubble.innerHTML = message.replace(/\n/g, '<br>');
  return bubble;
}



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



// Tabs
function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("conversation");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].classList.remove("active");
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].classList.remove("active");
  }
  document.getElementById(tabName).classList.add("active");
  evt.currentTarget.classList.add("active");
}



// Chats
function getChatHistory() {
  fetch('/chat-history')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      displayChatHistory(data.chat_history, 'pronunciation');
    })
    .catch(error => console.error(error));
}

function displayChatHistory(chatHistory, activeMode) {
  const activeConversation = document.getElementById(activeMode);
  console.log(activeConversation);
  console.log(chatHistory);

  // Tampilkan riwayat chat sesuai dengan mode yang aktif
  chatHistory.forEach(chat => {
    const { mode, message, response } = chat;

    // Cek apakah mode dari chat saat ini sama dengan mode yang aktif
    if (mode === activeMode) {
      // Buat elemen bubble untuk setiap pesan
      const userBubble = createBubble('user', message);
      const botBubble = createBubble('bot', response);

      // Tambahkan bubble ke aktivitas percakapan
      activeConversation.appendChild(userBubble);
      activeConversation.appendChild(botBubble);
    }
  });

  // Menggulir ke bawah setelah chat ditampilkan
  activeConversation.scrollTop = activeConversation.scrollHeight;
}


// Dropdowns
function generatePromptDropdownOptions(mode) {
  switch (mode) {
    case "pronunciation":
      return pronunciationDropdownOptions;
    case "context":
      return contextDropdownOptions;
    case "reading":
      return readingDropdownOptions;
    default:
      return '';
  }
}



//Inputs
function clearUserChatInput() {
  const userInput = document.getElementById('user-input');
  userInput.value = "";
}

function getStudyPlanInputValues() {
  const englishLevel = document.getElementById('english-level').value;
  const goals = Array.from(document.querySelectorAll('input[name="goals[]"]:checked')).map(el => el.value);
  const otherInput = document.getElementById('other-input').value;
  const startDate = document.getElementById('start-date').value;
  const endDate = document.getElementById('end-date').value;
  const days = document.getElementById('days').value;
  const hours = document.getElementById('hours').value;

  return {
    englishLevel,
    goals,
    otherInput,
    startDate,
    endDate,
    days,
    hours
  };
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
      timerElement.textContent = "00:00";
      timesupContainer.style.display = 'block';
      spanCountdown(textSpanCountdown);
    }
  }, 1000);
}

  
  function spanCountdown(textSpanCountdown) {
    var body = document.querySelector('body');
    body.classList.add('disable-selection');

    const alertOk = document.querySelector('#alert-ok');

    var countdownElement = document.getElementById("span-countdown");
    var countdownValue = textSpanCountdown
  
    var countdownInterval = setInterval(function() {
      countdownValue--;
      countdownElement.textContent = countdownValue;
  
      if (countdownValue <= 0) {
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
    
    // Disable text selection
    var body = document.querySelector('body');
    body.classList.add('disable-selection');

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


  function getEnglishLevelAndSetItToDropdown() {
    fetch('/get-english-level')
      .then(response => response.json())
      .then(data => {
        const englishLevelDropdown = document.getElementById('english-level');
        const englishLevelFromDatabase = data.englishLevel;
        
        // Cek apakah nilai ada dalam dropdown
        const optionExists = Array.from(englishLevelDropdown.options).some(option => option.value === englishLevelFromDatabase);
  
        if (!optionExists) {
          const newOption = new Option(englishLevelFromDatabase, englishLevelFromDatabase);
          englishLevelDropdown.add(newOption);
        }
  
        englishLevelDropdown.value = englishLevelFromDatabase;
      })
      .catch(error => {
        console.error('Failed to fetch English level from database:', error);
      });
  }
  



//Export
export {
  addLoader,
  clearUserChatInput,
  createBubble,
  generatePromptDropdownOptions,
  getChatHistory,
  getEnglishLevelAndSetItToDropdown,
  getStudyPlanInputValues,
  getQuestions,
  placementTestCountdown,
  removeLoader,
  getResult,
  spanCountdown,
  submitAnswers
};

  