import { getStudyPlanInputValues, getEnglishLevelAndSetItToDropdown,addLoader, removeLoader} from './helpers.js';

// VARIABLES
const planContainer = document.querySelector('.plan-container');
const bubbleContainer = document.getElementById('bubble-container');
const saveButton = document.getElementById('save-button');
const successMessage = document.getElementById('success-message');
const form = document.getElementById('study-plan-form');



//EVENTS
getEnglishLevelAndSetItToDropdown()


// Event of create study plan
form.addEventListener('submit', async (event) => {
    addLoader();
    event.preventDefault(); 

    const inputValues = getStudyPlanInputValues();

    const response = await fetch('/create-study-plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(inputValues)
    });

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



// Event of save the study plan to the database
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
      successMessage.textContent = 'Success to save study plan!';
      successMessage.style.display = 'block';
      setTimeout(() => {
        successMessage.style.display = 'none';
      }, 3000); // Hide the success message after 3 seconds
    } else {
      window.scrollTo(0, 0);
      successMessage.textContent = 'Failed to save study plan!';
      successMessage.style.display = 'block';
      setTimeout(() => {
        successMessage.style.display = 'none';
      }, 3000); // Hide the success message after 3 seconds
    }
  })
  .catch(error => {
    console.error('Error saving study plan:', error);
  });
});










