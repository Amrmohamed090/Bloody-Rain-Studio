let lastScrollTop = 0;
const navbar = document.getElementById('navbar');

window.addEventListener("scroll", () => {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop) {
        // Scrolling down
        navbar.style.transition = "top 0.5s ease-in-out"; // Add transition
        navbar.style.top = `-${navbar.offsetHeight}px`;
    } else {
        // Scrolling up
        navbar.style.transition = "top 0.5s ease-in-out"; // Add transition
        navbar.style.top = 0;
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
}, false);
