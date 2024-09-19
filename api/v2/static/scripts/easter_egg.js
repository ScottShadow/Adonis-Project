document.getElementById('quiz-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const answer = document.getElementById('question').value.toLowerCase();
  const correctAnswer = "easter";

  if (answer === correctAnswer) {
    document.getElementById('response-message').innerText = "Correct! You've unlocked the Easter Egg!";
    document.getElementById('easter-egg').classList.remove('hidden');
  } else {
    document.getElementById('response-message').innerText = "Oops! Try again.";
    document.getElementById('easter-egg').classList.add('hidden');
  }
});
