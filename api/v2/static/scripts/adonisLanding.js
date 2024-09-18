// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

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

$(document).ready(function() {
    $('.toggle-link').on('click', function(e) {
        e.preventDefault();
        console.log('Toggle link clicked'); // Debug log
        console.log('Target:', $(this).data('target')); // Debug log
        $('.auth-container').removeClass('active');
        $($(this).data('target')).addClass('active');
        console.log('Active class added to:', $(this).data('target')); // Debug log
    });

    $('#openLoginModal').on('click', function() {
        console.log('Login button clicked'); // Debug log
        $('.auth-container').removeClass('active');
        $('#login-container').addClass('active');
    });
});