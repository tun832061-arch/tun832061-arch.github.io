// node brand.cjs ../brand -> avatar.png (800x800) + banner.png (2560x1440)
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => { const out = path.resolve(process.argv[2]); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2560, height: 1440 } });
  await p.goto('file://' + path.join(__dirname, 'brand.html')); await p.evaluate(() => document.fonts.load('400 40px Anton').then(() => document.fonts.load('800 40px Inter')));
  for (const k of ['avatar', 'banner']) { const d = await p.evaluate(k => { window[k](); return document.getElementById('c').toDataURL('image/png').split(',')[1]; }, k); fs.writeFileSync(path.join(out, k + '.png'), Buffer.from(d, 'base64')); }
  await b.close(); })();
