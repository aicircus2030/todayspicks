function getBasePrefix() {
  // Works for:
  // - Netlify root (domain.com/)
  // - GitHub Pages project site (domain.com/repo/)
  // It uses the <base> tag if present, otherwise infers from location.pathname.
  const baseTag = document.querySelector("base");
  if (baseTag && baseTag.getAttribute("href")) {
    return baseTag.getAttribute("href").replace(/\/$/, "");
  }

  // If you are on /blog/..., we want to go up one level for relative reads.
  // For root pages, prefix is "".
  const p = window.location.pathname;
  if (p.includes("/blog/")) return "..";
  if (p.endsWith("/blog")) return "..";
  return "";
}

async function loadPosts(){
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  const cards = document.getElementById("cards");
  if (!cards) return;

  const prefix = getBasePrefix();
  const url = `${prefix}/data/posts.json`.replace("//", "/");

  try{
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status} loading ${url}`);
    const data = await res.json();

    const items = (data.posts || []).slice(0, 12);

    cards.innerHTML = items.map(p => `
      <article class="card">
        <div class="inner">
          <span class="badge">${escapeHtml(p.category || "General")}</span>
          <h3><a href="${escapeAttr(prefix + p.url)}">${escapeHtml(p.title)}</a></h3>
          <p>${escapeHtml(p.summary || "")}</p>
          <div class="meta">
            <span>${escapeHtml(p.date || "")}</span>
            <a class="cta" href="${escapeAttr(prefix + p.url)}">Read →</a>
          </div>
        </div>
      </article>
    `).join("");
  }catch(e){
    cards.innerHTML = `
      <div class="muted">
        Blog failed to load posts.<br/>
        Tried: <code>${escapeHtml(url)}</code><br/>
        Error: <code>${escapeHtml(String(e.message || e))}</code>
      </div>`;
  }
}

function escapeHtml(s){
  return (s ?? "").toString()
    .replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;")
    .replaceAll('"',"&quot;").replaceAll("'","&#039;");
}
function escapeAttr(s){ return escapeHtml(s).replaceAll("`",""); }

loadPosts();
