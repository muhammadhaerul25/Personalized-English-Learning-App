function startCountdown() {
  setTimeout(function() {
    var countDownDate = new Date().getTime() + 10000; // 10 minutes from now

    var timerElement = document.getElementById("timer");

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
        // Time countdown is finished, perform further actions here
        timerElement.textContent = "Time's up!";
        alertOk.click();
      }
    }, 1000);
  }, 0); // 5-second delay before starting the countdown
}


// Export the function to make it accessible to other files
export { startCountdown };

  