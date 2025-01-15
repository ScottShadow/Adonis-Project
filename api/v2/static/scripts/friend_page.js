function showSection(sectionId) {
  const sections = document.querySelectorAll('.friends-container section');
  sections.forEach(section => {
    if (section.id === sectionId) {
      section.classList.remove('hidden');
    } else {
      section.classList.add('hidden');
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const ajaxForms = document.querySelectorAll(".ajax-action-form");

  ajaxForms.forEach(form => {
    form.addEventListener("submit", async event => {
      event.preventDefault(); // Prevent default form submission
      const actionUrl = form.getAttribute("action");
      const formData = new FormData(form);

      try {
        const response = await fetch(actionUrl, {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          // Reload the page on success
          location.reload();
        } else {
          console.error("Failed to process the request.");
        }
      } catch (error) {
        console.error("Error occurred:", error);
      }
    });
  });
});
