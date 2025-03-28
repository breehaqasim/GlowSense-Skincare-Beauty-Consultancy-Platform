document.addEventListener("DOMContentLoaded", function() {
    // Example functionality: Display an alert when the consultation form is submitted
    const consultationForm = document.querySelector('form');
    consultationForm.addEventListener('submit', function(event) {
        event.preventDefault();
        alert('Thank you for submitting your skincare concerns!');
    });
});
