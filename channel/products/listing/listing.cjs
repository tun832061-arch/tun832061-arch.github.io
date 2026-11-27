// node listing.cjs -> 01-cover.png ... 05-videos.png (2000x1500)
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 2000, height: 1500 } });
  p.on('pageerror', e => console.log('ERR', e.message)); await p.goto('file://' + path.join(__dirname, 'listing.html'));
  for (const [i, k] of ['cover', 'plan', 'debt', 'funds', 'videos'].entries()) { const d = await p.evaluate(k => draw(k), k); fs.writeFileSync(path.join(__dirname, `0${i + 1}-${k}.png`), Buffer.from(d, 'base64')); }
  await b.close(); console.log('done'); })();
