// render.cjs — renders an episode to MP4 (frame-by-frame canvas -> ffmpeg) or still frames for checking.
//   node render.cjs ../ep01                      -> ep01/build/video.mp4 (1920x1080) + captions.srt
//   node render.cjs ../ep01 --stills 3,40,95     -> ep01/build/still-<sec>.png
//   options: --script short.json  --size 1080x1920  --out short.mp4  --audio mix-short.wav  --timeline timeline-short.json
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const fs = require('fs'); const path = require('path');
const args = process.argv.slice(2); const ep = path.resolve(args[0]);
const opt = k => { const i = args.indexOf('--' + k); return i > 0 ? args[i + 1] : null; };
const B = path.join(ep, 'build');
const script = JSON.parse(fs.readFileSync(path.join(ep, opt('script') || 'script.json')));
const tl = JSON.parse(fs.readFileSync(path.join(B, opt('timeline') || 'timeline.json')));
const [w, h] = (opt('size') || '1920x1080').split('x').map(Number);
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: w, height: h } }); p.on('pageerror', e => console.log('ERR', e.message)); p.on('console', m => console.log('LOG', m.text()));
  await p.goto('file://' + path.join(__dirname, 'player.html'));
  await p.evaluate(([s, t, w, h]) => window.init(s, t, w, h), [script, tl, w, h]);
  const stills = opt('stills');
  if (stills) {
    for (const s of stills.split(',')) {
      const d = await p.evaluate(f => { render(f); return document.getElementById('c').toDataURL('image/png').split(',')[1]; }, Math.round(parseFloat(s) * 30));
      fs.writeFileSync(path.join(B, `still-${s}.png`), Buffer.from(d, 'base64'));
    }
    await b.close(); return console.log('stills done');
  }
  const out = path.join(B, opt('out') || 'video.mp4'), audio = path.join(B, opt('audio') || 'mix.wav');
  const N = Math.round(tl.dur * 30);
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-', '-i', audio,
    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = 0; f < N; f += 10) {
    const batch = await p.evaluate(([s, N]) => { const r = []; for (let i = s; i < Math.min(s + 10, N); i++) { render(i); r.push(document.getElementById('c').toDataURL('image/jpeg', 0.92).split(',')[1]); } return r; }, [f, N]);
    for (const d of batch) { if (!ff.stdin.write(Buffer.from(d, 'base64'))) await new Promise(r => ff.stdin.once('drain', r)); }
    if (f % 900 === 0) console.log(`frame ${f}/${N}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
  // captions file for upload (YouTube indexes it for search)
  const ts = s => { const ms = Math.round(s * 1000); const hh = Math.floor(ms / 3600000), mm = Math.floor(ms / 60000) % 60, ss = Math.floor(ms / 1000) % 60; return `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')},${String(ms % 1000).padStart(3, '0')}`; };
  const srt = script.lines.map((l, i) => `${i + 1}\n${ts(tl.lines[i].start)} --> ${ts(tl.lines[i].end)}\n${l.cap || l.say}\n`).join('\n');
  fs.writeFileSync(out.replace(/\.mp4$/, '.srt'), srt);
  console.log('done', out);
})();
