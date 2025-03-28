// script.js
document.addEventListener("DOMContentLoaded", function() {
    // Mobile menu functionality
    const navbarToggle = document.querySelector('.btn-navbar');
    const navCollapse = document.querySelector('.nav-collapse');
    
    if(navbarToggle && navCollapse) {
        navbarToggle.addEventListener('click', function() {
            navCollapse.classList.toggle('in');
        });
    }

    // Smooth scroll functionality
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if(target) {
                window.scrollTo({
                    top: target.offsetTop - 60,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Scrollspy initialization
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('.row-fluid');
        const navLinks = document.querySelectorAll('.nav a');
        
        sections.forEach(section => {
            const top = window.scrollY;
            const offset = section.offsetTop - 100;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');

            if(top >= offset && top < offset + height) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if(link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    });
});