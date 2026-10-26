// build.mjs — generates the portfolio pages (index.html + work/*.html). Static, no dependencies.
//   node build.mjs
// Edit NAME / EMAIL / SERVICES below; pages are rebuilt from these.
import fs from "node:fs";
import path from "node:path";
const ROOT = path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/, "$1"));

const NAME = "Clown";
const EMAIL = "tun832061@gmail.com";
const YEAR = 2026;

const page = ({ title, desc, depth = 0, body, current }) => {
  const r = depth ? "../" : "";
  const link = (href, label, key, cls = "") => `<li${cls ? ` class="${cls}"` : ""}><a href="${r}${href}"${current === key ? ' aria-current="page"' : ""}>${label}</a></li>`;
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<meta name="description" content="${desc}">
<meta property="og:title" content="${title}">
<meta property="og:description" content="${desc}">
<meta property="og:image" content="${r}assets/img/poster-showreel.jpg">
<link rel="stylesheet" href="${r}assets/site.css">
</head>
<body>
<nav class="nav"><div class="wrap">
  <a class="logo" href="${r}index.html">${NAME.toUpperCase()}<span>.</span></a>
  <ul>${link("index.html#work", "Work", "work")}${link("index.html#services", "Services", "services", "hide-sm")}${link("index.html#contact", "Contact", "contact")}</ul>
</div></nav>
${body}
<footer><div class="wrap"><div>© ${YEAR} ${NAME} · Motion design</div><div><a href="mailto:${EMAIL}">${EMAIL}</a></div></div></footer>
</body>
</html>
`;
};

const vid = (src, poster, { cls = "", loop = false, auto = false } = {}) =>
  `<div class="player ${cls}"><video src="${src}" poster="${poster}" controls playsinline preload="metadata"${loop ? " loop" : ""}${auto ? " autoplay muted" : ""}></video></div>`;

const WORK = [
  { slug: "nova", title: "NOVA", meta: "Product launch · 15s · 9:16", poster: "poster-nova.jpg",
    tags: ["Product ad", "Vertical", "Shape morph", "Sound design"] },
  { slug: "clown-club", title: "Clown Club — Pack & Unpack", meta: "Product motion · 15s · 16:9", poster: "poster-clown-club.jpg",
    tags: ["Fashion", "Photo motion", "Captions", "Sound design"] },
  { slug: "bez-and-the-boos", title: "Bez & the Boos", meta: "Character music video · 15s · 16:9", poster: "poster-bez-and-the-boos.jpg",
    tags: ["Character", "Beat-synced", "Seasonal", "Score"] },
  { slug: "no-after-effects", title: "No After Effects", meta: "Character motion · 12s · 16:9", poster: "poster-no-after-effects.jpg",
    tags: ["Character", "UI animation", "Beat-synced"] },
  { slug: "raise-trap", title: "The Raise Trap", meta: "Animated explainer · 60s · 16:9", poster: "poster-raise-trap.jpg",
    tags: ["Explainer", "Character", "Data viz", "Voiceover", "Captions"] },
  { slug: "corvo", title: "CORVO Knockout", meta: "Social ad pack · 9:16 · 1:1 · 16:9", poster: "poster-corvo-bumper.jpg",
    tags: ["Product ad", "3 formats", "Kinetic type", "Sound design"] },
  { slug: "pulse", title: "Pulse", meta: "SaaS launch promo · 15s · remaster", poster: "poster-pulse.jpg",
    tags: ["UI animation", "Logo sting", "Launch promo"] },
  { slug: "make-it-move", title: "Make It Move", meta: "Kinetic type · 15s · 9:16 · remaster", poster: "poster-mim.jpg",
    tags: ["Kinetic type", "Vertical", "Score"] },
];

// ---------------------------------------------------------------- home
const home = page({
  title: `${NAME} — Motion design`,
  desc: "Motion design for brands and explainers: animated explainers, social ad packs and product launch promos.",
  body: `
<header class="hero"><div class="wrap">
  <div class="eyebrow">Motion designer</div>
  <h1 class="display">Make it <span class="acc">move.</span></h1>
  <p class="lede">I design and animate explainer videos, social ads and launch promos — story, design, motion and sound, delivered in every format your channels need.</p>
  <div class="cta"><a class="btn primary" href="#contact">Start a project</a><a class="btn" href="#work">See the work</a></div>
  <div class="reel"><video src="assets/video/showreel.mp4" poster="assets/img/poster-showreel.jpg" controls playsinline preload="metadata"></video></div>
</div></header>

<section id="work"><div class="wrap">
  <div class="eyebrow">Selected work</div>
  <h2 class="display">Work</h2>
  <div class="grid">
${WORK.map((w) => `    <a class="card" href="work/${w.slug}.html">
      <div class="thumb"><img src="assets/img/${w.poster}" alt="${w.title} still" loading="lazy"></div>
      <div class="body"><h3>${w.title}</h3><div class="meta">${w.meta}</div><div class="tags">${w.tags.map((t) => `<span>${t}</span>`).join("")}</div></div>
    </a>`).join("\n")}
  </div>
</div></section>

<section id="services"><div class="wrap">
  <div class="eyebrow">What I make</div>
  <h2 class="display">Services</h2>
  <div class="services">
    <div class="svc"><h3>Explainer videos</h3><div class="price">Quote on request</div><p class="muted">60–90s animated explainers that make one idea land.</p>
      <ul><li>Script &amp; storyboard</li><li>Illustration &amp; data visualisation</li><li>Voiceover, captions, music</li><li>16:9 + vertical cutdown</li></ul></div>
    <div class="svc"><h3>Social ad packs</h3><div class="price">Quote on request</div><p class="muted">Scroll-stopping product ads, built sound-off first.</p>
      <ul><li>15s hero + 6s bumper</li><li>9:16, 1:1 and 16:9 versions</li><li>Offer &amp; CTA end cards</li><li>Original music + sound design</li></ul></div>
    <div class="svc"><h3>Launch promos</h3><div class="price">Quote on request</div><p class="muted">Logo stings and UI-driven promos for apps and SaaS.</p>
      <ul><li>Logo animation</li><li>Product UI animation</li><li>Tagline &amp; end card</li><li>Web + social exports</li></ul></div>
  </div>
  <h3 style="margin:48px 0 18px;font-size:22px">How a project runs</h3>
  <div class="steps">
    <div class="step"><b>1 · Brief</b><p>Your goal, audience and channels in one page.</p></div>
    <div class="step"><b>2 · Storyboard</b><p>A beat-by-beat plan and still frames to approve.</p></div>
    <div class="step"><b>3 · Animate</b><p>Motion, sound and a preview to review.</p></div>
    <div class="step"><b>4 · Deliver</b><p>Final renders in every format you need.</p></div>
  </div>
</div></section>

<section id="contact" class="contact"><div class="wrap">
  <div class="eyebrow">Contact</div>
  <h2 class="display">Let's make it move</h2>
  <p class="muted">Tell me what you're launching or explaining, and where it will run.</p>
  <a class="mail" href="mailto:${EMAIL}?subject=Motion%20design%20project">${EMAIL}</a>
</div></section>`,
});
fs.writeFileSync(path.join(ROOT, "index.html"), home);

// ---------------------------------------------------------------- case studies
fs.mkdirSync(path.join(ROOT, "work"), { recursive: true });
const cs = (slug, title, desc, inner) => {
  const idx = WORK.findIndex((w) => w.slug === slug);
  const prev = WORK[(idx + WORK.length - 1) % WORK.length], next = WORK[(idx + 1) % WORK.length];
  fs.writeFileSync(path.join(ROOT, "work", slug + ".html"), page({ title: `${title} — ${NAME}`, desc, depth: 1, current: "work", body: inner + `
<section><div class="wrap next"><a class="btn" href="${prev.slug}.html">← ${prev.title}</a><a class="btn primary" href="../index.html#contact">Start a project</a><a class="btn" href="${next.slug}.html">${next.title} →</a></div></section>` }));
};
const facts = (rows) => `<div class="facts">${rows.map(([k, v]) => `<div><b>${k}</b>${v}</div>`).join("")}</div>`;

cs("nova", "NOVA", "A 15-second vertical launch film for a pair of earbuds.", `
<header class="cs-hero"><div class="wrap">
  <div class="eyebrow">01 · Product launch</div>
  <h1 class="display">NOVA</h1>
  <p class="sum">A premium vertical launch spot for wireless earbuds, built around one shape that never cuts: a line of light becomes the case, the earbud, an equaliser, and finally the O in the NOVA logo.</p>
  ${facts([["Format", "15s · 1080×1920"], ["Role", "Concept, design, animation, sound"], ["Channels", "Reels · TikTok · Shorts"], ["Type", "Spec ad · fictional brand"]])}
  ${vid("../assets/video/nova.mp4", "../assets/img/poster-nova.jpg", { cls: "vertical" })}
</div></header>
<section><div class="wrap prose">
  <h3>The challenge</h3>
  <p>Tech launch ads tend to look the same: product spins, glow and a tagline. NOVA needed to feel premium and hold attention for 15 seconds with no footage and no 3D model.</p>
  <h3>The approach</h3>
  <ul><li>One continuous shape carries the whole film, so the eye never has to look for the next thing.</li>
  <li>Every move uses physical spring motion with overshoot and settle, not stock ease curves.</li>
  <li>The type is short and timed to the sound hits: four lines, each with room to land.</li></ul>
  <h3>Craft notes</h3>
  <ul><li>Real motion blur: each frame blends up to 16 sub-frames across a 180° shutter, so fast moves smear like film.</li>
  <li>Original synthesized score and sound design, mastered for phone speakers.</li>
  <li>Text kept clear of the Reels and TikTok interface zones.</li></ul>
  <p class="note">Spec work: NOVA is a fictional brand created for this portfolio.</p>
</div></section>`);

cs("clown-club", "Clown Club — Pack & Unpack", "A 15-second product film for the Clown Club clothing label.", `
<header class="cs-hero"><div class="wrap">
  <div class="eyebrow">02 · Product motion</div>
  <h1 class="display">Clown Club — Pack &amp; Unpack</h1>
  <p class="sum">Seven tees leave the rail, fold into a box, get taped and shipped, then unbox top-down and land back on the rail. The whole order journey in 15 seconds.</p>
  ${facts([["Format", "15s · 1920×1080"], ["Role", "Concept, design, animation, sound"], ["Brand", "Clown Club (my label)"], ["Captions", "Pick it. Pack it. Ship it. Wear it."]])}
  ${vid("../assets/video/clown-club.mp4", "../assets/img/poster-clown-club.jpg")}
</div></header>
<section><div class="wrap prose">
  <h3>The challenge</h3>
  <p>Drawn clothes looked cheap, so the garments had to come from real photos while staying fully animated: they fly, fold and stack on the beat.</p>
  <h3>The approach</h3>
  <ul><li>One photographed tee, cut out and recoloured into seven colourways that keep the real fabric shading.</li>
  <li>The story is a single camera move: rail → box → push-in → cut to top-down unboxing → back to the rail.</li>
  <li>Each tee drops into the box on an eighth note; tape, label and box bounces sit on the beat.</li></ul>
  <h3>Craft notes</h3>
  <ul><li>Squash and stretch on the box, with motion blur on every fast move.</li>
  <li>Four story captions keep the film readable with the sound off.</li></ul>
  <p class="note">Tee photo by Avtar Singh on Unsplash (Unsplash License).</p>
</div></section>`);

cs("bez-and-the-boos", "Bez & the Boos", "A 15-second Halloween character music video.", `
<header class="cs-hero"><div class="wrap">
  <div class="eyebrow">03 · Character music video</div>
  <h1 class="display">Bez &amp; the Boos</h1>
  <p class="sum">Bez the mascot wanders onto a dark stage and wakes up a band, one beat at a time: a ghost on organ, a pumpkin on drums, a bat on sax and a cat on double bass.</p>
  ${facts([["Format", "15s · 1920×1080"], ["Role", "Characters, animation, music"], ["Occasion", "Halloween"], ["Type", "Self-initiated"]])}
  ${vid("../assets/video/bez-and-the-boos.mp4", "../assets/img/poster-bez-and-the-boos.jpg")}
</div></header>
<section><div class="wrap prose">
  <h3>The challenge</h3>
  <p>Seasonal posts get one scroll's worth of attention. The film had to be instantly readable, a little funny and built to loop.</p>
  <h3>The approach</h3>
  <ul><li>Each new musician enters on its own instrument's first note, so you hear the band build as you see it.</li>
  <li>The title letters drop in on the beat, then the whole band plays together for the payoff.</li>
  <li>A limited palette (charcoal, cream, one orange) keeps five characters calm on screen.</li></ul>
  <h3>Craft notes</h3>
  <ul><li>Characters and instruments are drawn in code, with every hop and hit driven from one shared beat timeline.</li>
  <li>Original score with each part arranged per character.</li></ul>
</div></section>`);

cs("no-after-effects", "No After Effects", "A 12-second character film: a mascot escapes a keyboard into an app.", `
<header class="cs-hero"><div class="wrap">
  <div class="eyebrow">04 · Character motion</div>
  <h1 class="display">No After Effects</h1>
  <p class="sum">Bez pops out of a keyboard keycap, dives into the monitor and builds a motion graphic in a fictional animation app by hopping on its buttons and keyframes, landing on every beat. The film itself is made entirely in code, with no After Effects.</p>
  ${facts([["Format", "12s · 1920×1080"], ["Role", "Character, UI design, animation, sound"], ["Product", "Fictional app “Loopwork”"], ["Type", "Self-initiated"]])}
  ${vid("../assets/video/no-after-effects.mp4", "../assets/img/poster-no-after-effects.jpg")}
</div></header>
<section><div class="wrap prose">
  <h3>The challenge</h3>
  <p>UI promos usually show the interface on its own. This one needed a character so the product feels alive, and the motion had to follow the music.</p>
  <h3>The approach</h3>
  <ul><li>Every hop changes something: it presses a tool, stamps a keyframe or plays back the timeline, and 17 landings sit on a 120 BPM grid.</li>
  <li>The app logic is real: stamped keys snap the comp to a pose, and the playhead rewinds to play back the eased move.</li>
  <li>Squash on landing and stretch in the air give a small character real weight.</li></ul>
  <h3>Craft notes</h3>
  <ul><li>A deterministic, frame-accurate pipeline: HTML/SVG animation rendered frame by frame, then encoded with sound.</li>
  <li>Original beat and sound effects, with the timing driven by the same timeline as the animation.</li></ul>
</div></section>`);

cs("raise-trap", "The Raise Trap", "A 60-second animated explainer about lifestyle inflation.", `
<header class="cs-hero"><div class="wrap">
  <div class="eyebrow">05 · Animated explainer</div>
  <h1 class="display">The Raise Trap</h1>
  <p class="sum">A warm, character-led explainer that makes one money idea stick: a raise only makes you richer if your spending doesn't rise with it.</p>
  ${facts([["Format", "60s · 1920×1080"], ["Role", "Script, design, animation, sound"], ["Audience", "Young professionals"], ["Type", "Self-initiated"]])}
  ${vid("../assets/video/raise-trap.mp4", "../assets/img/poster-raise-trap.jpg")}
</div></header>
<section><div class="wrap prose">
  <h3>The challenge</h3>
  <p>Lifestyle inflation is invisible: no single upgrade feels like the problem. The video had to make that slow creep visible in a minute, without lecturing.</p>
  <h3>The approach</h3>
  <ul><li>One character, Theo, carries the story: raise → upgrades → the chart that gives it away → the fix.</li>
  <li>The key frame is a chart where income steps up and spending follows — the "what he keeps" gap never grows.</li>
  <li>The fix is a single concrete action (split every raise on payday), then proved with real numbers.</li></ul>
  <h3>Craft notes</h3>
  <ul><li>Every reveal is timed to the spoken word it illustrates; captions are burned in for sound-off viewing.</li>
  <li>Figures are calculated, not guessed: $300/month at 5%/yr compounded monthly → $20,402 after five years, stated on screen.</li>
  <li>Original score and sound effects; warm sticker-style design system (cream, charcoal outlines, coral accents).</li></ul>
</div></section>
<section><div class="wrap">
  <div class="eyebrow">Process</div>
  <h3 style="font-size:24px;margin-top:8px">Storyboard — approved before any animation</h3>
  <div class="board">${[1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) => `<img src="../assets/img/rt-board-${i}.jpg" alt="Storyboard frame ${i}" loading="lazy">`).join("")}</div>
  <p class="note">Figures are illustrative and not financial advice.</p>
