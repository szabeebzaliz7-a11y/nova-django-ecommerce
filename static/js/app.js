document.addEventListener("DOMContentLoaded", () => {
    const menu = document.getElementById("mainNav");
    const toggle = document.getElementById("menuToggle");
    if (toggle && menu) {
        toggle.addEventListener("click", () => menu.classList.toggle("open"));
    }

    const slides = [...document.querySelectorAll(".hero-slide")];
    const dots = [...document.querySelectorAll(".slider-dots button")];
    let current = 0;
    let timer;

    function showSlide(index) {
        if (!slides.length) return;
        current = (index + slides.length) % slides.length;
        slides.forEach((slide, i) => slide.classList.toggle("active", i === current));
        dots.forEach((dot, i) => dot.classList.toggle("active", i === current));
    }

    function startSlider() {
        if (slides.length > 1) {
            timer = setInterval(() => showSlide(current + 1), 5000);
        }
    }

    dots.forEach((dot) => {
        dot.addEventListener("click", () => {
            clearInterval(timer);
            showSlide(Number(dot.dataset.slide));
            startSlider();
        });
    });
    startSlider();

    document.querySelectorAll(".flash").forEach((el) => {
        setTimeout(() => {
            el.style.opacity = "0";
            setTimeout(() => el.remove(), 400);
        }, 3500);
    });
});
