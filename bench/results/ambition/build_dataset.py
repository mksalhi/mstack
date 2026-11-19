import json,random,subprocess,os,sys
B='/tmp/claude-0/b'; R='/home/user/mstack'
random.seed(7)
tasks={t['id']:t for t in json.load(open(f'{R}/bench/tasks/tasks.json'))}
hook=json.load(open(f'{B}/hook.json'))['rows']; so=json.load(open(f'{B}/scoper-only.json'))
items=[]
for r in hook: items.append(dict(task=r['task'],cond=r['cond'],text=r['text'],reads=r['reads'],gpt=r['checks']+r['judged'],checks=r['checks'],run=r['run']))
for r in so: items.append(dict(task=r['task'].split('@')[0],cond='scoper-'+r['cond'],text=r['text'],reads=r['reads'],gpt=None,checks=None,run=r['run']))
key=json.load(open(f'{B}/judge-key.json'))
out=[]
for tid in sorted({i['task'] for i in items}):
    its=[i for i in items if i['task']==tid]; random.shuffle(its)
    rat=f'{B}/judge/{tid}.rationale.json'; rat=json.load(open(rat)) if os.path.exists(rat) else {}
    grades=json.load(open(f'{B}/judge/{tid}.out.json'))
    t=tasks[tid]; resp=[]
    for k,i in enumerate(its):
        rid=f'{tid}-{k:02d}'; assert key[rid]==i['cond']
        cl=rat.get(rid) or [{'pass':v,'why':None} for v in grades[rid]]
        resp.append({'id':rid,'cond':i['cond'],'run':i['run'],'files_read':i['reads'],'regex_checks':i['checks'],'gpt_judge':i['gpt'][len(t['checks']):] if i['gpt'] else None,'claude_judge':cl,'answer':i['text']})
    out.append({'id':tid,'skill':t['skill'],'prompt':t['prompt'],'regex_checks':t['checks'],'assertions':t['judge'],'responses':resp})
def show(ref,p): return subprocess.check_output(['git','-C',R,'show',f'{ref}:{p}'],text=True)
meta={'runner':'gpt-6.2-sol (OpenAI Responses API, reasoning effort low)','judge':'Claude (Opus 5.5 subagents), blind: responses shuffled, condition hidden','runs_per_condition':6,
 'system_prompt':"You are a coding agent helping a user in a chat. You cannot run commands or see their repository; everything you need is in the message. Answer the request directly.",
 'conditions':{'none':'No skill, no hook.','old':'Skill at 4ee3b10 (main before this PR) injected after the prompt, plus scoper SKILL.md body in the system prompt (as the SessionStart hook does).','new':'Same, at bf166ae (this PR).','scoper-old':'Only scoper loaded (hook text in system prompt and scoper as the fired skill), at 4ee3b10.','scoper-new':'Same at bf166ae.'},
 'refs':{'old':'4ee3b10','new':'bf166ae'},
 'skill_text':{f'{s}@{ref}':show(ref,f'plugin/skills/{s}/SKILL.md') for s in ('mstack-mode','scoper') for ref in ('4ee3b10','bf166ae')}}
json.dump({'meta':meta,'tasks':out},open(sys.argv[1],'w'),indent=1)
print('ok',sum(len(t['responses']) for t in out))