</div></section>`);

cs("corvo", "CORVO Knockout", "A three-format social ad pack for a boxing-glove launch.", `
<header class="cs-hero"><div class="wrap">
  <div class="eyebrow">06 · Social ad pack</div>
  <h1 class="display">CORVO Knockout</h1>
  <p class="sum">A loud, punch-timed ad pack for a boxing-glove launch: one design system, three deliverables, built to stop the scroll with the sound off.</p>
  ${facts([["Deliverables", "15s 9:16 · 6s 16:9 · 15s 1:1"], ["Role", "Concept, design, animation, music"], ["Audience", "Beginner–intermediate boxers"], ["Type", "Spec ad · fictional brand"]])}
  <div class="formats">
    <figure>${vid("../assets/video/corvo-hero.mp4", "../assets/img/poster-corvo.jpg")}<figcaption>Hero · 15s · 9:16 (Reels / TikTok)</figcaption></figure>
    <figure>${vid("../assets/video/corvo-square.mp4", "../assets/img/poster-corvo-square.jpg")}<figcaption>Feed · 15s · 1:1</figcaption></figure>
    <figure>${vid("../assets/video/corvo-bumper.mp4", "../assets/img/poster-corvo-bumper.jpg")}<figcaption>Bumper · 6s · 16:9 (YouTube)</figcaption></figure>
  </div>
