// build.mjs — generates the portfolio pages (index.html + work/*.html). Static, no dependencies.
//   node build.mjs
// Edit NAME / EMAIL / SERVICES below; pages are rebuilt from these.
import fs from "node:fs";
import path from "node:path";
const ROOT = path.dirname(new URL(import.meta.url).pathname.replace(/^\/(\w:)/, "$1"));

const NAME = "Clown";
const EMAIL = "tun832061@gmail.com";
const YEAR = 2026;

const page = ({ title, desc, depth = 0, body, current, noindex = false, bodyClass = "" }) => {
  const r = depth ? "../" : "";
  const link = (href, label, key, cls = "") => `<li${cls ? ` class="${cls}"` : ""}><a href="${r}${href}"${current === key ? ' aria-current="page"' : ""}>${label}</a></li>`;
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${title}</title>
<meta name="description" content="${desc}">
${noindex ? '<meta name="robots" content="noindex">\n' : ""}<meta property="og:title" content="${title}">
<meta property="og:description" content="${desc}">
<meta property="og:image" content="${r}assets/img/poster-showreel.jpg">
<link rel="stylesheet" href="${r}assets/site.css">
</head>
<body${bodyClass ? ` class="${bodyClass}"` : ""}>
<nav class="nav"><div class="wrap">
  <a class="logo" href="${r}index.html">${NAME.toUpperCase()}<span>.</span></a>
  <ul>${link("index.html#work", "Work", "work")}${link("index.html#services", "Services", "services", "hide-sm")}<li><a class="nav-cta" href="mailto:${EMAIL}">Email me</a></li></ul>
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
  { slug: "corvo", title: "CORVO Knockout", meta: "Social ad pack · 9:16 · 1:1 · 16:9", poster: "poster-corvo-bumper.jpg",
    tags: ["Product ad", "3 formats", "Kinetic type", "Sound design"] },
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
  { slug: "pulse", title: "Pulse", meta: "SaaS launch promo · 15s · remaster", poster: "poster-pulse.jpg",
    tags: ["UI animation", "Logo sting", "Launch promo"] },
  { slug: "make-it-move", title: "Make It Move", meta: "Kinetic type · 15s · 9:16 · remaster", poster: "poster-mim.jpg",
    tags: ["Kinetic type", "Vertical", "Score"] },
];

