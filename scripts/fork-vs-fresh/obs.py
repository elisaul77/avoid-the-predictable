import json,glob,os,collections,statistics as st
# precios $/MTok (in, out); cache write 1.25x, read 0.1x
PR={'opus':(5,25),'sonnet':(3,15),'haiku':(1,5)}
def fam(m):
    for k in PR:
        if k in (m or ''): return k
rows=[]
for f in glob.glob(os.path.expanduser('~/.claude/projects/*/*/subagents/agent-*.jsonl')):
    mf=f[:-6]+'.meta.json'
    meta=json.load(open(mf)) if os.path.exists(mf) else {}
    typ=meta.get('agentType','?')
    seen=set();u=collections.Counter();turns=0;tools=0;first=None;model=None;cost=0
    for l in open(f):
        try:d=json.loads(l)
        except:continue
        if d.get('type')!='assistant':continue
        m=d['message'];mid=m.get('id')
        tools+=sum(1 for c in m.get('content',[]) if c.get('type')=='tool_use')
        if mid in seen:continue
        seen.add(mid);us=m.get('usage',{});model=m.get('model');turns+=1
        ctx=us.get('input_tokens',0)+us.get('cache_creation_input_tokens',0)+us.get('cache_read_input_tokens',0)
        if first is None:first=(ctx,us.get('cache_read_input_tokens',0))
        for k in('input_tokens','cache_creation_input_tokens','cache_read_input_tokens','output_tokens'):u[k]+=us.get(k,0)
        p=PR.get(fam(model))
        if p: cost+=(us.get('input_tokens',0)*p[0]+us.get('cache_creation_input_tokens',0)*p[0]*1.25+us.get('cache_read_input_tokens',0)*p[0]*.1+us.get('output_tokens',0)*p[1])/1e6
    if not turns:continue
    rows.append(dict(typ=typ,model=fam(model),turns=turns,tools=tools,ctx0=first[0],hit0=first[1]/max(first[0],1),cw=u['cache_creation_input_tokens'],cr=u['cache_read_input_tokens'],out=u['output_tokens'],cost=cost,date=os.path.getmtime(f)))
json.dump(rows,open('obs.json','w'))
g=collections.defaultdict(list)
for r in rows:g[r['typ']].append(r)
print(f"{'tipo':18}{'n':>4}{'modelo':>8}{'ctx0':>8}{'hit0':>6}{'turnos':>7}{'cwrite':>9}{'cread':>10}{'out':>7}{'$med':>7}")
for t,v in sorted(g.items(),key=lambda x:-len(x[1])):
    md=lambda k:st.median(r[k] for r in v)
    ms=collections.Counter(r['model'] for r in v).most_common(1)[0][0]
    print(f"{t[:18]:18}{len(v):>4}{ms:>8}{md('ctx0'):>8.0f}{md('hit0'):>6.2f}{md('turns'):>7.0f}{md('cw'):>9.0f}{md('cr'):>10.0f}{md('out'):>7.0f}{md('cost'):>7.3f}")