</div></header>
<section><div class="wrap prose">
  <h3>The challenge</h3>
  <p>Product ads live or die in the first second, are mostly watched muted, and have to ship in several formats at once.</p>
  <h3>The approach</h3>
  <ul><li>Hook → claim → proof → detail → offer → CTA, in 15 seconds.</li>
  <li>Every cut and callout lands on a beat of an original 120 BPM score; the text carries the message without sound.</li>
  <li>The bumper and the square cut are built from the same design system and motion, re-laid out per format — change the price once, every cut updates.</li></ul>
  <h3>Craft notes</h3>
  <ul><li>The glove and the crow-wing mark are drawn in code — no stock photos, no licensing risk.</li>
  <li>Text kept clear of the Reels/TikTok interface zones.</li></ul>
</div></section>
<section><div class="wrap">
  <div class="eyebrow">Process</div>
  <h3 style="font-size:24px;margin-top:8px">Storyboard — six beats, approved before animation</h3>
  <div class="board tall">${[1, 2, 3, 4, 5, 6].map((i) => `<img src="../assets/img/corvo-board-${i}.jpg" alt="Storyboard frame ${i}" loading="lazy">`).join("")}</div>
  <p class="note">Spec work: CORVO is a fictional brand created for this portfolio. Product, price and claims are invented.</p>
