// ── Config ───────────────────────────────────────
// Update this to your Render backend URL after deploying
const API_BASE = "https://vikas-portfolio-api.onrender.com";

// ── Nav scroll highlight ─────────────────────────
const sections = document.querySelectorAll("section[id]");
const navLinks = document.querySelectorAll(".nav-links a");

function onScroll() {
  const scrollY = window.scrollY + 80;
  sections.forEach(sec => {
    const top = sec.offsetTop;
    const height = sec.offsetHeight;
    const id = sec.getAttribute("id");
    if (scrollY >= top && scrollY < top + height) {
      navLinks.forEach(a => {
        a.classList.toggle("active", a.getAttribute("href") === `#${id}`);
      });
    }
  });

  // Shrink nav on scroll
  document.getElementById("nav").classList.toggle("scrolled", window.scrollY > 40);
}
window.addEventListener("scroll", onScroll, { passive: true });

// ── Smooth close mobile menu on nav link click ───
navLinks.forEach(a => {
  a.addEventListener("click", () => document.body.classList.remove("menu-open"));
});

// ── Blog posts ───────────────────────────────────
async function loadBlogPosts() {
  const container = document.getElementById("blog-posts");
  const empty = document.getElementById("blog-empty");
  try {
    const res = await fetch(`${API_BASE}/blog`);
    if (!res.ok) throw new Error("API error");
    const posts = await res.json();
    if (!posts.length) {
      container.innerHTML = "";
      empty.style.display = "block";
      return;
    }
    container.innerHTML = posts.map(post => `
      <article class="blog-card" onclick="openPost('${post.slug}')">
        <div class="blog-date">${formatDate(post.published_at)}</div>
        <div class="blog-title">${esc(post.title)}</div>
        <div class="blog-excerpt">${esc(post.excerpt)}</div>
        <span class="blog-tag">${esc(post.tag || "AI/ML")}</span>
      </article>
    `).join("");
  } catch {
    container.innerHTML = "";
    empty.style.display = "block";
  }
}

function openPost(slug) {
  window.location.href = `blog/${slug}.html`;
}

function formatDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
}

function esc(str) {
  const d = document.createElement("div");
  d.textContent = str || "";
  return d.innerHTML;
}

loadBlogPosts();

// ── Contact form ─────────────────────────────────
async function submitContact(e) {
  e.preventDefault();
  const btn = document.getElementById("submit-btn");
  const status = document.getElementById("form-status");
  const form = e.target;

  const payload = {
    name:    form.name.value.trim(),
    email:   form.email.value.trim(),
    subject: form.subject.value.trim(),
    message: form.message.value.trim(),
  };

  btn.textContent = "Sending…";
  btn.disabled = true;
  status.className = "form-status";
  status.textContent = "";

  try {
    const res = await fetch(`${API_BASE}/contact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Server error");
    status.className = "form-status success";
    status.textContent = "✓ Message sent! I'll get back to you soon.";
    form.reset();
  } catch {
    status.className = "form-status error";
    status.textContent = "Something went wrong. Try emailing me directly.";
  } finally {
    btn.textContent = "Send message";
    btn.disabled = false;
  }
}

// ── Nav active style ─────────────────────────────
const style = document.createElement("style");
style.textContent = `
  .nav-links a.active { color: var(--text); }
  #nav.scrolled { background: rgba(12,14,18,0.95); }
`;
document.head.appendChild(style);
