
  document.addEventListener('DOMContentLoaded', () => {
    const messages = document.querySelectorAll('.message-box');
    messages.forEach((msg, index) => {
      setTimeout(() => {
        msg.classList.add('fade-out');
        setTimeout(() => msg.remove(), 500); // remove from DOM after fade
      }, 3000); // 3 seconds
    });
  });

