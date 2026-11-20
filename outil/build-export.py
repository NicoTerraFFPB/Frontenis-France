# usage: python3 build-export.py <dossier_live> <page_source.html> <sortie/index.html> [dossier_sauvegarde]
# usage 2 : python3 build-export.py --entete <index.html>  (remplace seulement l'en-tête d'un index.html déjà construit)
import json,glob,os,datetime,sys,shutil
SITE="https://nicoterraffpb.github.io/Frontenis-France/"
DESC="Tout le Frontenis masculin sénior français dans une app : classements, résultats, plannings et palmarès."
# écrans de démarrage iPhone / iPad (fichiers dans demarrage/, générés à partir de icone.svg)
STARTUP='<link rel="apple-touch-startup-image" media="(device-width: 440px) and (device-height: 956px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)" href="demarrage/demarrage-1320x2868.png"><link rel="apple-touch-startup-image" media="(device-width: 430px) and (device-height: 932px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)" href="demarrage/demarrage-1290x2796.png"><link rel="apple-touch-startup-image" media="(device-width: 428px) and (device-height: 926px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)" href="demarrage/demarrage-1284x2778.png"><link rel="apple-touch-startup-image" media="(device-width: 420px) and (device-height: 912px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)" href="demarrage/demarrage-1260x2736.png"><link rel="apple-touch-startup-image" media="(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)" href="demarrage/demarrage-1242x2688.png"><link rel="apple-touch-startup-image" media="(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-828x1792.png"><link rel="apple-touch-startup-image" media="(device-width: 414px) and (device-height: 736px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)" href="demarrage/demarrage-1242x2208.png"><link rel="apple-touch-startup-image" media="(device-width: 402px) and (device-height: 874px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)" href="demarrage/demarrage-1206x2622.png"><link rel="apple-touch-startup-image" media="(device-width: 393px) and (device-height: 852px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)" href="demarrage/demarrage-1179x2556.png"><link rel="apple-touch-startup-image" media="(device-width: 390px) and (device-height: 844px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)" href="demarrage/demarrage-1170x2532.png"><link rel="apple-touch-startup-image" media="(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)" href="demarrage/demarrage-1125x2436.png"><link rel="apple-touch-startup-image" media="(device-width: 375px) and (device-height: 667px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-750x1334.png"><link rel="apple-touch-startup-image" media="(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-640x1136.png"><link rel="apple-touch-startup-image" media="(device-width: 1032px) and (device-height: 1376px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-2064x2752.png"><link rel="apple-touch-startup-image" media="(device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-2048x2732.png"><link rel="apple-touch-startup-image" media="(device-width: 834px) and (device-height: 1210px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-1668x2420.png"><link rel="apple-touch-startup-image" media="(device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-1668x2388.png"><link rel="apple-touch-startup-image" media="(device-width: 834px) and (device-height: 1112px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-1668x2224.png"><link rel="apple-touch-startup-image" media="(device-width: 820px) and (device-height: 1180px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-1640x2360.png"><link rel="apple-touch-startup-image" media="(device-width: 810px) and (device-height: 1080px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-1620x2160.png"><link rel="apple-touch-startup-image" media="(device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-1536x2048.png"><link rel="apple-touch-startup-image" media="(device-width: 744px) and (device-height: 1133px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)" href="demarrage/demarrage-1488x2266.png">'
# appli installée : barre d'état, zones sûres, et rechargement quand de nouveaux résultats sont publiés
APP_JS=r"""<script>(function(){
var d=document.documentElement,sa=false;try{sa=navigator.standalone===true||matchMedia("(display-mode: standalone)").matches||matchMedia("(display-mode: fullscreen)").matches}catch(e){}
if(sa)d.classList.add("pwa");
var tag=null,busy=false,hidAt=0,pill=null,LIVE=/^#(jour-j|nat-a)/;
function snapAt(t){var m=/"at":\s*"([^"]+)"/.exec(t||"");return m?m[1]:""}
function curAt(){var e=document.getElementById("snap");return e?snapAt(e.textContent.slice(0,200)):""}
function show(){if(pill)return;pill=document.createElement("button");pill.type="button";pill.className="ff-maj";pill.innerHTML='<span></span>Nouveaux résultats · <b>Mettre à jour</b>';pill.onclick=function(){location.reload()};document.body.appendChild(pill)}
function check(auto){
  if(busy||document.hidden||(navigator.onLine===false))return;busy=true;
  fetch(location.pathname,{method:"HEAD",cache:"no-store"}).then(function(r){
    var k=r.headers.get("etag")||r.headers.get("last-modified");
    if(!k||k===tag){busy=false;return}
    var first=tag===null;tag=k;if(first){busy=false;return}
    return fetch(location.pathname,{cache:"no-store"}).then(function(x){return x.text()}).then(function(t){
      busy=false;var i=t.indexOf('id="sn'+'ap">{'),a=i<0?"":snapAt(t.slice(i,i+300)),c=curAt();
      if(!a||!c||a<=c)return;
      if(auto||LIVE.test(location.hash))location.reload();else show();
    });
  }).catch(function(){busy=false});
}
document.addEventListener("visibilitychange",function(){
  if(document.hidden){hidAt=Date.now();return}
  check(hidAt&&Date.now()-hidAt>20000);
});
check(false);setInterval(function(){check(false)},90000);
})();</script>"""
APP_CSS=(":root{padding-top:env(safe-area-inset-top,0px)}"
 ".pwa body::before{background:#0B1628!important}"
 ".pwa,.pwa body{overscroll-behavior-y:none}.pwa body{-webkit-tap-highlight-color:transparent}"
 ".ff-maj{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:95;display:flex;align-items:center;gap:8px;"
 "font:600 15px/1 Barlow,system-ui,sans-serif;color:#fff;background:#12233F;border:1px solid #2C4268;border-radius:999px;padding:12px 18px;box-shadow:0 10px 30px rgba(0,0,0,.35);cursor:pointer;white-space:nowrap}"
 ".ff-maj b{color:#FFEB7A}.ff-maj span{width:9px;height:9px;border-radius:50%;background:#FF5F57;flex:none}"
 "@media (prefers-reduced-motion:no-preference){.ff-maj{animation:ffmaj .5s cubic-bezier(.23,1,.32,1) both}}"
 "@keyframes ffmaj{from{opacity:0;transform:translate(-50%,16px)}}@media print{.ff-maj{display:none}}")
