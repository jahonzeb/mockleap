/* MockLeap — main.js */
'use strict';

// ── Dark mode ──────────────────────────────────────────────────────
const DarkMode = {
  init() {
    const stored = localStorage.getItem('ml.dark');
    if (stored === '1' || document.documentElement.classList.contains('dark')) {
      document.documentElement.classList.add('dark');
    }
  },
  toggle() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('ml.dark', isDark ? '1' : '0');
    // Sync with server preference
    fetch('/profile/dark-mode/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: 'dark=' + (isDark ? '1' : '0'),
    }).catch(_=> {});
  }
};
DarkMode.init();

// ── Toast notifications ────────────────────────────────────────────
const Toast = {
  show(message, type = 'info', duration = 3500) {
    const colors = {
      info: 'background:var(--ink)',
      ok: 'background:var(--ok)',
      warn: 'background:var(--warn)',
      error: 'background:#B91C1C',
    };
    const el = document.createElement('div');
    el.className = 'ml-toast';
    el.style.cssText = colors[type] || colors.info;
    el.innerHTML = `<span>${message}</span>
      <button onclick="this.parentElement.remove()" style="margin-left:auto;opacity:.7;font-size:16px;cursor:pointer;background:none;border:none;color:inherit;">✕</button>`;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), duration);
  }
};
window.Toast = Toast;

// ── Exam timer ─────────────────────────────────────────────────────
class ExamTimer {
  constructor(el, seconds, onEnd) {
    this.el = el;
    this.remaining = seconds;
    this.onEnd = onEnd;
    this.interval = null;
  }
  start() {
    this.render();
    this.interval = setInterval(() => {
      this.remaining--;
      this.render();
      if (this.remaining <= 0) {
        clearInterval(this.interval);
        if (this.onEnd) this.onEnd();
      }
    }, 1000);
  }
  stop() { clearInterval(this.interval); }
  render() {
    const m = Math.floor(this.remaining / 60).toString().padStart(2, '0');
    const s = (this.remaining % 60).toString().padStart(2, '0');
    if (this.el) this.el.textContent = `${m}:${s}`;
    if (this.remaining <= 300 && this.el) this.el.style.color = 'var(--warn)';
  }
}
window.ExamTimer = ExamTimer;

// ── Waveform generator ─────────────────────────────────────────────
function drawWaveform(svgId, bars, width, height, activeCount, activeColor, inactiveColor) {
  const svg = document.getElementById(svgId);
  if (!svg) return;
  const barW = (width - bars * 2) / bars;
  let html = '';
  for (let i = 0; i < bars; i++) {
    const seed = Math.sin(i * 0.7) * Math.cos(i * 0.3);
    const h = Math.max(4, Math.abs(seed) * height * 0.85);
    const x = i * (barW + 2);
    const y = (height - h) / 2;
    const fill = i < activeCount ? activeColor : inactiveColor;
    html += `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${barW.toFixed(1)}" height="${h.toFixed(1)}" rx="1.5" fill="${fill}"/>`;
  }
  svg.innerHTML = html;
}
window.drawWaveform = drawWaveform;

// ── MediaRecorder (Speaking) ───────────────────────────────────────
class AudioRecorder {
  constructor({ onStart, onStop, onData } = {}) {
    this.mediaRecorder = null;
    this.chunks = [];
    this.startTime = null;
    this.onStart = onStart;
    this.onStop = onStop;
    this.onData = onData;
  }
  async start() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    this.mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
    this.chunks = [];
    this.mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) this.chunks.push(e.data);
      if (this.onData) this.onData(e.data);
    };
    this.mediaRecorder.onstop = () => {
      const blob = new Blob(this.chunks, { type: 'audio/webm' });
      const duration = Math.round((Date.now() - this.startTime) / 1000);
      stream.getTracks().forEach(t => t.stop());
      if (this.onStop) this.onStop(blob, duration);
    };
    this.mediaRecorder.start(100);
    this.startTime = Date.now();
    if (this.onStart) this.onStart();
  }
  stop() {
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      this.mediaRecorder.stop();
    }
  }
  get isRecording() {
    return this.mediaRecorder && this.mediaRecorder.state === 'recording';
  }
}
window.AudioRecorder = AudioRecorder;

// ── Autosave ──────────────────────────────────────────────────────
function setupAutosave(formId, url, interval = 8000) {
  const form = document.getElementById(formId);
  if (!form) return;
  let timer = setInterval(async () => {
    const data = {};
    form.querySelectorAll('input,textarea,select').forEach(el => {
      if (el.name) data[el.name] = el.value;
    });
    try {
      await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(data),
      });
    } catch (_) {}
  }, interval);
  return () => clearInterval(timer);
}
window.setupAutosave = setupAutosave;

// ── Band ring (SVG donut) ──────────────────────────────────────────
function drawBandRing(svgId, value, max = 9) {
  const svg = document.getElementById(svgId);
  if (!svg) return;
  const size = parseInt(svg.getAttribute('width')) || 120;
  const r = (size - 14) / 2;
  const c = 2 * Math.PI * r;
  const pct = Math.min(value / max, 1);
  svg.innerHTML = `
    <circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="var(--border)" stroke-width="6"/>
    <circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="var(--accent)" stroke-width="6"
      stroke-dasharray="${(c*pct).toFixed(1)} ${c.toFixed(1)}" stroke-linecap="round"
      transform="rotate(-90 ${size/2} ${size/2})"/>`;
}
window.drawBandRing = drawBandRing;

// ── Utility ───────────────────────────────────────────────────────
function getCookie(name) {
  const v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
  return v ? v[2] : '';
}
window.getCookie = getCookie;

// ── FAQ accordion ─────────────────────────────────────────────────
document.querySelectorAll('[data-faq]').forEach(btn => {
  btn.addEventListener('click', () => {
    const answer = btn.nextElementSibling;
    const icon = btn.querySelector('[data-faq-icon]');
    const isOpen = !answer.classList.contains('hidden');
    // Close all
    document.querySelectorAll('[data-faq-answer]').forEach(a => a.classList.add('hidden'));
    document.querySelectorAll('[data-faq-icon]').forEach(i => i.textContent = '+');
    if (!isOpen) {
      answer.classList.remove('hidden');
      if (icon) icon.textContent = '−';
    }
  });
});

// ── Mobile nav toggle ─────────────────────────────────────────────
const menuBtn = document.getElementById('mobile-menu-btn');
const sidebar = document.getElementById('sidebar');
if (menuBtn && sidebar) {
  menuBtn.addEventListener('click', () => sidebar.classList.toggle('-translate-x-full'));
}
