// frontend/script.js
const API_BASE = 'http://127.0.0.1:8000';

// return token without whitespace
function getToken() {
  const t = localStorage.getItem('token') || '';
  return t.replace(/\s/g,'');
}

// simple GET wrapper that throws on non-ok
async function apiGet(path) {
  const url = API_BASE + path;
  const token = getToken();
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = 'Bearer ' + token;
  const res = await fetch(url, { headers });
  if (!res.ok) {
    let errText = `HTTP ${res.status}`;
    try {
      const json = await res.json();
      if (json.detail) errText = json.detail;
      else if (json.message) errText = json.message;
    } catch(e){}
    throw new Error(errText);
  }
  return res.json();
}
