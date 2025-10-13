// welcome.js
document.addEventListener('DOMContentLoaded', () => {
  const btns = document.querySelectorAll('.welcome-btn');
  btns.forEach(btn => {
    btn.style.animation = 'pulse 2.5s ease-in-out infinite alternate';
  });
});

const style = document.createElement('style');
style.textContent = `
@keyframes pulse {
  0% { box-shadow: 0 0 12px rgba(102, 204, 204, 0.4); }
  100% { box-shadow: 0 0 28px rgba(102, 204, 204, 0.7); }
}`;
document.head.appendChild(style);
