// Clown — small, dependency-free interactions shared by every page.
(() => {
  const root = document.documentElement;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  root.classList.add("js");

  // nav: hairline once scrolled, mobile menu
  const nav = document.querySelector(".nav");
  const onScroll = () => nav && nav.classList.toggle("scrolled", window.scrollY > 8);
  onScroll(); window.addEventListener("scroll", onScroll, { passive: true });
  const menu = document.querySelector(".menu-btn");
  if (menu && nav) {
    menu.addEventListener("click", () => { const open = nav.classList.toggle("open"); menu.setAttribute("aria-expanded", open); menu.textContent = open ? "Close" : "Menu"; });
    nav.querySelectorAll(".nav-links a").forEach((a) => a.addEventListener("click", () => { nav.classList.remove("open"); menu.setAttribute("aria-expanded", "false"); menu.textContent = "Menu"; }));
  }

  // scroll-triggered reveals
  const items = document.querySelectorAll("[data-reveal]");
  if (reduce || !("IntersectionObserver" in window)) items.forEach((el) => el.classList.add("in"));
  else {
    const io = new IntersectionObserver((entries) => entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    items.forEach((el) => io.observe(el));
  }

  // project previews: play only while on screen
  const previews = document.querySelectorAll("video[data-preview]");
  if (!reduce && "IntersectionObserver" in window) {
    const vo = new IntersectionObserver((entries) => entries.forEach((e) => { const v = e.target; if (e.isIntersecting) { v.preload = "auto"; v.play().catch(() => {}); } else v.pause(); }), { threshold: 0.3 });
    previews.forEach((v) => vo.observe(v));
  }

  // showreel: muted preview loop -> one click plays with sound; click again pauses
  const reel = document.querySelector("[data-reel]");
  if (reel) {
    const v = reel.querySelector("video"), btn = reel.querySelector(".reel-play"), label = btn.querySelector(".lbl");
    const icon = (playing) => (btn.querySelector(".ico").innerHTML = playing
      ? '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="2" width="3.5" height="12" rx="1"/><rect x="9.5" y="2" width="3.5" height="12" rx="1"/></svg>'
      : '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5v11a.6.6 0 0 0 .9.5l9-5.5a.6.6 0 0 0 0-1l-9-5.5a.6.6 0 0 0-.9.5z"/></svg>');
    let withSound = false;
    if (reduce) { v.removeAttribute("autoplay"); v.pause(); }
    const setState = () => {
      const playing = withSound && !v.paused;
      reel.classList.toggle("playing", playing); reel.classList.toggle("paused", withSound && v.paused);
      icon(playing); label.textContent = playing ? "Pause" : withSound ? "Resume" : "Play showreel";
      btn.setAttribute("aria-label", playing ? "Pause showreel" : "Play showreel with sound");
    };
    const toggle = () => {
      if (!withSound) { withSound = true; v.muted = false; v.loop = false; v.currentTime = 0; v.play(); }
      else if (v.paused) v.play(); else v.pause();
    };
    btn.addEventListener("click", (e) => { e.stopPropagation(); toggle(); });
    v.addEventListener("click", () => { if (withSound) toggle(); });
    v.addEventListener("play", setState); v.addEventListener("pause", setState);
    v.addEventListener("ended", () => { withSound = false; v.muted = true; v.loop = true; if (!reduce) v.play(); setState(); });
    reel.addEventListener("keydown", (e) => { if (e.key === " " && withSound && e.target === v) { e.preventDefault(); toggle(); } });
    setState();
  }

  // about intro: muted loop while visible; one click restarts it with sound and native controls
  const intro = document.querySelector("[data-intro]");
  if (intro) {
    const v = intro.querySelector("video"), b = intro.querySelector(".intro-play");
    if (!reduce && "IntersectionObserver" in window) new IntersectionObserver((es) => es.forEach((e) => { if (intro.classList.contains("on")) return; e.isIntersecting ? v.play().catch(() => {}) : v.pause(); }), { threshold: 0.4 }).observe(v);
    b.addEventListener("click", () => { intro.classList.add("on"); v.muted = false; v.loop = false; v.controls = true; v.currentTime = 0; v.play(); });
    v.addEventListener("ended", () => { intro.classList.remove("on"); v.controls = false; v.muted = true; v.loop = true; });
  }

  // copy email
  document.querySelectorAll("[data-copy]").forEach((b) => b.addEventListener("click", async () => {
    const out = document.querySelector(".copied");
    try { await navigator.clipboard.writeText(b.dataset.copy); if (out) out.textContent = "Email address copied."; }
    catch { if (out) out.textContent = b.dataset.copy; }
  }));
})();
