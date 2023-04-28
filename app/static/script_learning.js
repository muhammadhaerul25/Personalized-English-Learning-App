// VARIABLES
const form = document.getElementById('user-form');
const userInput = document.getElementById('user-input');
const modeInput = document.getElementById('mode');

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

function createBubble(sender, message) {
  const bubble = document.createElement('div');
  bubble.classList.add('message', sender);
  const paragraphs = message.split('\n');
  paragraphs.forEach(paragraph => {
    if (paragraph.trim() !== '') {
      const p = document.createElement('p');
      p.textContent = paragraph.trim();
      bubble.appendChild(p);
    }

    // if (paragraph !== paragraphs[paragraphs.length - 1]) {
    //   const lineBreak = document.createElement('br');
    //   bubble.appendChild(lineBreak);
    // }
  });
  return bubble;
}



// EVENTS
// event pada saat tab diubah
const tabs = document.querySelectorAll('.tablink');
tabs.forEach(tab => {
  tab.addEventListener('click', function() {
    const activeTab = document.querySelector('.tablink.active');
    activeTab.classList.remove('active');
    this.classList.add('active');
    const mode = this.getAttribute('data-mode');
    modeInput.value = mode;
    const activeConversation = document.querySelector('.conversation.active');
    activeConversation.classList.remove('active');
    const targetConversation = document.getElementById(mode);
    targetConversation.classList.add('active');
  });
});

// event pada saat form dikirim
form.addEventListener('submit', function(e) {
  e.preventDefault();
  const message = userInput.value.trim();
  if (message !== '') {
    const userBubble = createBubble('user', message);
    const activeConversation = document.querySelector('.conversation.active');
    activeConversation.appendChild(userBubble);
    userInput.value = '';
    addLoader();

    fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_input: message, mode: modeInput.value })
    })
    .then(response => response.json())
    .then(data => {
      const botBubble = createBubble('bot', data.message);
      activeConversation.appendChild(botBubble);
      removeLoader();

      // menggulir ke bawah setelah chat diterima
      activeConversation.scrollTop = activeConversation.scrollHeight;
    })
    .catch(error => console.error(error));
  }
});


// BUTTONS
// exit button
const exitButton = document.getElementById('exit-button');
const alertDialog = document.getElementById('alert-dialog');
const alertOkButton = document.getElementById('alert-ok');
const alertCancelButton = document.getElementById('alert-cancel');

exitButton.addEventListener('click', function() {
  alertDialog.classList.remove('hide');
});

alertOkButton.addEventListener('click', function() {
  window.location.href = "/";
});

alertCancelButton.addEventListener('click', function() {
  alertDialog.classList.add('hide');
});


// DROPDOWN
const dropdown = document.getElementById('message-options-dropdown');

dropdown.addEventListener('change', function() {
  userInput.value = dropdown.value;
});

// Generate dropdown for Pronunciation tab when page loads
for (var i = 0; i < tabs.length; i++) {
  tabs[i].addEventListener("click", function() {
    // get the selected mode from the tab data attribute
    var mode = this.getAttribute("data-mode");
    
    // update dropdown options based on selected mode
    switch (mode) {
      case "pronunciation":
        dropdown.innerHTML = `
          <option value="">Select a prompt</option>
          <option value="pronunciation-option-1">Pronunciation option 1</option>
          <option value="pronunciation-option-2">Pronunciation option 2</option>
          <option value="pronunciation-option-3">Pronunciation option 3</option>
        `;
        break;
      case "context":
        dropdown.innerHTML = `
          <option value="">Select a prompt</option>
          <option value="context-option-1">Context option 1</option>
          <option value="context-option-2">Context option 2</option>
          <option value="context-option-3">Context option 3</option>
        `;
        break;
      case "reading":
        dropdown.innerHTML = `
          <option value="">Select a prompt</option>
          <option value="reading-option-1">Reading option 1</option>
          <option value="reading-option-2">Reading option 2</option>
          <option value="reading-option-3">Reading option 3</option>
        `;
        break;
    }
  });
}

// // Text History
// // saat halaman akan ditutup atau di-refresh
// window.addEventListener('beforeunload', function() {
//   sessionStorage.setItem('userInput', userInput.value);
// });

// // saat halaman dimuat kembali
// window.addEventListener('load', function() {
//   const savedInput = sessionStorage.getItem('userInput');
//   if (savedInput) {
//     userInput.value = savedInput;
//   }
// });