// ---------------------------------------------------------------- new pieces (portfolio rebuild)
// Six self-initiated pieces from the rebuild plan. Each one gets a page now; it joins the
// home grid automatically once its main video exists. Drop files in with these names:
//   assets/video/<slug>.mp4               main video (this is what flips the piece to "ready")
//   assets/video/<slug>-<extra>.mp4       extra cuts listed in `extras` below
//   assets/img/<slug>/poster.jpg          card + player poster
//   assets/img/<slug>/moodboard.jpg       process: moodboard
//   assets/img/<slug>/frame-1.jpg …       process: styleframes (up to 6)
//   assets/img/<slug>/board-1.jpg …       process: storyboard / animatic stills (up to 12)
// Fill `role`, `tools` and `notes` (one line per process image: the decision and why) as you go.
const has = (rel) => fs.existsSync(path.join(ROOT, rel));
const NEW = [
  { slug: "the-last-watch", title: "The Last Watch", kind: "Story trailer", format: "50s · 16:9", vertical: false,
    tags: ["Story", "Parallax", "Match cuts", "Sound design"],
    sum: "A title sequence for an original fantasy short. An old royal guard keeps the last watch over a sleeping city the night before it falls — quiet, cinematic, and hopeful at the end.",
    brief: "Carry a story with motion alone: mood, pacing, a character and a turn. Flat 2D silhouettes in layered parallax, deep navy, lantern amber and paper white, with a serif title face.",
    extras: [["teaser", "9:16 teaser · 0:30–0:50", true]],
    tools: ["Made in code: HTML canvas, frame-by-frame render", "Original score and sound design"],
    notes: {
      "frame-1": "The film opens on one light in the dark. Everything after it is about that lantern.",
      "frame-2": "The guard stands against the sky, not the buildings, so his silhouette reads at a glance.",
      "frame-3": "A close-up with no face: the hand tightening on the hilt carries the fear.",
      "frame-4": "During the fast cuts the moon sits behind each silhouette, so every 0.5-second shot reads instantly.",
      "frame-5": "The turn: a second lantern, and the city answers. The light spreads outward from the flame.",
    } },
  { slug: "say-it-slower", title: "Say It Slower", kind: "Kinetic typography", format: "35s · 16:9 + 9:16", vertical: false,
    tags: ["Kinetic type", "Voice sync", "Vertical"],
    sum: "A spoken-word piece about patience in a fast world, set entirely in type. Every word lands on the voice.",
    brief: "Prove type skill and timing. Black, off-white and one accent colour, a single grotesk in three weights, original words in my own voice. Every word lands on the syllable. The 9:16 is re-composed, not cropped.",
    extras: [["vertical", "Re-composed 9:16", true]],
    role: "Words, voice, design, animation, sound",
    tools: ["Made in code: HTML canvas, frame-by-frame render", "Every word timed to the voice by forced alignment", "Original sound design"],
    notes: {
      "frame-1": "FAST slams in with motion blur. The opening is as impatient as the line.",
      "frame-2": "Each new FAST line pushes the last one up and shrinks it, faster each time.",
      "frame-3": "Then everything stops. TIME stands alone while its letter-spacing slowly opens.",
      "frame-4": "The one frame from the film strip fills the screen and becomes the next scene.",
      "frame-5": "The timecode counts up to exactly one second, then freezes.",
      "frame-6": "The words arrive as posts in a feed, until SCROLL AWAY flicks the feed off screen.",
      "frame-7": "The last word breaks into letters that bounce on their own, then clear for the name.",
    } },
  { slug: "kettle-and-kiln", title: "Kettle & Kiln", kind: "Brand identity in motion", format: "25s · 16:9 + 1:1", vertical: false,
    tags: ["Logo animation", "Motion system", "Templates"],
    sum: "A motion system for an invented coffee roaster: a logo built from a pour, one circle transition reused across price tags, menu boards and stories, plus lower-third and end-card templates.",
    brief: "Build a motion system a brand can reuse, not just a logo animated once. Warm, crafted, slow-poured.",
    extras: [["square", "1:1 re-compose", false], ["sting", "Logo sting · 3.6 s", false]],
    tools: ["Made in code: HTML canvas, frame-by-frame render", "Original music and sound design"],
    notes: {
      "frame-1": "The logo is made by its own idea: coffee pours in and draws the cup.",
      "frame-2": "A cup seen from above, plus a serif wordmark. The ampersand is the only kiln orange.",
      "frame-3": "The motion guideline: one ease, one duration, one transition, written down for the team.",
      "frame-4": "The same circle wipe on a price tag, a menu board and a story, so every surface feels related.",
      "frame-5": "Lower third and end card templates: practical pieces a client actually reuses.",
      "frame-6": "Steam on the settled logo, so the film loops back to where it started.",
    } },
  { slug: "splitly", title: "Splitly", kind: "Explainer / app UI", format: "50s · 16:9", vertical: false,
    tags: ["Explainer", "UI animation", "Voiceover"],
    sum: "An explainer for an invented bill-splitting app: snap the receipt, tap who had what, and everyone gets a link.",
    brief: "Make something clear, not just pretty. Friendly and fast for young adults, a clean UI with one bright brand colour, every move under 400 ms and eased like a real product.",
    extras: [],
    tools: ["Made in code: HTML canvas, frame-by-frame render", "Original music and UI sound design"],
    notes: {
      "frame-1": "The problem in one image: scrambling numbers and four friends pointing at each other.",
      "frame-2": "The camera screen keeps the real receipt in frame, so the next step is obvious.",
      "frame-3": "Each friend has one colour from start to finish, so who had what reads at a glance.",
      "frame-4": "The pie chart turns the maths into a picture: the shares add up to exactly $121.90.",
      "frame-5": "Each payment lands with a tick and a sound, and the bar fills to 4 of 4 paid.",
      "frame-6": "The logo is two halves of one circle: the product idea in a single mark.",
    } },
  { slug: "kicks-drop", title: "Kicks Drop", kind: "Social ad pack", format: "3 ads · 9:16 / 1:1 / 4:5", vertical: true,
    tags: ["Product ad", "3 formats", "Sound-off"],
    sum: "A three-ad launch pack for an invented sneaker colourway — a hook, a product ad and an offer — each readable with the sound off.",
    brief: "Deliver what most paying clients buy: short ads that stop the scroll, in every format, fast. Text kept clear of the TikTok and Reels interface.",
    main: "Ad A · Hook · 6s",
    extras: [["product", "Ad B · Product · 15s", true], ["offer", "Ad C · Offer · 10s", true], ["square", "Ad A re-composed for 1:1", false]],
    tools: ["Made in code: sneaker drawn and animated in HTML canvas", "Original beat and sound design"],
    notes: {
      "frame-1": "The hook: the box lid slams off toward camera in the first half second.",
      "frame-2": "The 360 spin is eight stills 45 degrees apart, like a product turntable shoot.",
      "frame-3": "One reason at a time, each with a line to the exact part of the shoe.",
      "frame-4": "The end card: logo, price and a pulsing button, all inside the safe area.",
      "frame-5": "The offer hook: −20% crashes in and shakes. It reads with the sound off.",
      "frame-6": "The code is the last thing on screen, big enough to read on a phone.",
      "frame-7": "The same hook re-composed for 1:1: the title, shoe and date are rearranged, not cropped.",
    } },
  { slug: "lagos-in-24-frames", title: "Lagos in 24 Frames", kind: "Experimental", format: "20s", vertical: false,
    tags: ["Experimental", "Frame-by-frame", "Shape morph"],
    sum: "Twenty-four shots of under a second each, each a different motion technique, one palette, cut to a single drum loop: the danfo, the market, the generator hum, the traffic light.",
    brief: "No client. The rule: 24 shots under a second each, each a different technique, one palette, one drum loop. Then a single slow shot. Show my own voice and my craft ceiling, with the same finish as the client-style pieces.",
    extras: [],
    tools: ["Made in code: HTML canvas, frame-by-frame render", "Original drum loop and sound design"],
    notes: {
      "frame-1": "Shots 1–10 are one shape morphing on every beat: sun, road, window, umbrella, traffic light.",
      "frame-2": "The generator hum becomes a shape. Colours flip on every beat, so each shot is its own frame.",
      "frame-3": "Shots 11–24 are the same danfo, drawn a different way every half second. This one is flat 2D.",
      "frame-4": "A halftone version: the bus built only from dots.",
      "frame-5": "Pixel art, one of fourteen techniques in seven seconds.",
      "frame-6": "The only slow shot: five seconds of sunset over the bridge, with grain and tiny danfos crossing.",
      "frame-7": "The title builds from the shapes that opened the film.",
    } },
  { slug: "behind-the-frame", title: "Behind the Frame", kind: "Talking-head edit", format: "45s · 9:16 + 16:9", vertical: true,
    tags: ["Talking head", "Animated captions", "B-roll", "Vertical"],
    sum: "A creator-style talking-head edit, with me as the speaker: animated captions, punch-ins, B-roll cut from my own work, and sound design. Shown next to the raw footage it came from.",
    brief: "Turn one plain, locked-off take into a video people watch to the end. Built 9:16 first for Reels, TikTok and Shorts, with captions that read with the sound off and stay clear of the app interface.",
    main: "Edited · 9:16",
    extras: [["raw", "Raw footage (before)", true], ["wide", "16:9 cut", false]] },
].map((n) => ({ ...n, role: n.role || "Concept, design, animation, sound", tools: n.tools || [], notes: n.notes || {},
  ready: has(`assets/video/${n.slug}.mp4`), meta: `${n.kind} · ${n.format}` }));
