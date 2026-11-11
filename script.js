// ===== Menú móvil =====
const toggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");

toggle.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");
  toggle.classList.toggle("open", isOpen);
  toggle.setAttribute("aria-expanded", isOpen);
});

// Cerrar el menú al hacer clic en un enlace
navLinks.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.classList.remove("open");
    toggle.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  });
});

// ===== Sombra del header al hacer scroll =====
const header = document.querySelector(".header");
window.addEventListener("scroll", () => {
  header.classList.toggle("scrolled", window.scrollY > 10);
});

// ===== Animación de aparición al hacer scroll =====
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);

document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));

// ===== Formulario de suscripción =====
const form = document.querySelector(".cta-form");
const emailInput = document.getElementById("email");
const msg = document.querySelector(".form-msg");
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const email = emailInput.value.trim();

  if (!emailRegex.test(email)) {
    emailInput.classList.add("invalid");
    msg.textContent = "Por favor ingresa un correo válido.";
    return;
  }

  emailInput.classList.remove("invalid");
  msg.textContent = `¡Gracias! Te escribiremos a ${email}.`;
  form.reset();
});

// ===== Año actual en el footer =====
document.getElementById("year").textContent = new Date().getFullYear();
