document.addEventListener("DOMContentLoaded", () => {
  const loginContainer = document.getElementById("login-container");
  const chatContainer = document.getElementById("chat-container");
  const uploadPopup = document.getElementById("upload-popup");
  const chatBox = document.getElementById("chat-box");
  const input = document.getElementById("query");

  // === Fake session to simulate login (API integration can replace this) ===
  async function login() {
  const user = document.getElementById("username").value.trim();
  const pwd = document.getElementById("password").value.trim();

  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",  // ✅ Important: send cookies
      body: JSON.stringify({ username: user, password: pwd })
    });

    const data = await response.json();

    if (response.ok) {
      loginContainer.classList.add("hidden");
      chatContainer.classList.remove("hidden");
    } else {
      document.getElementById("login-error").innerText = data.error || "Invalid credentials";
    }
  } catch (err) {
    document.getElementById("login-error").innerText = "Server error during login";
  }
}


  window.login = login;
  // === Logout API ===
  async function logout() {
    try {
      const res = await fetch("/logout", {
        method: "POST",
        credentials: "include"
      });

      const data = await res.json();
      if (res.ok) {
        alert(data.message || "Logged out");
        location.reload(); // reloads to show login screen
      } else {
        alert(data.error || "Logout failed");
      }
    } catch (err) {
      alert("Error during logout.");
    }
  }

  window.logout = logout;

  // === Send Query ===
  async function sendQuery() {
    const question = input.value.trim();
    if (!question) return;

    appendMessage("user", question);
    input.value = "";

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ query: question })
      });

      const data = await response.json();
      if (response.ok) {
        appendMessage("bot", data.response);
      } else {
        appendMessage("bot", data.error || "An error occurred.");
      }
    } catch (err) {
      appendMessage("bot", "Server error. Try again later.");
    }
  }

  window.sendQuery = sendQuery;

  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // === Upload Handling ===
  function toggleUpload() {
    uploadPopup.classList.toggle("hidden");
  }

  window.toggleUpload = toggleUpload;

  async function uploadFile() {
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/upload", {
        method: "POST",
        credentials: "include",
        body: formData
      });

      if (res.redirected) {
        toggleUpload();
        alert("File uploaded and processed!");
      } else {
        alert("Upload failed. Make sure you're logged in.");
      }
    } catch (err) {
      alert("Error uploading file.");
    }
  }

  window.uploadFile = uploadFile;
});