</div></section>`);

cs("pulse", "Pulse", "A 15-second SaaS launch promo, remastered.", `
<header class="cs-hero"><div class="wrap">
  <div class="eyebrow">07 · Launch promo · remaster</div>
  <h1 class="display">Pulse</h1>
  <p class="sum">A 15-second launch promo for a productivity app — logo sting, live dashboard, tagline and end card — rebuilt from my first version with readable UI, sound and smoother transitions.</p>
  ${facts([["Format", "15s · 1920×1080"], ["Role", "Design, animation, sound"], ["Product", "Fictional app"], ["Version", "v2 remaster"]])}
  ${vid("../assets/video/pulse-v2.mp4", "../assets/img/poster-pulse.jpg")}
</div></header>
<section><div class="wrap">
  <div class="eyebrow">Before / after</div>
  <div class="ba">
    <figure>${vid("../assets/video/pulse-v1.mp4", "../assets/img/poster-pulse-v1.jpg")}<figcaption><b>v1</b> · silent, small UI text, a layout jump at 7s, static 3.5s end card</figcaption></figure>
    <figure>${vid("../assets/video/pulse-v2.mp4", "../assets/img/poster-pulse.jpg")}<figcaption><b>v2</b> · scored, UI fills the frame, logo docks into the header, designed wipe, living end card</figcaption></figure>
  </div>
