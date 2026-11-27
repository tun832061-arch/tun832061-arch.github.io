// node thumb.cjs ../ep01  -> ep01/build/thumbnail.png (1280x720)
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto('file://' + path.join(__dirname, 'thumb.html')); await p.evaluate(() => document.fonts.load('400 40px Anton').then(() => document.fonts.load('900 40px Inter')));
  await p.evaluate(e => draw(e), path.basename(path.resolve(process.argv[2]))); await (await p.$('#c')).screenshot({ path: path.join(path.resolve(process.argv[2]), 'build', 'thumbnail.png') }); await b.close(); })();
