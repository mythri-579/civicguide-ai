requireAdminOrRedirect();

const checkNowBtn = document.getElementById("checkNowBtn");
const checkStatus = document.getElementById("checkStatus");
const alertsList = document.getElementById("alertsList");


checkNowBtn.addEventListener("click", async () => {
  setChecking(true);
  hideCheckStatus();

  try {
    const response = await fetch(`${API_BASE_URL}/api/sources/check-updates`, {
      method: "POST"
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Check failed");
    }

    showCheckStatus(`Checked ${data.checked} document(s) — ${data.alerts_created} new alert(s) found.`);
    loadAlerts();

  } catch (error) {
    showCheckStatus(`Error: ${error.message}`);
    console.error("Check-updates error:", error);
  } finally {
    setChecking(false);
  }
});

async function loadAlerts() {
  try {
    const response = await authfetch(`${API_BASE_URL}/api/sources/alerts`);
    const alerts = await response.json();
    renderAlerts(alerts);
  } catch (error) {
    alertsList.innerHTML = `<p class="empty-state">Failed to load alerts.</p>`;
    console.error("Load alerts error:", error);
  }
}

function renderAlerts(alerts) {
  if (!alerts || alerts.length === 0) {
    alertsList.innerHTML = `<p class="empty-state">No pending alerts. All sources up to date.</p>`;
    return;
  }

  alertsList.innerHTML = "";

  alerts.forEach((alert) => {
    const card = document.createElement("div");
    card.className = "alert-card";

    const detectedDate = new Date(alert.detected_at).toLocaleString();

    card.innerHTML = `
      <div class="alert-title">Change detected — Document ID ${alert.document_id}</div>
      <div class="alert-meta">
        Source: ${escapeHtml(alert.source_url)}<br/>
        Old hash: ${alert.old_hash.substring(0, 16)}...<br/>
        New hash: ${alert.new_hash.substring(0, 16)}...<br/>
        Detected: ${detectedDate}
      </div>
      <div class="alert-actions">
        <button class="approve-btn" data-id="${alert.id}">Approve</button>
        <button class="reject-btn" data-id="${alert.id}">Reject</button>
      </div>
    `;

    alertsList.appendChild(card);
  });

  document.querySelectorAll(".approve-btn").forEach((btn) => {
    btn.addEventListener("click", () => handleDecision(btn.dataset.id, "approve"));
  });

  document.querySelectorAll(".reject-btn").forEach((btn) => {
    btn.addEventListener("click", () => handleDecision(btn.dataset.id, "reject"));
  });
}

async function handleDecision(alertId, action) {
  const endpoint = action === "approve"
    ? `/api/sources/approve-update/${alertId}`
    : `/api/sources/reject-update/${alertId}`;

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, { method: "POST" });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `${action} failed`);
    }

    showCheckStatus(data.message || `${action} successful`);
    loadAlerts();

  } catch (error) {
    showCheckStatus(`Error: ${error.message}`);
    console.error(`${action} error:`, error);
  }
}

function setChecking(isChecking) {
  checkNowBtn.disabled = isChecking;
  checkNowBtn.textContent = isChecking ? "Checking..." : "Check Now";
}

function showCheckStatus(message) {
  checkStatus.textContent = message;
  checkStatus.classList.remove("hidden");
}

function hideCheckStatus() {
  checkStatus.classList.add("hidden");
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

loadAlerts();