</div></section>
<section><div class="wrap prose">
  <h3>What changed</h3>
  <ul><li>Original score with UI sound design: a tick lands on every task check.</li>
  <li>Dashboard enlarged so every label reads on a phone (task text 32px).</li>
  <li>The logo lockup now travels into the dashboard header in one move.</li>
  <li>A lime wipe and a heartbeat end card replace a static flash and a frozen hold.</li></ul>
</div></section>`);

cs("make-it-move", "Make It Move", "A 15-second vertical kinetic type piece, remastered.", `
<header class="cs-hero"><div class="wrap">
  <div class="eyebrow">08 · Kinetic type · remaster</div>
  <h1 class="display">Make It Move</h1>
  <p class="sum">A vertical kinetic-type study — chrome type, a silver sphere and a score cut to the hits — rebuilt from my first version to fix rendering glitches and use the full 9:16 frame.</p>
  ${facts([["Format", "15s · 1080×1920"], ["Role", "Design, animation, music"], ["Type", "Self-initiated"], ["Version", "v2 remaster"]])}
</div></header>
<section><div class="wrap">
  <div class="eyebrow">Before / after</div>
  <div class="ba">
    <figure>${vid("../assets/video/make-it-move-v1.mp4", "../assets/img/poster-mim-v1.jpg", { cls: "vertical" })}<figcaption><b>v1</b> · stray glitch blocks, empty lower half, disconnected sphere</figcaption></figure>
    <figure>${vid("../assets/video/make-it-move-v2.mp4", "../assets/img/poster-mim.jpg", { cls: "vertical" })}<figcaption><b>v2</b> · glitch fixed at the root, type fills the frame, the sphere becomes the full stop</figcaption></figure>
  </div>
</div></section>
<section><div class="wrap prose">
  <h3>What changed</h3>
  <ul><li>Found the cause of v1's stray blocks — a chrome text fill breaking on individually animated letters — and fixed it per glyph.</li>
  <li>Re-composed for vertical: larger type, frame furniture, a progress hairline.</li>
  <li>The sphere is now a motif: it drops in, zooms through to the next beat and lands as the period of "MOVE."</li>
  <li>An original score with hits on every cut, mastered for social.</li></ul>
</div></section>`);

console.log("built: index.html + work/*.html");
