const state = {
  health: null,
  tradeJournals: [],
  news: [],
  fearGreed: [],
  editingTradeId: null,
};

const endpoints = {
  health: "/api/health/full",
  tradeJournals: "/api/trade-journals",
  news: "/api/news",
  newsSync: "/api/news/sync",
  fearGreed: "/api/fear-greed",
  fearGreedSync: "/api/fear-greed/sync",
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));
const API_BASE_URL =
  document.querySelector('meta[name="api-base"]')?.content?.trim() ||
  window.__API_BASE_URL__ ||
  "";
const IS_GITHUB_PAGES = window.location.hostname.endsWith("github.io");
const HAS_BACKEND = Boolean(API_BASE_URL);

async function request(path, options = {}) {
  if (!HAS_BACKEND) {
    const method = String(options.method || "GET").toUpperCase();
    if (method === "GET") {
      return offlineResponse(path);
    }
    throw new Error("백엔드 연결이 아직 설정되지 않았습니다.");
  }

  const url = API_BASE_URL ? `${API_BASE_URL}${path}` : path;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await response.text();
  let payload = {};
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch {
      payload = { message: text };
    }
  }

  if (!response.ok) {
    throw new Error(payload.detail || payload.message || `HTTP ${response.status}`);
  }

  return payload;
}

function offlineResponse(path) {
  if (path.startsWith("/api/health")) {
    return {
      api: { status: "unavailable", service: "backend" },
      database: { status: "unavailable", service: "database", connected: false },
      overall: "offline",
      message: "백엔드 연결이 아직 설정되지 않았습니다.",
    };
  }

  if (path.startsWith("/api/trade-journals")) {
    return { items: [] };
  }

  if (path.startsWith("/api/news")) {
    return { items: [] };
  }

  if (path.startsWith("/api/fear-greed")) {
    return { items: [] };
  }

  return {};
}

