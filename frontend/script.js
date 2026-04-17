const API_BASE = "http://127.0.0.1:8000";
const sessionId = "faiz-session-001";

function addMessage(role, text) {
  const chatBox = document.getElementById("chatBox");
  const div = document.createElement("div");
  div.className = "message";

  if (role === "user") {
    div.innerHTML = `<span class="user">You:</span> ${text}`;
  } else {
    div.innerHTML = `<span class="assistant">FaizGPT:</span> ${text}`;
  }

  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();

  if (!message) return;

  addMessage("user", message);
  input.value = "";

  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id: sessionId,
        message: message
      })
    });

    const data = await response.json();

    if (response.ok) {
      addMessage("assistant", data.response);
    } else {
      addMessage("assistant", `Error: ${data.detail || "Request failed."}`);
    }
  } catch (error) {
    addMessage("assistant", "Error: Could not reach backend.");
  }
}

async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("status");

  if (!fileInput.files.length) {
    status.textContent = "Please choose a file first.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (response.ok) {
      status.textContent = `Uploaded: ${data.filename}`;
    } else {
      status.textContent = `Upload failed: ${data.detail || "Request failed."}`;
    }
  } catch (error) {
    status.textContent = "Upload error: backend unreachable.";
  }
}