import json,os
D=os.path.dirname(os.path.abspath(__file__))
logo=json.load(open(D+'/../logo/logo.json')); ol=json.load(open(D+'/../act1/outline_pts.json'))
env2=json.load(open(D+'/env2.json')) if os.path.exists(D+'/env2.json') else None
open(D+'/data.js','w').write('window.LOGO='+json.dumps(logo)+';\nwindow.OL='+json.dumps(ol)+';\n'+('window.ENV2='+json.dumps(env2)+';\n' if env2 else ''))
print('ok')
