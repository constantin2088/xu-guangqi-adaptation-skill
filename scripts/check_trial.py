"""Local deterministic aid; never a factual or model behavior certificate."""
import math
def analyze(p):
 if not isinstance(p.get('unit'),str) or not p['unit'].strip():raise ValueError('explicit unit required')
 def index(rows):
  d={}
  for r in rows:
   v=r['value']
   if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):raise ValueError('finite measurement required')
   if r['id'] in d:raise ValueError('duplicate observation id')
   if not isinstance(r.get('conditions'),str) or not r['conditions'].strip():raise ValueError('conditions required')
   d[r['id']]=r
  return d
 a,b=index(p['baseline']),index(p['trial'])
 if not a or set(a)!=set(b):raise ValueError('same nonempty paired observations required')
 for k in a:
  if a[k]['conditions']!=b[k]['conditions']:raise ValueError('conditions mismatch; compare separately')
 delta={k:b[k]['value']-a[k]['value'] for k in sorted(a)}
 return {'unit':p['unit'],'paired_delta':delta,'mean_delta':sum(delta.values())/len(delta),'note':'Descriptive comparison only; matching labels do not prove controlled conditions or causality.'}

if __name__=='__main__':
 import json,sys
 print(json.dumps(analyze(json.loads(open(sys.argv[1],encoding='utf-8').read())),ensure_ascii=False,indent=2))