for (const n of NEW) n.poster = has(`assets/img/${n.slug}/poster.jpg`) ? `${n.slug}/poster.jpg` : null;

// ---------------------------------------------------------------- homepage picks
// FEATURED is the homepage, in order: one piece per skill a hirer looks for. To swap a piece,
// change its slug here. A featured piece only appears once its video exists; until then the
// homepage is topped up with your other finished work so it always shows HOME_COUNT pieces.
// Pieces left off the homepage keep their pages, so you can still send their links directly.
const FEATURED = [
  "corvo",              // bold commercial work first
  "nova",               // premium product launch
  "splitly",            // app / UI explainer
  "pulse",              // SaaS launch promo
  "the-last-watch",     // story, in the middle as proof of range
  "kettle-and-kiln",    // brand system
  "say-it-slower",      // kinetic type
  "kicks-drop",         // social ads
  "behind-the-frame",   // talking-head edit
  "lagos-in-24-frames", // your own voice
  "clown-club",
  "no-after-effects",
];
const HOME_COUNT = 8;
const ALL = [...NEW, ...WORK.map((w) => ({ ...w, ready: true }))];
const bySlug = Object.fromEntries(ALL.map((w) => [w.slug, w]));
for (const f of FEATURED) if (!bySlug[f]) throw new Error(`FEATURED has unknown slug "${f}"`);
const picks = FEATURED.map((f) => bySlug[f]).filter((w) => w.ready);
// Never on the homepage (their pages stay up for direct links).
const OFF_HOME = ["raise-trap", "bez-and-the-boos"];
const HOME = [...picks, ...WORK.filter((w) => !picks.includes(bySlug[w.slug]) && !OFF_HOME.includes(w.slug))].slice(0, HOME_COUNT);
if (HOME.length % 2 && HOME.length > 1) HOME.pop(); // two-column grid: keep rows full
// prev/next on case studies: homepage pieces first, then every other finished piece
const SHOWN = [...HOME, ...ALL.filter((w) => w.ready && !HOME.includes(w))];

