// Super Cerebro AI PWA app logic
const API_URL = 'https://ai-agent-backend80.onrender.com/api/chat';
const messagesEl = () => document.getElementById('messages');
const form = () => document.getElementById('chatForm');
const input = () => document.getElementById('messageInput');
const notifToggle = () => document.getElementById('notifToggle');
const darkToggle = () => document.getElementById('darkToggle');
const installBtn = () => document.getElementById('installBtn');

let deferredInstallEvent = null;

// Tabs
const tabs = document.querySelectorAll('.tab');
tabs.forEach(t => t.addEventListener('click', () => {
  const target = t.dataset.tab;
  document.querySelectorAll('.tab').forEach(b => b.classList.toggle('active', b===t));
  document.querySelectorAll('.view').forEach(v => v.classList.toggle('active', v.id === `view-${target}`));
}));

// Theme
if (darkToggle()) darkToggle().addEventListener('change', e => {
  document.documentElement.classList.toggle('light', !e.target.checked);
});

// Notifications
if (notifToggle()) notifToggle().addEventListener('change', async e => {
  if (e.target.checked) {
    try {
      const perm = await Notification.requestPermission();
      if (perm !== 'granted') e.target.checked = false;
    } catch {
      e.target.checked = false;
    }
  }
});

// Service worker
(async function registerSW(){
  if ('serviceWorker' in navigator) {
    try {
      const reg = await navigator.serviceWorker.register('./sw.js');
      console.log('SW registered', reg.scope);
    } catch (e) { console.error('SW fail', e); }
  }
})();

// Install prompt
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredInstallEvent = e;
  if (installBtn()) installBtn().hidden = false;
});
if (installBtn()) installBtn().addEventListener('click', async () => {
  if (!deferredInstallEvent) return;
  deferredInstallEvent.prompt();
  const { outcome } = await deferredInstallEvent.userChoice;
  console.log('Install', outcome);
  deferredInstallEvent = null;
  installBtn().hidden = true;
});

// Chat helpers
function addMessage({ role, content }) {
  const li = document.createElement('li');
  li.className = `msg ${role}`;
  li.innerHTML = `<div class="bubble">${escapeHtml(content)}</div>`;
  messagesEl().appendChild(li);
  messagesEl().scrollTop = messagesEl().scrollHeight;
}
function addTyping() {
  const li = document.createElement('li');
  li.className = 'msg ai typing';
  li.innerHTML = '<div class="bubble"><span class="dot d1"></span><span class="dot d2"></span><span class="dot d3"></span></div>';
  li.id = 'typing';
  messagesEl().appendChild(li);
  messagesEl().scrollTop = messagesEl().scrollHeight;
}
function removeTyping(){ const el = document.getElementById('typing'); if (el) el.remove(); }
function escapeHtml(str){ return str.replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[m])); }

// Submit
if (form()) form().addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input().value.trim();
  if (!text) return;
  addMessage({ role: 'user', content: text });
  input().value='';
  addTyping();
  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    removeTyping();
    addMessage({ role: data.role || 'ai', content: data.reply || data.content || JSON.stringify(data) });
    maybeNotify('New reply from Super Cerebro AI');
  } catch (err) {
    removeTyping();
    addMessage({ role: 'system', content: `Error: ${err.message}. Please try again.` });
  }
});

function maybeNotify(body){
  try {
    if (Notification.permission === 'granted' && navigator.serviceWorker?.ready) {
      navigator.serviceWorker.ready.then(reg => reg.showNotification('Super Cerebro AI', { body, icon: './icons/icon-192.png' }));
    }
  } catch {}
}

// Initial welcome
addMessage({ role: 'system', content: 'Welcome to Super Cerebro AI. How can I help you today?' });
