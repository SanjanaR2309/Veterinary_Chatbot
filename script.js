const form = document.getElementById("chatForm");
const responseDiv = document.getElementById("response");
const themeToggle = document.getElementById("themeToggle");

form.onsubmit = async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const res = await fetch("/ask", {
    method: "POST",
    body: formData
  });
  const data = await res.json();
  responseDiv.textContent = data.response;
  responseDiv.classList.add('response-color');
};

themeToggle.onclick = () => {
  document.body.classList.toggle('dark-theme');
  const isDark = document.body.classList.contains('dark-theme');
  themeToggle.textContent = isDark ? 'Switch to Bright Theme' : 'Switch to Dark Theme';
};
