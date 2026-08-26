const API_BASE_URL = "http://127.0.0.1:8000";

const eligibilityForm = document.getElementById("eligibilityForm");
const checkBtn = document.getElementById("checkBtn");
const resultBox = document.getElementById("resultBox");

eligibilityForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    scheme_name: document.getElementById("schemeName").value.trim(),
    age: parseInt(document.getElementById("age").value, 10),
    income: parseFloat(document.getElementById("income").value),
    category: document.getElementById("category").value.trim(),
    is_student: document.getElementById("isStudent").value === "true",
    state: document.getElementById("state").value.trim()
  };

  setChecking(true);
  hideResult();

  try {
    const response = await fetch(`${API_BASE_URL}/api/eligibility/check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Something went wrong");
    }

    renderResult(data);

  } catch (error) {
    renderError(error.message);
    console.error("Eligibility check error:", error);
  } finally {
    setChecking(false);
  }
});

function renderResult(data) {
  resultBox.className = data.eligible ? "eligibility-result eligible" : "eligibility-result not-eligible";

  let html = `<h3>${data.eligible ? "✅ You may be eligible" : "❌ You may not be eligible"}</h3>`;
  html += `<p>${escapeHtml(data.reason)}</p>`;

  if (data.required_documents && data.required_documents.length > 0) {
    html += `<p style="margin-top:10px;"><strong>Required documents:</strong></p>`;
    html += `<ul class="doc-list">`;
    data.required_documents.forEach((doc) => {
      html += `<li>${escapeHtml(doc)}</li>`;
    });
    html += `</ul>`;
  }

  resultBox.innerHTML = html;
  resultBox.classList.remove("hidden");
}

function renderError(message) {
  resultBox.className = "eligibility-result not-eligible";
  resultBox.innerHTML = `<h3>Error</h3><p>${escapeHtml(message)}</p>`;
  resultBox.classList.remove("hidden");
}

function hideResult() {
  resultBox.classList.add("hidden");
}

function setChecking(isChecking) {
  checkBtn.disabled = isChecking;
  checkBtn.textContent = isChecking ? "Checking..." : "Check Eligibility";
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}