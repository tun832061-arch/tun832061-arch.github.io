const { chromium } = require('playwright'); const { spawn } = require('child_process');
(async () => {
  const [out, audio] = process.argv.slice(2); const N = 50 * 30;
  const ff = spawn('ffmpeg', ['-v','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-i',audio,
    '-af','loudnorm=I=-16:TP=-1.5:LRA=14','-c:v','libx264','-preset','slow','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','224k','-movflags','+faststart','-shortest',out], { stdio: ['pipe','inherit','inherit'] });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + __dirname + '/sp.html'); await p.evaluate(() => window.ready);
  const t0 = Date.now();
  for (let f = 0; f < N; f += 10) {
    const batch = await p.evaluate((s) => { const r = []; for (let i = s; i < s + 10; i++) { render(i); r.push(document.getElementById('c').toDataURL('image/jpeg', 0.95).split(',')[1]); } return r; }, f);
    for (const d of batch) { if (!ff.stdin.write(Buffer.from(d, 'base64'))) await new Promise(r => ff.stdin.once('drain', r)); }
    if (f % 300 === 0) console.log(`frame ${f}/${N}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('done', out);
})();
