const loginForm = document.getElementById("loginForm");
const submitBtn = document.getElementById("submitBtn");
const loginStatus = document.getElementById("loginStatus");
const formTitle = document.getElementById("formTitle");
const fullNameGroup = document.getElementById("fullNameGroup");
const toggleModeLink = document.getElementById("toggleModeLink");

let isSignupMode = false;

toggleModeLink.addEventListener("click", (event) => {
  event.preventDefault();
  isSignupMode = !isSignupMode;

  if (isSignupMode) {
    formTitle.textContent = "Sign Up";
    submitBtn.textContent = "Sign Up";
    fullNameGroup.classList.remove("hidden");
    toggleModeLink.textContent = "Already have an account? Login";
  } else {
    formTitle.textContent = "Login";
    submitBtn.textContent = "Login";
    fullNameGroup.classList.add("hidden");
    toggleModeLink.textContent = "Don't have an account? Sign up";
  }
});

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const fullName = document.getElementById("fullName").value.trim();

  setSubmitting(true);
  hideStatus();

  const endpoint = isSignupMode ? "/api/auth/signup" : "/api/auth/login";
  const payload = isSignupMode
    ? { email, password, full_name: fullName || null }
    : { email, password };

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Authentication failed");
    }

    saveAuth(data.access_token, data.user);
    showStatus(`Welcome, ${data.user.full_name || data.user.email}! Redirecting...`, "success");

    setTimeout(() => {
      window.location.href = "dashboard.html";
    }, 1000);

  } catch (error) {
    showStatus(`Error: ${error.message}`, "error");
    console.error("Auth error:", error);
  } finally {
    setSubmitting(false);
  }
});

function setSubmitting(isSubmitting) {
  submitBtn.disabled = isSubmitting;
}

function showStatus(message, type) {
  loginStatus.textContent = message;
  loginStatus.className = `upload-status ${type}`;
}

function hideStatus() {
  loginStatus.className = "upload-status hidden";
}