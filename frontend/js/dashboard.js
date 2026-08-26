requireAdminOrRedirect();

const user = getUser();
document.getElementById("welcomeMsg").textContent = `Welcome, ${user.full_name || user.email}`;

async function loadDashboard() {
  try {
    const [docsRes, alertsRes] = await Promise.all([
      authFetch(`${API_BASE_URL}/api/documents/`),
      authFetch(`${API_BASE_URL}/api/sources/alerts`)
    ]);

    const documents = await docsRes.json();
    const alerts = await alertsRes.json();

    const activeCount = documents.filter(d => d.status === "active").length;

    document.getElementById("totalDocs").textContent = documents.length;
    document.getElementById("activeDocs").textContent = activeCount;
    document.getElementById("pendingAlerts").textContent = alerts.length;

    renderRecentDocs(documents.slice(0, 5));

  } catch (error) {
    console.error("Dashboard load error:", error);
  }
}

function renderRecentDocs(documents) {
  const list = document.getElementById("recentDocsList");

  if (!documents || documents.length === 0) {
    list.innerHTML = `<p class="empty-state">No documents uploaded yet.</p>`;
    return;
  }

  list.innerHTML = "";
  documents.forEach((doc) => {
    const card = document.createElement("div");
    card.className = "document-card";
    card.innerHTML = `
      <div class="doc-title">${escapeHtml(doc.title)}</div>
      <div class="doc-meta">Uploaded ${new Date(doc.uploaded_at).toLocaleString()}</div>
      <span class="doc-status">${escapeHtml(doc.status)}</span>
    `;
    list.appendChild(card);
  });
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

loadDashboard();