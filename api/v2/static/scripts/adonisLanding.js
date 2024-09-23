// Scripts
//

window.addEventListener('DOMContentLoaded', event => {

  // Collapse responsive navbar when toggler is visible
  const navbarToggler = document.body.querySelector('.navbar-toggler');
  const responsiveNavItems = [].slice.call(
    document.querySelectorAll('#navbarResponsive .nav-link')
  );
  responsiveNavItems.map(function (responsiveNavItem) {
    responsiveNavItem.addEventListener('click', () => {
      if (window.getComputedStyle(navbarToggler).display !== 'none') {
        navbarToggler.click();
      }
    });
  });

});

// jQuery for handling the toggling of login/signup containers
$(document).ready(function () {

  // Toggle between login and signup forms
  $('.toggle-link').on('click', function (e) {
    e.preventDefault();

    // Debug logs to help during development
    console.log('Toggle link clicked');
    console.log('Target:', $(this).data('target'));

    // Handle the container swapping
    $('.auth-container').removeClass('active');
    $($(this).data('target')).addClass('active');

    console.log('Active class added to:', $(this).data('target')); // Debug log
  });

  // Opens the login modal
  $('#openLoginModal').on('click', function () {
    console.log('Login button clicked'); // Debug log
    $('.auth-container').removeClass('active');
    $('#login-container').addClass('active');
  });

});
