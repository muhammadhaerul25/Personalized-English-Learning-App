import { getQuestions, submitAnswers } from './helpers.js';


//MAIN
getQuestions('/section1');


//BUTTONS
const form = document.getElementById('answer-form');
const submitButton = document.querySelector('.submit-button');
const alertDialog = document.querySelector('#alert-dialog');
const alertOk = document.querySelector('#alert-ok');
const alertCancel = document.querySelector('#alert-cancel');

submitButton.addEventListener('click', function(event) {
  event.preventDefault();
  alertDialog.classList.remove('hide');
});

alertCancel.addEventListener('click', function(event) {
  event.preventDefault();
  alertDialog.classList.add('hide');
});

alertOk.addEventListener('click', function(event) {
  event.preventDefault();
  submitAnswers(event, '/placement-test2');
});






