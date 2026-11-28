const {chromium}=require('playwright'); const {spawn}=require('child_process'); const path=require('path');
const args=process.argv.slice(2);
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 const errs=[]; p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+path.resolve(__dirname,'index.html'));
 await p.evaluate(async()=>{init(); for(const t of [0.5,1.5,2.8,5,8,10.5,13,14,16,18,20,23,24.5,26,27.5]){render(t); await new Promise(r=>setTimeout(r,60));} await document.fonts.ready; await new Promise(r=>setTimeout(r,400));});
 if(args[0]==='--stills'){
  for(const t of args[1].split(',').map(Number)){await p.evaluate(t=>render(t),t);await p.screenshot({path:'/tmp/claude-0/-home-user-tun832061-arch-github-io/1d336f03-7800-5438-a46b-f354cd03bd18/scratchpad/am_stills/s_'+t.toFixed(2)+'.png'});}
  if(errs.length)console.error(errs); await b.close(); return;}
 const out=args[0], fps=+(args[1]||24), t0=+(args[2]||0), t1=+(args[3]||28.6);
 const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-c:v','png','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','15','-preset','medium',out],{stdio:['pipe','inherit','inherit']});
 const N=Math.round((t1-t0)*fps);
 for(let i=0;i<N;i++){const t=t0+i/fps; await p.evaluate(t=>render(t),t); const buf=await p.screenshot({type:'png'}); if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));}
 ff.stdin.end(); await new Promise(r=>ff.on('close',r)); if(errs.length)console.error(errs); await b.close(); console.log('done',N);
})();
