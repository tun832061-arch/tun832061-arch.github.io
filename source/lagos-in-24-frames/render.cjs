const { chromium } = require('playwright'); const { spawn } = require('child_process');
(async () => {
  const [out, audio, hash, secs] = process.argv.slice(2); const sq = hash === 'sq'; const N = Math.round(Number(secs) * 30);
  const ff = spawn('ffmpeg', ['-v','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-i',audio,
    '-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','224k','-movflags','+faststart','-shortest',out], { stdio: ['pipe','inherit','inherit'] });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080 * (sq ? 1 : 16 / 9), height: sq ? 1920 : 1080 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + __dirname + '/lg.html'); await p.evaluate(() => window.ready);
  for (let f = 0; f < N; f += 10) {
    const batch = await p.evaluate(([s, N]) => { const r = []; for (let i = s; i < Math.min(s + 10, N); i++) { render(i); r.push(document.getElementById('c').toDataURL('image/jpeg', 0.95).split(',')[1]); } return r; }, [f, N]);
    for (const d of batch) { if (!ff.stdin.write(Buffer.from(d, 'base64'))) await new Promise(r => ff.stdin.once('drain', r)); }
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('done', out);
})();
