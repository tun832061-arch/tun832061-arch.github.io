const { chromium } = require('playwright'); const { spawn } = require('child_process');
(async () => {
  const [out, audio, mode] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--allow-file-access-from-files', '--disable-web-security'] }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + __dirname + '/edit.html' + (mode === 'raw' ? '#raw' : '')); await p.evaluate(() => window.ready); const N = Math.round((await p.evaluate(() => window.DUR)) * 30);
  const ff = spawn('ffmpeg', ['-v','error','-y','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-i',audio,
    '-af','loudnorm=I=-15:TP=-1.5:LRA=9','-c:v','libx264','-preset','slow','-crf','21','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',out], { stdio: ['pipe','inherit','inherit'] });
  for (let f = 0; f < N; f += 8) {
    const batch = await p.evaluate(async ([s, N]) => { const r = []; for (let i = s; i < Math.min(s + 8, N); i++) { await render(i); r.push(document.getElementById('c').toDataURL('image/jpeg', 0.93).split(',')[1]); } return r; }, [f, N]);
    for (const d of batch) { if (!ff.stdin.write(Buffer.from(d, 'base64'))) await new Promise(r => ff.stdin.once('drain', r)); }
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); console.log('done', out);
})();