function formatDateTime(value) {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value);
  }
  return new Intl.DateTimeFormat("ko-KR", {
    timeZone: "Asia/Seoul",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}

function setActivePage(pageId) {
  $$(".nav-item").forEach((button) => {
    button.classList.toggle("active", button.dataset.page === pageId);
  });

  $$(".page").forEach((section) => {
    section.classList.toggle("is-active", section.id === pageId);
  });
}

function renderHealth() {
  const root = $("#health-status");
  if (!state.health) {
    root.innerHTML = '<div class="status-pill neutral">확인 중...</div>';
    return;
  }

  if (state.health.error) {
    root.innerHTML = `<div class="status-pill bad">${state.health.error}</div>`;
    return;
  }

  const apiStatus = state.health.api?.status === "ok";
  const dbStatus = state.health.database?.connected === true;
  root.innerHTML = `
    <div class="status-pill ${apiStatus ? "good" : "bad"}">API: ${state.health.api?.status || "unknown"}</div>
    <div class="status-pill ${dbStatus ? "good" : "bad"}">DB: ${dbStatus ? "connected" : "disconnected"}</div>
    <div class="status-pill neutral">Overall: ${state.health.overall}</div>
  `;
  $("#health-json").textContent = JSON.stringify(state.health, null, 2);
}

function renderNewsMini() {
  const root = $("#news-mini-list");
  const items = state.news.slice(0, 3);
  if (!items.length) {
    root.innerHTML = '<div class="mini-card muted">뉴스가 아직 없습니다.</div>';
    return;
  }

  root.innerHTML = items.map((item) => `
    <article class="mini-card">
      <h5>${escapeHtml(item.title)}</h5>
      <p>${escapeHtml(item.publisher || item.source || "-")}</p>
    </article>
  `).join("");
}

function renderFearGreedMini() {
  const root = $("#fear-greed-mini");
  const item = state.fearGreed[0];
  if (!item) {
    root.innerHTML = '<div class="mini-card muted">지수가 아직 없습니다.</div>';
    return;
  }

  root.innerHTML = `
    <div class="metric-value">${item.index_value}</div>
    <div class="metric-label">${escapeHtml(item.state_label || "unknown")}</div>
    <p class="muted">수집 시각: ${formatDateTime(item.fetched_at)}</p>
  `;
}

function renderNewsList() {
  const root = $("#news-list");
  if (!state.news.length) {
    root.innerHTML = '<div class="list-item muted">수집된 뉴스가 없습니다.</div>';
    return;
  }

  root.innerHTML = state.news.map((item) => `
    <article class="list-item">
      <h5><a href="${escapeAttr(item.url)}" target="_blank" rel="noreferrer">${escapeHtml(item.title)}</a></h5>
      <p>${escapeHtml(item.publisher || item.source || "-")} · ${formatDateTime(item.published_at || item.fetched_at)}</p>
      <p>${escapeHtml(item.summary || "요약 없음")}</p>
    </article>
  `).join("");
}

function renderFearGreedList() {
  const root = $("#fear-greed-list");
  if (!state.fearGreed.length) {
    root.innerHTML = '<div class="list-item muted">수집된 지수가 없습니다.</div>';
    return;
  }

  root.innerHTML = state.fearGreed.map((item) => `
    <article class="list-item">
      <h5>${escapeHtml(item.state_label || "unknown")}</h5>
      <p>지수: <strong>${item.index_value}</strong></p>
      <p>수집 시각: ${formatDateTime(item.fetched_at)}</p>
    </article>
  `).join("");
}

function renderTradeList() {
  const root = $("#trade-list");
  if (!state.tradeJournals.length) {
    root.innerHTML = '<div class="list-item muted">기록이 없습니다.</div>';
    return;
  }

  root.innerHTML = `
    <table class="table">
      <thead>
        <tr>
          <th>날짜</th>
          <th>종목</th>
          <th>구분</th>
          <th>수량</th>
          <th>가격</th>
          <th>메모</th>
          <th>작업</th>
        </tr>
      </thead>
      <tbody>
        ${state.tradeJournals.map((item) => `
          <tr>
            <td>${escapeHtml(item.trade_date)}</td>
            <td>${escapeHtml(item.stock_name)}<br /><span class="muted">${escapeHtml(item.ticker)}</span></td>
            <td>${escapeHtml(item.side)}</td>
            <td>${item.quantity}</td>
            <td>${item.price}</td>
            <td>${escapeHtml(item.memo || "-")}</td>
            <td>
              <div class="row-actions">
                <button class="ghost-btn" data-edit-trade="${item.id}" type="button">편집</button>
                <button class="ghost-btn" data-delete-trade="${item.id}" type="button">삭제</button>
              </div>
            </td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;

  root.querySelectorAll("[data-edit-trade]").forEach((button) => {
    button.addEventListener("click", () => {
      const item = state.tradeJournals.find((entry) => entry.id === Number(button.dataset.editTrade));
      if (item) fillTradeForm(item);
    });
  });

  root.querySelectorAll("[data-delete-trade]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (!confirm("이 기록을 삭제할까요?")) return;
      await request(`${endpoints.tradeJournals}/${button.dataset.deleteTrade}`, { method: "DELETE" });
      await loadTradeJournals();
    });
  });
}

function fillTradeForm(item) {
  state.editingTradeId = item.id;
  $("#trade-id").value = item.id;
  $("#trade-date").value = item.trade_date;
  $("#trade-ticker").value = item.ticker;
  $("#trade-stock-name").value = item.stock_name;
  $("#trade-side").value = item.side;
  $("#trade-quantity").value = item.quantity;
  $("#trade-price").value = item.price;
  $("#trade-memo").value = item.memo || "";
  $("#trade-form-message").textContent = `편집 중: #${item.id}`;
}

function resetTradeForm() {
  state.editingTradeId = null;
  $("#trade-id").value = "";
  $("#trade-form").reset();
  $("#trade-form-message").textContent = "";
  $("#trade-date").value = todayDateString();
}

function todayDateString() {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Seoul",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(new Date());
  const year = parts.find((part) => part.type === "year")?.value ?? "0000";
  const month = parts.find((part) => part.type === "month")?.value ?? "01";
  const day = parts.find((part) => part.type === "day")?.value ?? "01";
  return `${year}-${month}-${day}`;
}

async function loadHealth() {
  try {
    state.health = await request(endpoints.health);
  } catch (error) {
    state.health = { error: error.message };
  }
  renderHealth();
}

