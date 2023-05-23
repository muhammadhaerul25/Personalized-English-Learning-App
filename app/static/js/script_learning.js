// VARIABLES
const form = document.getElementById('user-form');
const userInput = document.getElementById('user-input');
const modeInput = document.getElementById('mode');
const dataChatHistory = [];
// let dataChatHistory = [];

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

function clearInput() {
  userInput.value = "";
}

function createBubble(sender, message) {
  const bubble = document.createElement('div');
  bubble.classList.add('message', sender);
  bubble.innerHTML = message.replace(/\n/g, '<br>');

  return bubble;
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

// Fungsi untuk mengambil riwayat chat dari server
function getChatHistory() {
  fetch('/chat-history')
    .then(response => response.json())
    .then(data => {
      console.log(data);
      dataChatHistory.push(data.chat_history);
      displayChatHistory(dataChatHistory[0], 'pronunciation');
    })
    .catch(error => console.error(error));
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
  // getChatHistory();
  // displayChatHistory(dataChatHistory[0], tabName);
}





// EVENTS
// event pada saat tab diubah
const tabs = document.querySelectorAll('.tablink');
const conversations = document.querySelectorAll('.conversation');
tabs.forEach(tab => {
  tab.addEventListener('click', function() {

    const activeTab = document.querySelector('.tablink.active');
    activeTab.classList.remove('active');
    this.classList.add('active');
    const mode = this.getAttribute('data-mode');

    modeInput.value = mode;
    clearInput();

    const activeConversation = document.querySelector('.conversation.active');
    activeConversation.classList.remove('active', 'fade-out');
    activeConversation.classList.add('fade-out');
    setTimeout(() => {
      activeConversation.classList.remove('fade-out');
      activeConversation.classList.remove('active');
      const targetConversation = document.getElementById(mode);
      targetConversation.classList.add('active', 'fade-in');
      setTimeout(() => {
        targetConversation.classList.remove('fade-in');
      }, 500);
    }, 500);
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
    activeConversation.scrollTop = activeConversation.scrollHeight;
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



// DROPDOWN
const dropdown = document.getElementById('message-options-dropdown');

dropdown.addEventListener('change', function() {
  userInput.value = dropdown.value;
});



//MAIN
// Tampilkan riwayat chat saat halaman dimuat
// getChatHistory();



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
        <option value="Explain who are you and what can you do?">Explain who are you and what can you do?</option>
        <option value="Explain my English level and how can I improve it">Explain my English level and how can I improve it</option>
        <option value="Recall what I learned last time">Recall what I learned last time</option>
        <option value="I want to learn about ...">I want to learn about ...</option>
        <option value="Give me lesson about...">Give me lesson about ...</option>
        <option value="Let's have a conversation about ...">Let's have a conversation about ...</option>
        <option value="Let's have a conversation about ... and suggest different vocabularies">Let's have a conversation about ... and suggest different vocabularies</option>
        <option value="Let's have a conversation about ... and correct my mistakes">Let's have a conversation about ... and correct my mistakes</option>
        <option value="Write a conversation about ...">Write a conversation about ...</option>
        <option value="Write a conversation between ...">Write a conversation between ...</option>
        <option value="Let's simulate an interview for">Let's simulate a interview for</option>
        <option value="Let's practice">Let's practice</option>
        <option value="Give me feedbacks">Give me feedbacks</option>
        `;
        break;
      case "context":
        dropdown.innerHTML = `
          <option value="">Select a prompt</option>
          <option value="Explain who are you and what can you do?">Explain who are you and what can you do?</option>
          <option value="Explain my English level and how can I improve it">Explain my English level and how can I improve it</option>
          <option value="Recall what I learned last time">Recall what I learned last time</option>
          <option value="I want to learn about ...">I want to learn about ...</option>
          <option value="Give me lesson about...">Give me lesson about ...</option>
          <option value="Explain about ...">Explain about ...</option>
          <option value="What is the meaning of ...">What is the meaning of ...</option>
          <option value="Write sentences using ...">Write sentences using ...</option>
          <option value="Correct my grammar mistakes in the following text: ...">Correct my grammar mistakes in the following text: ...</option>
          <option value="Write sentences using ...">Write sentences using ...</option>
          <option value="Let's practice">Let's practice</option>
          <option value="Give me feedbacks">Give me feedbacks</option>
        `;
        break;
      case "reading":
        dropdown.innerHTML = `
          <option value="">Select a prompt</option>
          <option value="Explain who are you and what can you do?">Explain who are you and what can you do?</option>
          <option value="Explain my English level and how can I improve it">Explain my English level and how can I improve it</option>
          <option value="Recall what I learned last time">Recall what I learned last time</option>
          <option value="I want to learn about ...">I want to learn about ...</option>
          <option value="Give me lesson about ...">Give me lesson about ...</option>
          <option value="Write a text about ...">Write a text about ...</option>
          <option value="Explain this text: ...">Explain this text: ...</option>
          <option value="Simplify this text: ...">Simplify this text: ...</option>
          <option value="Beautify this text: ...">Beautify this text: ...</option>
          <option value="Summarize this text: ...">Summarize this text: ...</option>
          <option value="Conclude this text: ...">Conclude this text: ...</option>
          <option value="Let's practice">Let's practice</option>
          <option value="Give me feedbacks">Give me feedbacks</option>
        `;
        break;
    }
  });
}


