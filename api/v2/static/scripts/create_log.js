document.getElementById('create-log-form').addEventListener('submit', function (event) {
  event.preventDefault();

  const formData = new FormData(this);

  fetch(this.action, {
    method: 'POST',
    body: formData
  })
    .then(response => {
      if (response.redirected) {
        window.location.href = response.url;  // Follow the redirect manually
      } else {
        return response.json();  // Handle JSON if no redirect
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
});

function toggleCustomHabit() {
  const habitType = document.getElementById('habit_type').value;
  const customFields = document.getElementById('custom-habit-fields');
  customFields.style.display = (habitType === 'custom') ? 'block' : 'none';
}
