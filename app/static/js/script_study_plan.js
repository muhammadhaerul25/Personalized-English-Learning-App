const planContainer = document.querySelector('.plan-container');

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

const form = document.getElementById('study-plan-form');

form.addEventListener('submit', async (event) => {
    addLoader();
    event.preventDefault(); // Prevent the default form submit behavior

    // Get the input values
    const englishLevel = document.getElementById('english-level').value;
    const goals = Array.from(document.querySelectorAll('input[name="goals[]"]:checked')).map(el => el.value);
    const otherInput = document.getElementById('other-input').value;
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const days = document.getElementById('days').value;
    const hours = document.getElementById('hours').value;

    // Send the data to the server using the fetch API
    const response = await fetch('/create-study-plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            englishLevel,
            goals,
            otherInput,
            startDate,
            endDate,
            days,
            hours
        })
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
    planContainer.appendChild(bubble);

});




//BUTTONS
const submitButton = document.querySelector('.submit-button');




