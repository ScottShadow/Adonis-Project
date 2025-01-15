document.getElementById('update-log-form').addEventListener('submit', function (event) {
  //event.preventDefault();

  const formData = new FormData(this);

  fetch(this.action, {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      const messageDiv = document.getElementById('response-message');
      if (data.error) {
        messageDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
      } else {
        messageDiv.innerHTML = `<p style="color:green;">${data.message}</p>`;
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
});
