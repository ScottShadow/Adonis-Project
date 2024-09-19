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
