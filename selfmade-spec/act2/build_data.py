import json,os
D=os.path.dirname(os.path.abspath(__file__))
logo=json.load(open(D+'/../logo/logo.json')); ol=json.load(open(D+'/../act1/outline_pts.json'))
open(D+'/data.js','w').write('window.LOGO='+json.dumps(logo)+';\nwindow.OL='+json.dumps(ol)+';\n')
print('ok')
