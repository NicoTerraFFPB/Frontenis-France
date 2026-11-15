import json,glob,os,datetime,sys
# usage: python3 build-export.py <dossier_live> <page_source.html> <sortie/index.html>
S=sys.argv[1].rstrip('/')+'/'
def load(col):
    out=[]
    for f in sorted(glob.glob(S+col+'/*.json')):
        raw=json.load(open(f)); d=dict(raw.get('data',raw)); d['id']=os.path.basename(f)[:-5]; out.append(d)
    return out
players=[{**p,"name":(p.get('first','')+" "+p.get('last','')).strip()} if 'name' not in p else p for p in load('players')]
for p in players: p.pop('birth',None)
idmap={}
entries=[]
for i,e in enumerate(load('entries')):
    e=dict(e); e.pop('by',None); new='e%d'%(i+1); idmap[e['id']]=new; e['id']=new; entries.append(e)
tj=json.dumps(load('tournaments'),ensure_ascii=False)
for old,new in idmap.items(): tj=tj.replace(old,new)
nat=json.load(open(S+'nat/a.json')); nat=nat.get('data',nat)
snap={"at":datetime.date.today().isoformat(),"players":players,"entries":entries,"tournaments":json.loads(tj),"nat":{"teams":nat.get('teams',{}),"days":nat.get('days',[]),"res":nat.get('res',{}),"fin":nat.get('fin',{})}}
cfg={}
for c in load('intlcfg'): cfg[c['id']]=bool(c.get('public'))
snap["intlCfg"]={"seniors":bool(cfg.get('seniors'))}
snap["intl"]=[{k:v for k,v in c.items()} for c in load('intl')] if cfg.get('seniors') else []
src=open(sys.argv[2],encoding='utf-8').read()
blob=json.dumps(snap,ensure_ascii=False).replace("</","<\\/")
page=src.replace('<script type="application/json" id="snap"></script>','<script type="application/json" id="snap">'+blob+'</script>',1)
doc='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>:root{color-scheme:light}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>\n'+page+'\n</body></html>'
open(sys.argv[3],'w',encoding='utf-8').write(doc)
print(len(players),"joueurs,",len(entries),"équipes,",len(snap["tournaments"]),"étapes")
