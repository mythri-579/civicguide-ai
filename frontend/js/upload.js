
const uploadForm = document.getElementById("uploadForm");
const submitBtn = document.getElementById("submitBtn");
const uploadStatus = document.getElementById("uploadStatus");
const documentsList = document.getElementById("documentsList");
requireAdminOrRedirect();

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(uploadForm);

  setSubmitting(true);
  hideStatus();

  try {
    const response = await authFetch(`${API_BASE_URL}/api/documents/upload`, {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Upload failed");
    }

    showStatus(`Uploaded successfully — ${data.chunk_count} chunks indexed.`, "success");
    uploadForm.reset();
    loadDocuments();

  } catch (error) {
    showStatus(`Error: ${error.message}`, "error");
    console.error("Upload error:", error);
  } finally {
    setSubmitting(false);
  }
});

async function loadDocuments() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/documents/`);
    const documents = await response.json();
    renderDocuments(documents);
  } catch (error) {
    documentsList.innerHTML = `<p class="empty-state">Failed to load documents.</p>`;
    console.error("Load documents error:", error);
  }
}

function renderDocuments(documents) {
  if (!documents || documents.length === 0) {
    documentsList.innerHTML = `<p class="empty-state">No documents uploaded yet.</p>`;
    return;
  }

  documentsList.innerHTML = "";

  documents.forEach((doc) => {
    const card = document.createElement("div");
    card.className = "document-card";

    const uploadedDate = new Date(doc.uploaded_at).toLocaleString();

    card.innerHTML = `
      <div class="doc-title">${escapeHtml(doc.title)}</div>
      <div class="doc-meta">
        ${doc.scheme_name ? escapeHtml(doc.scheme_name) + " &middot; " : ""}
        ${doc.department ? escapeHtml(doc.department) + " &middot; " : ""}
        Uploaded ${uploadedDate}
      </div>
      <span class="doc-status">${escapeHtml(doc.status)}</span>
    `;

    documentsList.appendChild(card);
  });
}

function setSubmitting(isSubmitting) {
  submitBtn.disabled = isSubmitting;
  submitBtn.textContent = isSubmitting ? "Uploading..." : "Upload Document";
}

function showStatus(message, type) {
  uploadStatus.textContent = message;
  uploadStatus.className = `upload-status ${type}`;
}

function hideStatus() {
  uploadStatus.className = "upload-status hidden";
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

loadDocuments();