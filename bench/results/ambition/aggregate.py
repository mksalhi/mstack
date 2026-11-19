import json,glob,collections
key=json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'claude-grades/key.json')))
res=collections.defaultdict(lambda: collections.defaultdict(list))
for f in sorted(glob.glob(__import__('os').path.join(__import__('os').path.dirname(__file__),'claude-grades/*.out.json'))):
    tid=f.split('/')[-1][:-len('.out.json')]
    for rid,v in json.load(open(f)).items():
        res[tid][key[rid]].append(sum(v)/len(v))
order=['none','old','new','scoper-old','scoper-new']
print('task | '+' | '.join(order))
tot=collections.defaultdict(list)
for t,d in res.items():
    print(t,' | '.join(f"{100*sum(d[c])/len(d[c]):.0f}% (n={len(d[c])})" if d[c] else '-' for c in order))
    for c in order: tot[c]+=d[c]
print('ALL',' | '.join(f"{100*sum(tot[c])/len(tot[c]):.0f}%" if tot[c] else '-' for c in order))
