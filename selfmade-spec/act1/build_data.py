import json,os
D=os.path.dirname(os.path.abspath(__file__))
logo=json.load(open(D+'/../logo/logo.json')); tim=json.load(open(D+'/timings.json')); ol=json.load(open(D+'/outline_pts.json'))
env=None
if os.path.exists(D+'/env.json'): env=json.load(open(D+'/env.json'))
open(D+'/data.js','w').write('window.LOGO='+json.dumps(logo)+';\nwindow.TIM='+json.dumps(tim)+';\nwindow.OL='+json.dumps(ol)+';\n'+('window.ENV='+json.dumps(env)+';\n' if env else ''))
print('data.js ok')
