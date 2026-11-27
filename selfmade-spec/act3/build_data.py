import json,os
D=os.path.dirname(os.path.abspath(__file__))
logo=json.load(open(D+'/../logo/logo.json'))
cta=[5.15,5.32,5.42,5.55,5.75,6.30,6.42,6.53,6.66,6.85]; dur=[.15,.1,.12,.2,.3,.1,.1,.12,.15,.4]
tim={"_note":"local seconds; t=0 is 30.5s in the full film. Placeholder VO timing.",
 "expand":3.3,"cta0":5.0,"end0":7.6,"cta":cta,"ctaW":[[a,b] for a,b in zip(cta,dur)],"callLen":"00:34"}
open(D+'/data.js','w').write('window.LOGO='+json.dumps(logo)+';\nwindow.TIM3='+json.dumps(tim)+';\n')
print('ok')
