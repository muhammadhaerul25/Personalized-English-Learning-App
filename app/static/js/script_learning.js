import { createBubble, clearUserChatInput, generatePromptDropdownOptions,addLoader, removeLoader} from './helpers.js';
import { defaultMode } from './config.js';

// VARIABLES
const form = document.getElementById('user-form');
const userInput = document.getElementById('user-input');
const modeInput = document.getElementById('mode');


// EVENTS
// event pada saat chat dikirim
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
      activeConversation.scrollTop = activeConversation.scrollHeight;
    })
    .catch(error => console.error(error));
  }
});


// event pada saat tab diubah
const tabs = document.querySelectorAll('.tablink');
tabs.forEach(tab => {
  tab.addEventListener('click', function() {

    const activeTab = document.querySelector('.tablink.active');
    activeTab.classList.remove('active');
    this.classList.add('active');
    const mode = this.getAttribute('data-mode');

    modeInput.value = mode;
    clearUserChatInput();
    dropdown.innerHTML = generatePromptDropdownOptions(mode);

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



// DROPDOWN
const dropdown = document.getElementById('message-options-dropdown');
dropdown.innerHTML = generatePromptDropdownOptions(defaultMode);

dropdown.addEventListener('change', function() {
  userInput.value = dropdown.value;
});



