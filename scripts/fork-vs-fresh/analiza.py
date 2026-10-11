import json,glob,os,statistics as st,random,collections
X=os.path.dirname(os.path.abspath(__file__)); RES=os.environ.get('RES','res')
enc=lambda p:''.join(c if c.isalnum() else '-' for c in p)
PRS={'sonnet':(3,15),'haiku':(1,5),'opus':(5,25)}
def sub_usage(run,sess):
    d=os.path.expanduser(f'~/.claude/projects/{enc(X+"/runs/"+run)}/{sess}/subagents')
    U=collections.Counter();seen=set();tools=0;turns=0;first=None;meta={}
    for f in glob.glob(d+'/*.jsonl'):
        meta=json.load(open(f[:-6]+'.meta.json'))
        for l in open(f):
            dd=json.loads(l)
            if dd.get('type')!='assistant':continue
            m=dd['message'];tools+=sum(c.get('type')=='tool_use' for c in m['content'])
            if m['id'] in seen:continue
            seen.add(m['id']);turns+=1;u=m['usage'];PR=next(v for k,v in PRS.items() if k in m.get('model','sonnet'))
            if first is None:first=u
            for k in('input_tokens','cache_creation_input_tokens','cache_read_input_tokens','output_tokens'):U[k]+=u.get(k,0)
            U['$']+=(u.get('input_tokens',0)*PR[0]+u.get('cache_creation_input_tokens',0)*PR[0]*1.25+u.get('cache_read_input_tokens',0)*PR[0]*.1+u.get('output_tokens',0)*PR[1])
    cost=U['$']/1e6
    f0=(first or {})
    return dict(sub_turns=turns,sub_tools=tools,sub_cw=U['cache_creation_input_tokens'],sub_cr=U['cache_read_input_tokens'],sub_in=U['input_tokens'],sub_out=U['output_tokens'],sub_cost=cost,sub_ctx0=f0.get('input_tokens',0)+f0.get('cache_creation_input_tokens',0)+f0.get('cache_read_input_tokens',0),sub_hit0=f0.get('cache_read_input_tokens',0),n_sub=len(glob.glob(d+'/*.jsonl')),type=meta.get('agentType'))
def brief(run,sess):
    f=os.path.expanduser(f'~/.claude/projects/{enc(X+"/runs/"+run)}/{sess}.jsonl')
    for l in open(f):
        d=json.loads(l)
        if d.get('type')=='assistant':
            for c in d['message']['content']:
                if c.get('type')=='tool_use' and c['name']=='Agent':return c['input'].get('prompt','')
    return ''
rows=[]
for f in sorted(glob.glob(f'{X}/{RES}/*.score.json')):
    run=os.path.basename(f)[:-11];t,c,i=run.split('_')
    try:j=json.load(open(f'{X}/{RES}/{run}.json'))
    except Exception:continue
    sc=json.load(open(f));r=dict(run=run,task=t,cond=c,total=j.get('total_cost_usd',0),parent_out=j['usage']['output_tokens'],dur=j.get('duration_ms',0)/1000,score=sum(sc.values())/len(sc),fails=[k for k,v in sc.items() if not v])
    r.update(sub_usage(run,j['session_id']));b=brief(run,j['session_id']);r['brief_chars']=len(b);r['brief']=b
    rows.append(r)
json.dump(rows,open(f'{X}/{RES}_rows.json','w'),ensure_ascii=False,indent=1)
def perm(a,b,n=20000):
    d=st.mean(a)-st.mean(b);p=a+b;k=0;rnd=random.Random(1)
    for _ in range(n):
        rnd.shuffle(p)
        if abs(st.mean(p[:len(a)])-st.mean(p[len(a):]))>=abs(d)-1e-12:k+=1
    return d,k/n
K=['score','total','sub_cost','sub_turns','sub_tools','sub_ctx0','sub_cr','sub_cw','sub_out','dur','brief_chars']
for t in sorted({r['task'] for r in rows}):
  print(f'== Tarea {t}')
  CS=sorted({r['cond'] for r in rows if r['task']==t})
  for base,other in [(a,b) for a in CS for b in CS if a<b]:
    print(f'-- {base} vs {other}')
    F=[r for r in rows if r['task']==t and r['cond']==base];N=[r for r in rows if r['task']==t and r['cond']==other]
    print(f"   n {base}={len(F)} fresh={len(N)}  tipos={collections.Counter(r['type'] for r in F+N)}")
    for k in K:
        a=[r[k] for r in F];b=[r[k] for r in N]
        if not a or not b:continue
        d,p=perm(a,b)
        print(f"   {k:12} {base[:5]}={st.mean(a):10.3f}  {other[:5]}={st.mean(b):10.3f}  Δ={d:+.3f} p={p:.3f}")
    print('   fallos fork :',collections.Counter(x for r in F for x in r['fails']))
    print('   fallos fresh:',collections.Counter(x for r in N for x in r['fails']))
