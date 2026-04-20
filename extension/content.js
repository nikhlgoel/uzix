// Uzix Content Script
// Watches text inputs and textareas, checks against the local Uzix API on paste/submit

const API_URL = "http://127.0.0.1:5000/detect";
const RISK_COLORS = {
  SAFE: "#22c55e",
  SUSPICIOUS: "#f59e0b",
  DANGEROUS: "#ef4444",
};

function createBadge(risk, info) {
  const badge = document.createElement("div");
  badge.id = "uzix-badge";
  badge.style.cssText = `
    position: fixed;
    bottom: 18px;
    right: 18px;
    z-index: 99999;
    background: ${RISK_COLORS[risk] || "#6b7280"};
    color: #fff;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-family: monospace;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
    transition: opacity 0.4s;
  `;
  badge.textContent = `Uzix: ${risk} — ${info}`;
  return badge;
}

function showBadge(risk, info) {
  const old = document.getElementById("uzix-badge");
  if (old) old.remove();
  const badge = createBadge(risk, info);
  document.body.appendChild(badge);
  setTimeout(() => {
    badge.style.opacity = "0";
    setTimeout(() => badge.remove(), 500);
  }, 3500);
}

async function checkText(text) {
  if (!text || text.trim().length < 5) return;
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: text }),
    });
    if (!res.ok) return;
    const data = await res.json();
    if (data.risk && data.risk !== "SAFE") {
      showBadge(data.risk, data.info || "");
    }
  } catch (_) {
    // API not running locally — silently skip
  }
}

// attach to all textareas and text inputs
function attachListeners() {
  const fields = document.querySelectorAll("textarea, input[type='text'], [contenteditable='true']");
  fields.forEach((el) => {
    if (el.dataset.uzixAttached) return;
    el.dataset.uzixAttached = "1";

    // check on paste
    el.addEventListener("paste", () => {
      setTimeout(() => checkText(el.value || el.innerText), 100);
    });

    // check on blur (when user leaves the field)
    el.addEventListener("blur", () => {
      checkText(el.value || el.innerText);
    });
  });
}

// run on load, then watch for dynamic elements (SPAs etc.)
attachListeners();
const observer = new MutationObserver(attachListeners);
observer.observe(document.body, { childList: true, subtree: true });
