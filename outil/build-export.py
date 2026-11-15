# usage: python3 build-export.py <dossier_live> <page_source.html> <sortie/index.html> [dossier_sauvegarde]
import json,glob,os,datetime,sys,shutil
from zoneinfo import ZoneInfo
S=sys.argv[1].rstrip('/')+'/'
SRC=sys.argv[2];OUT=sys.argv[3];BK=sys.argv[4] if len(sys.argv)>4 else None
SITE="https://nicoterraffpb.github.io/Frontenis-France/"
def load(col):
    out=[]
    for f in sorted(glob.glob(S+col+'/*.json')):
        raw=json.load(open(f,encoding='utf-8')); d=dict(raw.get('data',raw)); d['id']=os.path.basename(f)[:-5]; out.append(d)
    return out
players=[{**p,"name":(p.get('first','')+" "+p.get('last','')).strip()} if 'name' not in p else p for p in load('players')]
for p in players: p.pop('birth',None)
idmap={}
entries=[]
for i,e in enumerate(load('entries')):
    e=dict(e); e.pop('by',None); new='e%d'%(i+1); idmap[e['id']]=new; e['id']=new; entries.append(e)
tj=json.dumps(load('tournaments'),ensure_ascii=False)
for old,new in idmap.items(): tj=tj.replace(old,new)
nat=json.load(open(S+'nat/a.json',encoding='utf-8')); nat=nat.get('data',nat)
now=datetime.datetime.now(ZoneInfo('Europe/Paris')).replace(microsecond=0)
snap={"at":now.isoformat(),"players":players,"entries":entries,"tournaments":json.loads(tj),"nat":{"teams":nat.get('teams',{}),"days":nat.get('days',[]),"res":nat.get('res',{}),"fin":nat.get('fin',{})}}
cfg={}
for c in load('intlcfg'): cfg[c['id']]=bool(c.get('public'))
snap["intlCfg"]={"seniors":bool(cfg.get('seniors'))}
snap["intl"]=[{k:v for k,v in c.items()} for c in load('intl')] if cfg.get('seniors') else []
src=open(SRC,encoding='utf-8').read()
blob=json.dumps(snap,ensure_ascii=False).replace("</","<\\/")
page=src.replace('<script type="application/json" id="snap"></script>','<script type="application/json" id="snap">'+blob+'</script>',1)
head=('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
 '<title>Frontenis France</title>'
 '<meta name="description" content="Tout le Frontenis masculin sénior français dans une app : classements, résultats, plannings et palmarès.">'
 '<meta property="og:type" content="website"><meta property="og:site_name" content="Frontenis France"><meta property="og:locale" content="fr_FR">'
 '<meta property="og:title" content="Frontenis France"><meta property="og:description" content="Tout le Frontenis masculin sénior français dans une app : classements, résultats, plannings et palmarès.">'
 '<meta property="og:url" content="%s"><meta property="og:image" content="%sog.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
 '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="%sog.png">'
 '<meta name="theme-color" content="#0b1f3a"><link rel="icon" type="image/png" href="icon-192.png"><link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="manifest.webmanifest">'
 '<style>:root{color-scheme:light}body{margin:0}img{max-width:100%%}[hidden]{display:none!important}</style></head><body>\n')%(SITE,SITE,SITE)
doc=head+page+'\n</body></html>'
open(OUT,'w',encoding='utf-8').write(doc)
print(len(players),"joueurs,",len(entries),"équipes,",len(snap["tournaments"]),"étapes")
if BK:
    for col in ['tournaments','entries','players','nat','intl','intlcfg']:
        d=os.path.join(BK,col)
        if os.path.isdir(d): shutil.rmtree(d)
        for f in sorted(glob.glob(S+col+'/*.json')):
            raw=json.load(open(f,encoding='utf-8')); data=raw.get('data',raw)
            if col=='entries': data={k:v for k,v in data.items() if k!='by'}
            os.makedirs(d,exist_ok=True)
            json.dump(data,open(os.path.join(d,os.path.basename(f)),'w',encoding='utf-8'),ensure_ascii=False,indent=1,sort_keys=True)
    open(os.path.join(BK,'LISEZMOI.txt'),'w',encoding='utf-8').write("Sauvegarde automatique des données de l'application Frontenis France.\nUn fichier par document (dossier = collection). Les dates de naissance (privées) ne sont volontairement pas sauvegardées ici.\nPour restaurer : demander à Claude de réécrire ces documents dans la base de l'application.\n")
    print("sauvegarde écrite dans",BK)