def make_head():
    return ('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
 '<title>Frontenis France</title>'
 '<meta name="description" content="%s">'
 '<meta property="og:type" content="website"><meta property="og:site_name" content="Frontenis France"><meta property="og:locale" content="fr_FR">'
 '<meta property="og:title" content="Frontenis France"><meta property="og:description" content="%s">'
 '<meta property="og:url" content="%s"><meta property="og:image" content="%sog.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
 '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="%sog.png">'
 '<meta name="theme-color" content="#0B1628"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">'
 '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="Frontenis"><meta name="application-name" content="Frontenis">'
 '<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">'
 '<link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="manifest.webmanifest">'
 '%s'
 '<style>:root{color-scheme:light}body{margin:0}img{max-width:100%%}[hidden]{display:none!important}%s</style>%s</head><body>\n')%(DESC,DESC,SITE,SITE,SITE,STARTUP,APP_CSS,APP_JS)
if len(sys.argv)>2 and sys.argv[1]=='--entete':
    f=sys.argv[2];t=open(f,encoding='utf-8').read();i=t.index('<body>\n')+7
    open(f,'w',encoding='utf-8').write(make_head()+t[i:]);print("en-tête remplacé dans",f);sys.exit(0)
from zoneinfo import ZoneInfo
S=sys.argv[1].rstrip('/')+'/'
SRC=sys.argv[2];OUT=sys.argv[3];BK=sys.argv[4] if len(sys.argv)>4 else None
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
head=make_head()
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