// ---------------------------------------------------------------- home
const home = page({
  title: `${NAME} — Motion designer`,
  desc: "Motion designer for story, brand, product and social: title sequences, explainers, brand systems and ad packs.",
  bodyClass: "home",
  body: `
<header class="stage">
  <video class="stage-video" src="assets/video/showreel.mp4" poster="assets/img/poster-showreel.jpg" autoplay muted loop playsinline preload="auto"></video>
  <div class="stage-shade"></div>
  <div class="wrap stage-copy">
    <h1><span class="display">${NAME}<i>.</i></span> Motion designer for story, brand, product and social.</h1>
    <div class="stage-actions">
      <button class="btn primary" type="button" data-sound>▶ Watch the reel with sound</button>
      <a class="btn ghost" href="#work">See the work ↓</a>
    </div>
  </div>
</header>

<section id="work" class="work"><div class="wrap">
  <div class="work-head"><h2 class="display">Selected work</h2><p class="muted">${HOME.length} projects · tap any to see the brief, the process and the final film.</p></div>
  <div class="reelgrid">
${HOME.map((w, i) => {
    const prev = has(`assets/video/preview/${w.slug}.mp4`) ? `assets/video/preview/${w.slug}.mp4` : "";
    const img = w.poster ? `assets/img/${w.poster}` : "";
    return `    <a class="tile" href="work/${w.slug}.html">
      <div class="tile-media">${prev ? `<video src="${prev}"${img ? ` poster="${img}"` : ""} muted loop playsinline preload="none" data-preview></video>` : img ? `<img src="${img}" alt="" loading="lazy">` : ""}</div>
      <div class="tile-text"><span class="tile-num">${String(i + 1).padStart(2, "0")}</span><h3>${w.title}</h3><span class="tile-meta">${w.meta}</span></div>
    </a>`;
  }).join("\n")}
  </div>
</div></section>

<section id="services" class="make"><div class="wrap">
  <h2 class="display">What I make</h2>
  <ul class="make-list">
    <li><b>Story &amp; title sequences</b><span>Trailers, openers and short films that carry a mood and a turn.</span></li>
    <li><b>Explainers &amp; product UI</b><span>One idea made clear, with interfaces that move like the real product.</span></li>
    <li><b>Brand motion systems</b><span>Logo animation plus the transitions and templates your team reuses.</span></li>
    <li><b>Social ad packs</b><span>Hooks in the first second, built sound-off, in every format you post.</span></li>
  </ul>
  <p class="make-how muted">Every project runs brief → styleframes → animatic → animation → sound → delivery, and you approve each step before the next one.</p>
</div></section>

<section id="contact" class="contact"><div class="wrap">
  <p class="muted">Got something to launch, explain or tell?</p>
  <a class="mail display" href="mailto:${EMAIL}?subject=Motion%20design%20project">${EMAIL}</a>
  <p class="muted small">I reply within a day, with a rough idea of how I'd approach it.</p>
</div></section>
<script>
(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const stage = document.querySelector(".stage-video");
  if (reduce) stage.removeAttribute("autoplay"), stage.pause();
  document.querySelector("[data-sound]").addEventListener("click", (e) => {
    stage.currentTime = 0; stage.muted = false; stage.loop = false; stage.controls = true; stage.play();
    document.body.classList.add("watching"); e.currentTarget.blur();
  });
  stage.addEventListener("ended", () => { document.body.classList.remove("watching"); stage.muted = true; stage.loop = true; stage.controls = false; stage.play(); });
  const vids = document.querySelectorAll("[data-preview]");
  if (reduce || !("IntersectionObserver" in window)) return;
  const io = new IntersectionObserver((es) => es.forEach((x) => { const v = x.target; if (x.isIntersecting) { v.preload = "auto"; v.play().catch(() => {}); } else v.pause(); }), { threshold: 0.35 });
  vids.forEach((v) => io.observe(v));
})();
</script>`,
});
fs.writeFileSync(path.join(ROOT, "index.html"), home);

