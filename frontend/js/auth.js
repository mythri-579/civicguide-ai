const API_BASE_URL = "http://127.0.0.1:8000";

function saveAuth(token, user) {
  localStorage.setItem("cg_token", token);
  localStorage.setItem("cg_user", JSON.stringify(user));
}

function getToken() {
  return localStorage.getItem("cg_token");
}

function getUser() {
  const raw = localStorage.getItem("cg_user");
  return raw ? JSON.parse(raw) : null;
}

function clearAuth() {
  localStorage.removeItem("cg_token");
  localStorage.removeItem("cg_user");
}

function isLoggedIn() {
  return !!getToken();
}

function isAdmin() {
  const user = getUser();
  return user && user.role === "admin";
}

async function authFetch(url, options = {}) {
  const token = getToken();
  const headers = options.headers || {};

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  return fetch(url, { ...options, headers });
}

function requireAdminOrRedirect() {
  if (!isLoggedIn() || !isAdmin()) {
    window.location.href = "login.html";
  }
}