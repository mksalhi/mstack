import sys,json,os,concurrent.futures as cf
sys.path.insert(0,'/home/user/mstack/bench/tasks'); sys.path.insert(0,'/home/user/mstack/bench')
import run
from static import tree_at
tasks=[t for t in json.load(open('/home/user/mstack/bench/tasks/tasks.json')) if t['id'] in ('ambition-estimate','ambition-game','ambition-rewrite','ambition-overnight')]
conds={'old':tree_at('origin/main'),'new':tree_at('HEAD')}
jobs=[(t,c,r) for t in tasks for c in conds for r in range(6)]
def one(j):
    t,c,r=j
    for _ in range(2):
        try:
            text,u,reads=run.run_agent('gpt-6.2-sol',{**t,'skill':'scoper'},conds[c],hook=True)
            return {'task':t['id']+'@scoper','cond':c,'run':r,'text':text,'reads':reads}
        except Exception as e: err=str(e)
    return {'task':t['id'],'cond':c,'error':err}
with cf.ThreadPoolExecutor(12) as ex: rows=list(ex.map(one,jobs))
json.dump(rows,open('/tmp/claude-0/b/scoper-only.json','w'))
print(sum('error' in r for r in rows),'errors')