// ---------------------------------------------------------------- case studies
fs.mkdirSync(path.join(ROOT, "work"), { recursive: true });
const cs = (slug, title, desc, inner) => {
  const idx = SHOWN.findIndex((w) => w.slug === slug);
  const prev = SHOWN[(idx + SHOWN.length - 1) % SHOWN.length], next = SHOWN[(idx + 1) % SHOWN.length];
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

// ---------------------------------------------------------------- new piece pages (case study template)
// Order: video, brief, my role, process (each image with its one-line decision), tools.
// Until the main video exists the page shows "In production" and is kept out of search.
const esc = (t) => t.replace(/&(?!amp;)/g, "&amp;");
for (const n of NEW) {
  const img = (f) => `../assets/img/${n.slug}/${f}`;
  const poster = n.poster ? `../assets/img/${n.poster}` : "";
  const shot = (f, alt) => has(`assets/img/${n.slug}/${f}`)
    ? `<figure><img src="${img(f)}" alt="${alt}" loading="lazy">${n.notes[f.replace(".jpg", "")] ? `<figcaption>${n.notes[f.replace(".jpg", "")]}</figcaption>` : ""}</figure>` : "";
  const series = (prefix, max, label) => Array.from({ length: max }, (_, i) => shot(`${prefix}-${i + 1}.jpg`, `${label} ${i + 1}`)).join("");
  const mood = shot("moodboard.jpg", "Moodboard"), frames = series("frame", 6, "Styleframe"), boards = series("board", 12, "Storyboard frame");
  const process = [
    mood && `<h3 class="sub">Moodboard</h3><div class="shots one">${mood}</div>`,
    frames && `<h3 class="sub">Styleframes</h3><div class="shots">${frames}</div>`,
    boards && `<h3 class="sub">Storyboard &amp; animatic</h3><div class="shots">${boards}</div>`,
  ].filter(Boolean).join("");
  const extras = n.extras.filter(([k]) => has(`assets/video/${n.slug}-${k}.mp4`));
  const video = !n.ready
    ? `<div class="pending"><b>In production</b><span>The final film and process frames will appear here.</span></div>`
    : extras.length || n.main
      ? `<div class="cuts"><figure>${vid(`../assets/video/${n.slug}.mp4`, poster, { cls: n.vertical ? "vertical" : "" })}<figcaption>${n.main || "Main cut"}</figcaption></figure>${extras.map(([k, label, vert]) =>
          `<figure>${vid(`../assets/video/${n.slug}-${k}.mp4`, "", { cls: vert ? "vertical" : "" })}<figcaption>${label}</figcaption></figure>`).join("")}</div>`
      : vid(`../assets/video/${n.slug}.mp4`, poster, { cls: n.vertical ? "vertical" : "" });
  const nav = n.ready && SHOWN.length > 1 ? (() => {
    const i = SHOWN.findIndex((w) => w.slug === n.slug), p = SHOWN[(i + SHOWN.length - 1) % SHOWN.length], x = SHOWN[(i + 1) % SHOWN.length];
    return `<a class="btn" href="${p.slug}.html">← ${p.title}</a><a class="btn primary" href="../index.html#contact">Start a project</a><a class="btn" href="${x.slug}.html">${x.title} →</a>`;
  })() : `<a class="btn" href="../index.html#work">← All work</a><a class="btn primary" href="../index.html#contact">Start a project</a>`;
  const body = `
<header class="cs-hero"><div class="wrap">
  <div class="eyebrow">${n.kind}</div>
  <h1 class="display">${esc(n.title)}</h1>
  <p class="sum">${n.sum}</p>
  ${facts([["Format", n.format], ["Role", n.role], ["Brief", "Self-initiated"], ["Year", YEAR]])}
  ${video}
</div></header>
<section><div class="wrap prose">
  <h3>The brief</h3>
  <p>${n.brief}</p>
  <h3>My role</h3>
  <p>${n.role}.</p>
  ${n.tools.length ? `<h3>Tools</h3><p>${n.tools.join(" · ")}</p>` : ""}
  <p class="note">Self-initiated brief: ${esc(n.title)} is a fictional project made for this portfolio.</p>
</div></section>
${process ? `<section><div class="wrap"><div class="eyebrow">Process</div>${process}</div></section>` : ""}
<section><div class="wrap next">${nav}</div></section>`;
  fs.writeFileSync(path.join(ROOT, "work", n.slug + ".html"),
    page({ title: `${esc(n.title)} — ${NAME}`, desc: n.sum, depth: 1, current: "work", noindex: !n.ready, body }));
}

console.log(`built: index.html + work/*.html · new pieces ready: ${NEW.filter((n) => n.ready).length}/${NEW.length}`);
