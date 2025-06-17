/**
 * This script handles the client-side functionality for a chat application.
 * It includes login/logout, chat messaging, and file upload capabilities.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const loginContainer = document.getElementById("login-container");
  const chatContainer = document.getElementById("chat-container");
  const uploadPopup = document.getElementById("upload-popup");
  const chatBox = document.getElementById("chat-box");
  const input = document.getElementById("query");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  const fileInput = document.getElementById("file-input");
  const uploadZone = document.querySelector(".upload-zone");

  /**
   * Event listener for Enter key on login form fields.
   * Moves focus to the password field when Enter is pressed in the username field.
   * Attempts login when Enter is pressed in the password field.
   */
  usernameInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      passwordInput.focus();
    }
  });

  passwordInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      login();
    }
  });

  /**
   * Event listener for Enter key on chat input field.
   * Sends the chat query when Enter is pressed.
   */
  input.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      sendQuery();
    }
  });

  /**
   * Sets up drag and drop functionality for file uploads.
   * Changes visual feedback during drag and drop operations.
   */
  function setupDragAndDrop() {
    uploadZone.addEventListener("click", () => fileInput.click());

    uploadZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      uploadZone.style.borderColor = "#b71c1c";
      uploadZone.style.backgroundColor = "rgba(211, 47, 47, 0.05)";
    });

    uploadZone.addEventListener("dragleave", () => {
      uploadZone.style.borderColor = "#d32f2f";
      uploadZone.style.backgroundColor = "transparent";
    });

    uploadZone.addEventListener("drop", (e) => {
      e.preventDefault();
      uploadZone.style.borderColor = "#d32f2f";
      uploadZone.style.backgroundColor = "transparent";

      if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        uploadFile();
      }
    });
  }

  // Initialize drag and drop
  setupDragAndDrop();

  /**
   * Handles user login.
   * Validates input fields and sends a login request to the server.
   * On success, switches from login view to chat view.
   */
  async function login() {
    const user = usernameInput.value.trim();
    const pwd = passwordInput.value.trim();

    if (!user || !pwd) {
      document.getElementById("login-error").innerText = "Please enter both username and password";
      return;
    }

    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username: user, password: pwd })
      });

      const data = await response.json();

      if (response.ok) {
        loginContainer.classList.add("hidden");
        chatContainer.classList.remove("hidden");
        document.getElementById("login-error").innerText = "";
      } else {
        document.getElementById("login-error").innerText = data.error || "Invalid credentials";
      }
    } catch (err) {
      document.getElementById("login-error").innerText = "Server error during login";
      console.error("Login error:", err);
    }
  }

  window.login = login;

  /**
   * Handles user logout.
   * Sends a logout request to the server and switches back to login view.
   */
  async function logout() {
    try {
      const res = await fetch("/logout", {
        method: "POST",
        credentials: "include"
      });

      const data = await res.json();
      if (res.ok) {
        chatContainer.classList.add("hidden");
        loginContainer.classList.remove("hidden");
        document.getElementById("username").value = "";
        document.getElementById("password").value = "";
      } else {
        console.error("Logout failed:", data.error);
      }
    } catch (err) {
      console.error("Error during logout:", err);
    }
  }

  window.logout = logout;

  /**
   * Sends a chat query to the server.
   * Appends the user's message to the chat box and sends the query to the server.
   * On receiving a response, appends the bot's reply to the chat box.
   */
  async function sendQuery() {
    const question = input.value.trim();
    if (!question) return;

    appendMessage("user", question);
    input.value = "";

    // Disable input while waiting for response
    input.disabled = true;

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
        appendMessage("bot", data.error || "An error occurred while processing your request.");
      }
    } catch (err) {
      console.error("Error sending query:", err);
      appendMessage("bot", "Sorry, I'm having trouble connecting to the server. Please try again later.");
    } finally {
      input.disabled = false;
      input.focus();
    }
  }

  window.sendQuery = sendQuery;

  /**
   * Appends a message to the chat box with a timestamp.
   * @param {string} sender - The sender of the message ("user" or "bot").
   * @param {string} text - The text content of the message.
   */
  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;

    const textElement = document.createElement("div");
    textElement.className = "message-text";
    textElement.innerText = text;

    const timeElement = document.createElement("div");
    timeElement.className = "message-time";
    timeElement.innerText = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    msg.appendChild(textElement);
    msg.appendChild(timeElement);
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  /**
   * Toggles the visibility of the upload popup.
   * Resets the file input when closing the popup.
   */
  function toggleUpload() {
    uploadPopup.classList.toggle("hidden");
    // Reset file input when closing
    if (!uploadPopup.classList.contains("hidden")) {
      fileInput.value = "";
    }
  }

  window.toggleUpload = toggleUpload;

  /**
   * Handles file uploads.
   * Validates the file type and size, then sends the file to the server.
   * On success, appends a confirmation message to the chat box.
   */
  async function uploadFile() {
    const file = fileInput.files[0];

    if (!file) {
      alert("Please select a file first");
      return;
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      alert("File size exceeds 10MB limit");
      return;
    }

    const validTypes = ["application/pdf", "text/plain"];
    if (!validTypes.includes(file.type)) {
      alert("Please upload only PDF or TXT files");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    // Show loading state
    const uploadBtn = document.querySelector(".upload-btn");
    const originalBtnText = uploadBtn.innerText;
    uploadBtn.disabled = true;
    uploadBtn.innerText = "Uploading...";

    try {
      const res = await fetch("/upload", {
        method: "POST",
        credentials: "include",
        body: formData
      });

      if (res.ok) {
        const data = await res.json();
        toggleUpload();
        appendMessage("bot", `File uploaded successfully: ${file.name}`);
      } else {
        const data = await res.json();
        alert(data.error || "Upload failed. Please try again.");
      }
    } catch (err) {
      console.error("Upload error:", err);
      alert("Error uploading file. Please check your connection and try again.");
    } finally {
      // Reset button state
      uploadBtn.disabled = false;
      uploadBtn.innerText = originalBtnText;
    }
  }

  window.uploadFile = uploadFile;

  // Add welcome message to the chat box
  const welcomeMessage = document.createElement("div");
  welcomeMessage.className = "welcome-message";
  welcomeMessage.innerHTML = `
    <h3>Welcome to ChatFlow</h3>
    <p>How can I help you today?</p>
  `;
  chatBox.appendChild(welcomeMessage);
});
