// VARIABLES
const planContainer = document.querySelector('.plan-container');
const bubbleContainer = document.getElementById('bubble-container');
const saveButton = document.getElementById('save-button');
const successMessage = document.getElementById('success-message');
const form = document.getElementById('study-plan-form');


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

function getInputValues() {
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



//EVENTS
form.addEventListener('submit', async (event) => {
    addLoader();
    event.preventDefault(); // Prevent the default form submit behavior

    // Get the input values
    const inputValues = getInputValues();

    // Send the data to the server using the fetch API
    const response = await fetch('/create-study-plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(inputValues)
    });

    // Get the response from the server and display it
    const responseData = await response.json();
    console.log(responseData);
    removeLoader();

    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    const bubbleText = document.createElement('p');
    bubbleText.innerHTML = responseData.study_plan.replace(/\n/g, '<br>'); // Tambahkan tag br setelah setiap opsi
    bubble.appendChild(bubbleText);
    planContainer.prepend(bubble);
    saveButton.style.display = 'block';
});


// Save the study plan to the database
saveButton.addEventListener('click', () => {
  const bubbleText = document.querySelector('.bubble p').innerHTML;
  const studyPlan = { study_plan: bubbleText };
  
  fetch('/save-study-plan', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(studyPlan)
  })
  .then(response => {
    if (response.ok) {
      window.scrollTo(0, 0);
      successMessage.textContent = 'Study plan successfully!';
      successMessage.style.display = 'block';
      setTimeout(() => {
        successMessage.style.display = 'none';
      }, 3000); // Hide the success message after 3 seconds
    } else {
      console.error('Failed to save study plan.');
    }
  })
  .catch(error => {
    console.error('Error saving study plan:', error);
  });
});


//Get english level from database
fetch('/get-english-level')
  .then(response => response.json())
  .then(data => {
    const englishLevelDropdown = document.getElementById('english-level');
    const englishLevelFromDatabase = data.englishLevel;
    
    // Cek apakah nilai ada dalam dropdown
    let optionExists = false;
    for (let i = 0; i < englishLevelDropdown.options.length; i++) {
      if (englishLevelDropdown.options[i].value === englishLevelFromDatabase) {
        englishLevelDropdown.value = englishLevelFromDatabase;
        optionExists = true;
        break;
      }
    }

    // Jika nilai tidak ada dalam dropdown, tambahkan opsi baru
    if (!optionExists) {
      const newOption = document.createElement('option');
      newOption.value = englishLevelFromDatabase;
      newOption.text = englishLevelFromDatabase; // Gunakan properti 'text' untuk menambahkan teks pada opsi
      englishLevelDropdown.appendChild(newOption);
      englishLevelDropdown.value = englishLevelFromDatabase;
    }


  })
  .catch(error => {
    console.error('Failed to fetch English level from database:', error);
});





//BUTTONS
const submitButton = document.querySelector('.submit-button');