async function loadTradeJournals() {
  const filterDate = $("#trade-filter-date").value;
  const query = filterDate ? `?trade_date=${encodeURIComponent(filterDate)}` : "";
  try {
    const data = await request(`${endpoints.tradeJournals}${query}`);
    state.tradeJournals = data.items || [];
  } catch (error) {
    state.tradeJournals = [];
    $("#trade-list").innerHTML = `<div class="list-item muted">${escapeHtml(error.message)}</div>`;
    return;
  }
  renderTradeList();
}

async function loadNews() {
  try {
    const data = await request(endpoints.news);
    state.news = data.items || [];
  } catch (error) {
    state.news = [];
    $("#news-message").textContent = error.message;
    renderNewsMini();
    renderNewsList();
    return;
  }
  renderNewsMini();
  renderNewsList();
}

async function loadFearGreed() {
  try {
    const data = await request(endpoints.fearGreed);
    state.fearGreed = data.items || [];
  } catch (error) {
    state.fearGreed = [];
    $("#fg-message").textContent = error.message;
    renderFearGreedMini();
    renderFearGreedList();
    return;
  }
  renderFearGreedMini();
  renderFearGreedList();
}

async function handleTradeSubmit(event) {
  event.preventDefault();

  if (!HAS_BACKEND) {
    $("#trade-form-message").textContent = "백엔드 연결이 아직 설정되지 않았습니다.";
    return;
  }

  const payload = {
    trade_date: $("#trade-date").value,
    ticker: $("#trade-ticker").value.trim(),
    stock_name: $("#trade-stock-name").value.trim(),
    side: $("#trade-side").value,
    quantity: Number($("#trade-quantity").value),
    price: Number($("#trade-price").value),
    memo: $("#trade-memo").value.trim() || null,
  };

  const tradeId = $("#trade-id").value;
  const method = tradeId ? "PUT" : "POST";
  const path = tradeId ? `${endpoints.tradeJournals}/${tradeId}` : endpoints.tradeJournals;

  $("#trade-form-message").textContent = "저장 중...";
  try {
    await request(path, {
      method,
      body: JSON.stringify(payload),
    });
    $("#trade-form-message").textContent = "저장 완료";
    resetTradeForm();
    await loadTradeJournals();
  } catch (error) {
    $("#trade-form-message").textContent = error.message;
  }
}

async function syncNews() {
  if (!HAS_BACKEND) {
    $("#news-message").textContent = "백엔드 연결이 아직 설정되지 않았습니다.";
    return;
  }

  $("#news-message").textContent = "수집 중...";
  try {
    const result = await request(endpoints.newsSync, { method: "POST" });
    $("#news-message").textContent = `${result.message} (${result.saved_count || 0}건 저장)`;
    await loadNews();
  } catch (error) {
    $("#news-message").textContent = error.message;
  }
}

async function syncFearGreed() {
  if (!HAS_BACKEND) {
    $("#fg-message").textContent = "백엔드 연결이 아직 설정되지 않았습니다.";
    return;
  }

  $("#fg-message").textContent = "수집 중...";
  try {
    const result = await request(endpoints.fearGreedSync, { method: "POST" });
    $("#fg-message").textContent = `${result.message} (지수: ${result.index_value ?? "-"})`;
    await loadFearGreed();
  } catch (error) {
    $("#fg-message").textContent = error.message;
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeAttr(value) {
  return escapeHtml(value);
}

function wireEvents() {
  $$(".nav-item").forEach((button) => {
    button.addEventListener("click", () => setActivePage(button.dataset.page));
  });

  $("#trade-form").addEventListener("submit", handleTradeSubmit);
  $("#reset-trade").addEventListener("click", resetTradeForm);
  $("#trade-filter-btn").addEventListener("click", loadTradeJournals);
  $("#news-sync-btn").addEventListener("click", syncNews);
  $("#news-refresh-btn").addEventListener("click", loadNews);
  $("#fg-sync-btn").addEventListener("click", syncFearGreed);
  $("#fg-refresh-btn").addEventListener("click", loadFearGreed);
  $("#refresh-news-mini").addEventListener("click", loadNews);
  $("#refresh-fg-mini").addEventListener("click", loadFearGreed);
}

async function bootstrap() {
  $("#trade-date").value = todayDateString();
  $("#trade-filter-date").value = "";
  wireEvents();
  await Promise.all([
    loadHealth(),
    loadTradeJournals(),
    loadNews(),
    loadFearGreed(),
  ]);
}

document.addEventListener("DOMContentLoaded", bootstrap);

