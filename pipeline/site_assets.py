"""Static CSS and JavaScript for site/index.html. Kept apart from build_site.py so the HTML builder stays readable.
Tokens copied from spec/08 (the Economy Monitor's Frida Kahlo palette)."""

CSS = r"""
:root{
  --wall:#FBFAF6;--panel:#FFFFFF;--line:#E4E1D8;--ink:#1B1D26;--ink-2:#555A6B;--ink-3:#8A8E9C;
  --cobalt:#1F4FA8;--cobalt-deep:#173C82;--cobalt-wash:#EAF0FA;--cochineal:#B5263A;--rosa:#C9357A;
  --leaf:#2F7A52;--ochre:#C27F0A;--marigold:#F0B429;
  --serif:var(--font-anthropic-serif,Georgia,"Times New Roman",serif);
  --sans:var(--font-anthropic-sans,system-ui,-apple-system,"Segoe UI",sans-serif);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
body{margin:0;background:var(--wall);color:var(--ink);font:1rem/1.55 var(--sans)}
a{color:var(--cobalt)}a:hover{color:var(--cobalt-deep)}
:focus-visible{outline:3px solid var(--ochre);outline-offset:2px}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:8px;background:var(--panel);padding:8px;z-index:99}
header.site{padding-top:28px;padding-bottom:8px}
.builtby{font-size:.8125rem;color:var(--ink-2);text-decoration:none;letter-spacing:.02em}
.builtby strong{color:var(--ink)}
h1{font:600 2.4rem/1.15 var(--serif);margin:.4em 0 .2em}
.sub{color:var(--ink-2);margin:0 0 12px;max-width:62ch}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 0}
.pill{font-size:.8125rem;border:1px solid var(--line);background:var(--panel);border-radius:999px;padding:3px 10px;color:var(--ink-2);text-decoration:none}
.pill b{color:var(--ink);font-weight:600}
nav.views{position:sticky;top:0;z-index:20;background:var(--wall);border-bottom:1px solid var(--line);margin-top:18px}
nav.views ul{list-style:none;display:flex;gap:2px;margin:0;padding:0;overflow-x:auto;scrollbar-width:thin}
nav.views a{display:block;padding:10px 12px;font-size:.875rem;color:var(--ink-2);text-decoration:none;white-space:nowrap;border-bottom:2px solid transparent}
nav.views a[aria-current=true],nav.views a:hover{color:var(--ink);border-bottom-color:var(--cobalt)}
section.view{padding:34px 0 10px;scroll-margin-top:48px}
h2{font:600 1.4rem/1.25 var(--serif);margin:0 0 .5em}
h3{font:600 1.05rem/1.3 var(--serif);margin:1.2em 0 .4em}
.lede{font:1.12rem/1.6 var(--serif);max-width:70ch}
.summary p{margin:0 0 .55em}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:22px 0 6px}
.tile{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:14px 14px 12px;text-align:left;font:inherit;color:inherit;cursor:pointer}
.tile[aria-pressed=true]{border-color:var(--cobalt);box-shadow:inset 0 0 0 1px var(--cobalt)}
.tile .k{font-size:.8125rem;color:var(--ink-2);display:block}
.tile .v{font:600 2rem/1.15 var(--sans);font-variant-numeric:tabular-nums;display:block;margin:4px 0}
.tile .n{font-size:.8125rem;color:var(--ink-2);display:block}
.tile.apart{background:transparent;border-style:dashed}
.note{font-size:.8125rem;color:var(--ink-2)}
.analysis{display:inline-block;font-size:.72rem;font-weight:600;letter-spacing:.03em;color:var(--ink-2);background:var(--cobalt-wash);border-radius:3px;padding:0 6px;vertical-align:middle;text-transform:uppercase}
.badge{display:inline-block;font-size:.75rem;border-radius:3px;padding:1px 7px;border:1px solid var(--line);background:var(--panel);color:var(--ink-2);white-space:nowrap}
.badge.t{color:#fff;border-color:transparent}
.b-EQ,.b-EQ-SPV,.b-LP{background:var(--cobalt)}.b-EQ-C{background:#5876B8}.b-BK,.b-GU,.b-RV{background:var(--cochineal)}
.b-LB{background:var(--rosa)}.b-FC{background:var(--cobalt-deep)}.b-PP{background:#8A5A07}.b-LI{background:var(--leaf)}.b-CX{background:var(--ink-2)}
.chip{font:inherit;font-size:.75rem;border:1px solid var(--line);background:var(--cobalt-wash);color:var(--cobalt-deep);border-radius:3px;padding:0 6px;cursor:pointer;text-decoration:none;white-space:nowrap}
.chip:hover{border-color:var(--cobalt)}
.stale{color:var(--cochineal);font-size:.75rem}
/* constellation */
.map-wrap{display:grid;grid-template-columns:1fr 280px;gap:18px;align-items:start}
.map-box{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:8px;position:relative}
#map{width:100%;height:auto;display:block}
#map .ring{fill:none;stroke:var(--line)}
#map .ringlab{font:600 11px var(--sans);fill:var(--ink-3);letter-spacing:.04em;text-transform:uppercase}
#map .node{cursor:pointer}
#map .node circle.dot{fill:var(--panel);stroke:var(--ink-2);stroke-width:1.5}
#map .node.dim{opacity:.18}
#map .node:focus{outline:none}#map .node:focus circle.dot,#map .node.sel circle.dot{stroke:var(--ochre);stroke-width:3}
#map .node.hit circle.dot{stroke:var(--cochineal);stroke-width:3}
#map .node text{font:11.5px var(--sans);paint-order:stroke;stroke:var(--panel);stroke-width:3px;fill:var(--ink);pointer-events:none}
#map .edge{fill:none;stroke-linecap:round}
#map .edge.dim{opacity:.08}
#map .halo{fill:none;stroke-linecap:round;opacity:.18}
#map .core circle{fill:var(--ink);stroke:var(--marigold);stroke-width:3}
#map .core text{fill:#fff;font:600 13px var(--sans)}
#map .loopedge{stroke:var(--ochre);stroke-width:2;fill:none;stroke-dasharray:2 3}
.legend{font-size:.8125rem;color:var(--ink-2)}
.legend ul{list-style:none;padding:0;margin:0 0 10px}
.legend li{display:flex;align-items:center;gap:8px;margin:3px 0}
.legend svg{flex:none}
.controls{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px}
.controls label{font-size:.8125rem;color:var(--ink-2)}
select,input[type=date],input[type=search]{font:inherit;font-size:.875rem;padding:4px 6px;border:1px solid var(--line);border-radius:4px;background:var(--panel);color:var(--ink)}
button.btn{font:inherit;font-size:.875rem;padding:5px 10px;border:1px solid var(--line);border-radius:4px;background:var(--panel);color:var(--ink);cursor:pointer}
button.btn[aria-pressed=true]{background:var(--cobalt);color:#fff;border-color:var(--cobalt)}
.tip{position:absolute;pointer-events:none;background:var(--ink);color:#fff;font-size:.8125rem;padding:6px 8px;border-radius:4px;max-width:260px;z-index:5;display:none}
.ranked{display:none}
.ranked ol{padding-left:1.2em}
@media (max-width:820px){.map-wrap{grid-template-columns:1fr}.tiles{grid-template-columns:repeat(2,1fr)}}
@media (max-width:600px){.map-box{display:none}.ranked{display:block}.full-map-btn{display:inline-block!important}h1{font-size:1.85rem}.tile .v{font-size:1.5rem}}
.full-map-btn{display:none}
body.fullmap .map-box{display:block;position:fixed;inset:0;z-index:60;border-radius:0;overflow:auto}
/* ledger */
.tbl-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:6px;background:var(--panel)}
table{border-collapse:collapse;width:100%;font-size:.8125rem;font-variant-numeric:tabular-nums}
th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{position:sticky;top:0;background:var(--panel);font-weight:600;color:var(--ink-2);white-space:nowrap}
th button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
td.num,th.num{text-align:right}
#ledger td:first-child{min-width:230px}
#ledger td.dt{white-space:nowrap}
tr.row{cursor:pointer}tr.row:hover td{background:#F6F4EE}
tr.row.terminated td{color:var(--ink-3)}
tr.detail>td{padding:0;background:var(--wall)}
tr.detail details>summary{padding:4px 8px;font-size:.75rem;color:var(--ink-2);cursor:pointer}
tfoot td{font-weight:600;border-top:2px solid var(--ink);border-bottom:3px double var(--ink)}
.nc{color:var(--ink-3)}
/* panel */
#panel{position:fixed;top:0;right:0;bottom:0;width:min(640px,100vw);background:var(--panel);border-left:1px solid var(--line);z-index:50;overflow-y:auto;transform:translateX(100%);transition:transform .18s ease-out;padding:18px 20px 40px}
#panel.open{transform:none}
#panel .close{position:sticky;top:0;float:right;font-size:1.2rem;line-height:1;border:1px solid var(--line);background:var(--panel);border-radius:4px;padding:4px 9px;cursor:pointer}
@media (max-width:600px){#panel{width:100vw}}
.pb h3.cp{font:600 1.3rem/1.2 var(--serif);margin:0 0 6px}
.pb .meta{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.pb .insight{font:1.15rem/1.5 var(--serif);margin:10px 0 14px}
.amts{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 12px}
.amt{border:1px solid var(--line);border-radius:4px;padding:6px 8px}
.amt .k{font-size:.72rem;color:var(--ink-2);display:block}
.amt .v{font:600 1rem var(--sans);font-variant-numeric:tabular-nums;display:block}
.amt .d{font-size:.72rem;color:var(--ink-3);display:block}
@media (max-width:600px){.amts{grid-template-columns:repeat(2,1fr)}}
.dates{font-size:.8125rem;color:var(--ink-2);margin:0 0 8px}
.sig{display:flex;align-items:center;gap:8px;font-size:.8125rem;color:var(--ink-2);margin:0 0 12px}
.sig .bar{flex:0 0 140px;height:6px;background:var(--line);border-radius:3px;overflow:hidden}
.sig .bar i{display:block;height:100%;background:var(--cobalt)}
.pb details{border-top:1px solid var(--line);padding:6px 0}
.pb details>summary{cursor:pointer;font-weight:600;font-size:.9rem;padding:4px 0}
.pb details[open]>summary{color:var(--cobalt-deep)}
.pb .xall{float:right;font-size:.75rem}
.pb dl{display:grid;grid-template-columns:max-content 1fr;gap:4px 12px;font-size:.875rem;margin:6px 0}
.pb dt{color:var(--ink-2)}
.pb dd{margin:0}
.pb ul.cons{padding-left:1.1em;margin:6px 0}
.pb ul.cons li{margin:0 0 6px}
.lens{font-size:.72rem;color:var(--ink-2);text-transform:uppercase;letter-spacing:.03em;display:block}
ol.srcs{padding-left:1.2em;font-size:.8125rem}
ol.srcs li{margin:0 0 8px}
ol.srcs q{font-style:italic}
.tier{font-size:.7rem;border-radius:3px;padding:0 5px;margin-right:4px;background:var(--cobalt-wash);color:var(--cobalt-deep);font-weight:600}
cite{font-style:normal}
/* timeline */
#tl{width:100%;height:auto;background:var(--panel);border:1px solid var(--line);border-radius:6px;touch-action:none}
#tl .lane{font:11px var(--sans);fill:var(--ink-2)}
#tl .ev{cursor:pointer}
#tl .brush{fill:var(--cobalt);opacity:.12}
#tl .axis{font:11px var(--sans);fill:var(--ink-3)}
/* loops */
.loops{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}
.loop{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 14px}
.loop h3{margin:0 0 6px}
.loop ol{list-style:none;padding:0;margin:8px 0;font-size:.8125rem}
.loop li{border-left:3px solid var(--line);padding:2px 0 6px 10px;margin-left:4px}
.loop li b{font-weight:600}
.loop li .amtl{font-variant-numeric:tabular-nums;color:var(--ink)}
/* stress */
.scen{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 12px}
.sliders{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px 18px;margin:0 0 12px}
.sliders label{font-size:.8125rem;color:var(--ink-2);display:block}
.sliders input[type=range]{width:100%}
.out{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 14px;font-size:.9rem}
.out .big{font:600 1.5rem var(--sans);font-variant-numeric:tabular-nums}
/* generic */
.cards2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:820px){.cards2{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 14px}
.verdict{font-weight:600}
.v-Supported{color:var(--leaf)}.v-Partly{color:var(--ochre)}.v-Not{color:var(--cochineal)}
ul.changes{list-style:none;padding:0}
ul.changes li{border-bottom:1px solid var(--line);padding:6px 0;font-size:.875rem}
footer{border-top:1px solid var(--line);margin-top:40px;padding:20px 0 40px;font-size:.8125rem;color:var(--ink-2)}
dfn{font-style:normal;border-bottom:1px dotted var(--ink-3);cursor:help}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.pop{position:absolute;z-index:70;max-width:420px;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px 12px;font-size:.8125rem;box-shadow:0 0 0 1px var(--line)}
@media print{
  nav.views,.tiles,#constellation,#timeline,#loops,#stress,.controls,#panel .close,.skip{display:none!important}
  body{background:#fff}
  #panel{position:static;transform:none;width:auto;border:0}
  tr.detail details{display:block}
  .tbl-wrap{border:0}
  th{position:static}
}
"""

JS = r"""
(function(){
'use strict';
const D = JSON.parse(document.getElementById('data').textContent);
const $ = (s,el=document)=>el.querySelector(s), $$=(s,el=document)=>Array.from(el.querySelectorAll(s));
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
function money(v){ if(v==null) return 'Not disclosed'; const a=Math.abs(v); let s,u;
  if(a>=1e12){s=a/1e12;u=' trillion'}else if(a>=1e9){s=a/1e9;u=' billion'}else if(a>=1e6){s=a/1e6;u=' million'}else if(a>=1e3){s=a/1e3;u=' thousand'}else{return (v<0?'-':'')+'$'+a.toFixed(0)}
  let t = s<10? s.toFixed(2): s.toFixed(1); t=t.replace(/\.?0+$/,''); return (v<0?'-':'')+'$'+t+u; }
const ST = {}; // state
function readHash(){ const h=new URLSearchParams(location.hash.slice(1)); return {rel:h.get('rel'),view:h.get('view'),scenario:h.get('scenario'),filter:h.get('filter')}; }
function writeHash(){ const p=new URLSearchParams(); if(ST.rel)p.set('rel',ST.rel); if(ST.view)p.set('view',ST.view); if(ST.scenario)p.set('scenario',ST.scenario); if(ST.filter)p.set('filter',ST.filter);
  const s=p.toString(); history.replaceState(null,'',s?('#'+s):location.pathname+location.search); }
function store(k,v){try{localStorage.setItem('cbai:'+k,JSON.stringify(v))}catch(e){}}
function load(k,d){try{const v=localStorage.getItem('cbai:'+k);return v?JSON.parse(v):d}catch(e){return d}}

/* ---------------- filters shared by tiles, ledger, map, timeline ---------------- */
const F = {cluster:'',type:'',status:'',wwr:'',basis:'',from:'',to:'',tile:''};
function relPass(r){
  if(F.cluster && r.cl!==F.cluster) return false;
  if(F.type && r.t!==F.type) return false;
  if(F.status && r.s!==F.status) return false;
  if(F.wwr && r.w!==F.wwr) return false;
  if(F.basis && r.b!==F.basis) return false;
  const d=r.d||''; if(F.from && d && d<F.from) return false; if(F.to && d && d>F.to) return false;
  if(F.tile){ const x=r.x; if(F.tile==='funded' && !x.funded) return false; if(F.tile==='committed' && !(x.cu||x.csu)) return false;
    if(F.tile==='contingent' && !x.cont) return false; if(F.tile==='headline' && !r.h) return false; }
  return true;
}
function applyFilters(){
  const vis = new Set(D.rels.filter(r=>!r.agg && relPass(r)).map(r=>r.id));
  // ledger
  $$('#ledger tbody tr.row').forEach(tr=>{ const on=vis.has(tr.dataset.id); tr.hidden=!on; const d=tr.nextElementSibling; if(d&&d.classList.contains('detail')) d.hidden=!on; });
  // totals
  let t={funded:0,cu:0,csu:0,cont:0,gross:0,h:0,n:0};
  D.rels.forEach(r=>{ if(r.agg||r.t==='CX'||!vis.has(r.id)) return; t.n++; t.funded+=r.x.funded||0; t.cu+=r.x.cu||0; t.csu+=r.x.csu||0; t.cont+=r.x.cont||0; t.gross+=r.x.gross||0; t.h+=r.h||0; });
  const ft=$('#ledger tfoot'); if(ft){ ft.querySelector('[data-k=n]').textContent=t.n+' relationships';
    ft.querySelector('[data-k=funded]').textContent=money(t.funded); ft.querySelector('[data-k=cu]').textContent=money(t.cu+t.csu);
    ft.querySelector('[data-k=cont]').textContent=money(t.cont); ft.querySelector('[data-k=gross]').textContent=money(t.gross); ft.querySelector('[data-k=h]').textContent=money(t.h); }
  // tiles
  const tv={funded:t.funded,committed:t.cu+t.csu,contingent:t.cont,headline:t.h};
  $$('.tile').forEach(b=>{ const v=b.querySelector('.v'); if(v&&b.dataset.k in tv) v.textContent=money(tv[b.dataset.k]); });
  $('#filtered-note').hidden = !(F.cluster||F.type||F.status||F.wwr||F.basis||F.from||F.to||F.tile);
  // map
  const ents = new Set(D.rels.filter(r=>vis.has(r.id)).map(r=>r.to));
  $$('#map .node').forEach(n=>n.classList.toggle('dim', !ents.has(n.dataset.id)));
  $$('#map .edge,#map .halo').forEach(e=>e.classList.toggle('dim', !ents.has(e.dataset.to)));
  // timeline
  $$('#tl .ev').forEach(c=>{ c.style.opacity = vis.has(c.dataset.rel)?1:.15; });
}
$$('#ledger-filters select').forEach(s=>s.addEventListener('change',()=>{F[s.name]=s.value; applyFilters();}));
$$('.tile').forEach(b=>b.addEventListener('click',()=>{ const k=b.dataset.k; F.tile = F.tile===k?'':k; $$('.tile').forEach(x=>x.setAttribute('aria-pressed', String(F.tile===x.dataset.k)));
  ST.filter=F.tile||null; writeHash(); applyFilters(); }));
const clr=$('#clear-filters'); if(clr) clr.addEventListener('click',()=>{ Object.keys(F).forEach(k=>F[k]=''); $$('#ledger-filters select').forEach(s=>s.value=''); $$('.tile').forEach(x=>x.setAttribute('aria-pressed','false')); clearBrush(); ST.filter=null; writeHash(); applyFilters(); });

/* ---------------- sorting and CSV ---------------- */
$$('#ledger thead th[data-sort] button').forEach(btn=>btn.addEventListener('click',()=>{
  const th=btn.parentElement, key=th.dataset.sort, num=th.classList.contains('num'); const dir = th.getAttribute('aria-sort')==='descending'?'ascending':'descending';
  $$('#ledger thead th').forEach(x=>x.removeAttribute('aria-sort')); th.setAttribute('aria-sort',dir);
  const tb=$('#ledger tbody'); const pairs=$$('tr.row',tb).map(tr=>[tr,tr.nextElementSibling]);
  pairs.sort((a,b)=>{ let x=a[0].dataset[key]||'', y=b[0].dataset[key]||''; if(num){x=parseFloat(x)||0;y=parseFloat(y)||0;} return (x<y?-1:x>y?1:0)*(dir==='ascending'?1:-1); });
  pairs.forEach(([r,d])=>{tb.appendChild(r); if(d) tb.appendChild(d);});
}));
const csvBtn=$('#csv'); if(csvBtn) csvBtn.addEventListener('click',()=>{
  const cols=['id','counterparty','cluster','type','status','source_strength','funded_still_held','committed_confirmed_unpaid','committed_paid_portion_undisclosed','contingent_max','gross_exposure','headline','announced','last_verified','reconciliation','significance','source_url'];
  if(D.showGrades) cols.splice(14,0,'grade');
  const esc=v=>{v=v==null?'':String(v); return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;};
  const rows=[cols.join(',')]; D.rels.filter(r=>!r.agg && relPass(r)).forEach(r=>{ const e=D.ents[r.to]||{};
    const vals=[r.id,e.n,r.cll,r.tl,r.sl,r.bl,r.x.funded,r.x.cu,r.x.csu,r.x.cont,r.x.gross,r.h,r.d,r.lv,r.rc,r.sig,r.src]; if(D.showGrades) vals.splice(14,0,e.g||'');
    rows.push(vals.map(esc).join(',')); });
  const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([rows.join('\n')],{type:'text/csv'})); a.download='nvidia-exposure-register.csv'; a.click(); });

/* ---------------- panel ---------------- */
const panel=$('#panel'), pbody=$('#panel-body'); let lastFocus=null;
function openPanel(id, push=true){
  const src=document.getElementById('p-'+id); if(!src) return;
  lastFocus=document.activeElement; pbody.innerHTML=''; const c=src.cloneNode(true); c.removeAttribute('id'); c.hidden=false; pbody.appendChild(c);
  const sects=load('sections',{}); $$('details[data-sec]',c).forEach(d=>{ if(sects[d.dataset.sec]) d.open=true; d.addEventListener('toggle',()=>{ const s=load('sections',{}); s[d.dataset.sec]=d.open; store('sections',s); }); });
  const xa=$('.xall',c); if(xa) xa.addEventListener('click',e=>{ e.preventDefault(); const open=xa.dataset.mode!=='collapse'; $$('details[data-sec]',c).forEach(d=>d.open=open); xa.dataset.mode=open?'collapse':'expand'; xa.textContent=open?'Collapse all':'Expand all'; });
  bindChips(c);
  panel.hidden=false; requestAnimationFrame(()=>panel.classList.add('open')); panel.setAttribute('aria-hidden','false');
  $('.close',panel).focus(); ST.rel=id; if(push) writeHash(); selectNode(D.relEnt[id]);
}
function closePanel(){ panel.classList.remove('open'); panel.setAttribute('aria-hidden','true'); setTimeout(()=>{panel.hidden=true},reduced?0:200); ST.rel=null; writeHash(); if(lastFocus) lastFocus.focus(); }
$('.close',panel).addEventListener('click',closePanel);
document.addEventListener('keydown',e=>{ if(e.key==='Escape' && panel.classList.contains('open')) closePanel();
  if(e.key==='Tab' && panel.classList.contains('open')){ const f=$$('a,button,summary,[tabindex="0"]',panel).filter(x=>x.offsetParent!==null); if(!f.length) return;
    const first=f[0], last=f[f.length-1]; if(e.shiftKey && document.activeElement===first){e.preventDefault(); last.focus();} else if(!e.shiftKey && document.activeElement===last){e.preventDefault(); first.focus();} } });
$$('#ledger tr.row').forEach(tr=>{ tr.tabIndex=0; tr.addEventListener('click',e=>{ if(e.target.closest('a,button,summary')) return; openPanel(tr.dataset.id); });
  tr.addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); openPanel(tr.dataset.id);} }); });
$$('[data-open]').forEach(a=>a.addEventListener('click',e=>{ e.preventDefault(); openPanel(a.dataset.open); }));

/* citation chips: open the citation list in one click */
let pop=null;
function bindChips(root){ $$('.chip[data-ev]',root).forEach(ch=>ch.addEventListener('click',e=>{ e.preventDefault(); showCites(ch, ch.dataset.ev.split(' ')); })); }
function showCites(anchor, ids){
  if(pop) pop.remove(); pop=document.createElement('div'); pop.className='pop'; pop.setAttribute('role','dialog'); pop.setAttribute('aria-label','Sources');
  const items=ids.map(i=>{ const li=document.getElementById('src-'+i); return li?li.innerHTML:'' }).filter(Boolean);
  pop.innerHTML='<ol class="srcs">'+items.map(x=>'<li>'+x+'</li>').join('')+'</ol><button class="btn" type="button">Close</button>';
  document.body.appendChild(pop); const r=anchor.getBoundingClientRect(); pop.style.top=(scrollY+r.bottom+6)+'px'; pop.style.left=Math.max(8,Math.min(scrollX+r.left, scrollX+innerWidth-440))+'px';
  const b=pop.querySelector('button'); b.addEventListener('click',()=>{pop.remove();pop=null;anchor.focus();}); b.focus();
}
document.addEventListener('click',e=>{ if(pop && !pop.contains(e.target) && !e.target.closest('.chip')){pop.remove();pop=null;} });
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&pop){pop.remove();pop=null;} });
bindChips(document);

/* ---------------- constellation ---------------- */
const svg=$('#map'); const NS='http://www.w3.org/2000/svg';
const TYPE_STYLE={EQ:['var(--cobalt)',''],'EQ-SPV':['var(--cobalt)',''],'EQ-C':['#8FA6D6',''],BK:['var(--cochineal)','6 4'],GU:['var(--cochineal)','6 4'],
  RV:['var(--cochineal)','8 3 2 3'],LB:['var(--rosa)','1 4'],FC:['var(--cobalt-deep)',''],PP:['var(--ochre)',''],LP:['#5876B8','3 2'],LI:['var(--leaf)',''],CX:['var(--ink-3)','']};
function el(n,a,p){ const e=document.createElementNS(NS,n); for(const k in a) e.setAttribute(k,a[k]); if(p) p.appendChild(e); return e; }
const tip=$('#tip');
function drawMap(){
  if(!svg) return; const W=1120,H=1000,cx=W/2,cy=H/2; svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
  const rings=D.rings; const R0=105, outer=Math.min(cx,cy)-60;
  const counts=rings.map((_,i)=>D.nodes.filter(n=>n.ring===i).length); const used=counts.map(c=>c?1:0);
  const radii=[]; let acc=0; const tot=used.reduce((a,b)=>a+b,0)||1; rings.forEach((_,i)=>{ radii[i]=R0+30+(outer-R0-30)*(acc/(tot-1||1)); acc+=used[i]; });
  const gE=el('g',{},svg), gL=el('g',{},svg), gN=el('g',{},svg);
  const maxG=Math.max(1,...D.nodes.map(n=>n.gross||0));
  const pos={};
  rings.forEach((ring,ri)=>{ if(!counts[ri]) return; const r=radii[ri]; el('circle',{class:'ring',cx,cy,r},gL);
    const la=-Math.PI/2-0.03; const lab=el('text',{class:'ringlab',x:cx+r*Math.cos(la)+4,y:cy+r*Math.sin(la)-5,'text-anchor':'end'},gL); lab.textContent=ring.label;
    const ns=D.nodes.filter(n=>n.ring===ri); const off=0.18+ri*0.37;
    ns.forEach((n,i)=>{ const a=(-Math.PI/2)+off+(2*Math.PI*i/Math.max(ns.length,1)); pos[n.id]={x:cx+r*Math.cos(a),y:cy+r*Math.sin(a),ring:ri,idx:i}; }); });
  D.nodes.forEach(n=>{ const p=pos[n.id]; if(!p) return; const [col,dash]=TYPE_STYLE[n.type]||['var(--ink-3)',''];
    const w=n.gross?1.5+9*Math.sqrt(n.gross/maxG):1;
    if(n.headline && n.headline>(n.gross||0)){ const hw=1.5+9*Math.sqrt(Math.min(n.headline,maxG*1.2)/maxG)+6; el('path',{class:'halo',d:`M${cx},${cy} L${p.x},${p.y}`,stroke:col,'stroke-width':hw,'data-to':n.id},gE); }
    el('path',{class:'edge',d:`M${cx},${cy} L${p.x},${p.y}`,stroke:col,'stroke-width':w,'stroke-dasharray':dash,'data-to':n.id},gE); });
  const core=el('g',{class:'core'},gN); el('circle',{cx,cy,r:44},core); const ct=el('text',{x:cx,y:cy+5,'text-anchor':'middle'},core); ct.textContent='Nvidia';
  D.nodes.forEach(n=>{ const p=pos[n.id]; if(!p) return; const r=n.gross?6+16*Math.sqrt(n.gross/maxG):5;
    const g=el('g',{class:'node',tabindex:0,role:'button','data-id':n.id,'aria-label':`${n.name}. ${n.typeLabel}. Gross exposure ${n.gross?(n.lb?'at least ':'')+money(n.gross):'not sized'}. Press Enter to open.`},gN);
    el('circle',{class:'dot',cx:p.x,cy:p.y,r},g);
    if(n.wwr){ el('path',{d:`M${p.x+r*0.7},${p.y-r*0.7} l7,-7 l3,10 z`,fill:'var(--cochineal)'},g); }
    const right=p.x>=cx; const t=el('text',{x:p.x+(right?r+5:-r-5),y:p.y+4,'text-anchor':right?'start':'end'},g); t.textContent=n.name;
    g.addEventListener('click',()=>openPanel(n.rel)); g.addEventListener('keydown',e=>keyNav(e,n,pos));
    g.addEventListener('mouseenter',ev=>showTip(n,p)); g.addEventListener('mouseleave',()=>tip.style.display='none'); g.addEventListener('focus',()=>showTip(n,p)); g.addEventListener('blur',()=>tip.style.display='none');
  });
  ST.pos=pos;
  if(!reduced){ gN.style.opacity=0; gE.style.opacity=0; requestAnimationFrame(()=>{ gN.style.transition=gE.style.transition='opacity .4s ease-out'; gN.style.opacity=1; gE.style.opacity=1; }); }
}
function showTip(n,p){ const b=svg.getBoundingClientRect(), s=b.width/1120; tip.innerHTML=`<b>${n.name}</b><br>${n.typeLabel}<br>Gross exposure: ${n.gross?(n.lb?'at least ':'')+money(n.gross):'not sized'}${n.date?'<br>'+n.date:''}${n.wwr?'<br>Specific wrong-way risk':''}`;
  tip.style.left=(p.x*s+10)+'px'; tip.style.top=(p.y*s+10)+'px'; tip.style.display='block'; }
function keyNav(e,n,pos){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); openPanel(n.rel); return; }
  if(!['ArrowRight','ArrowLeft','ArrowUp','ArrowDown'].includes(e.key)) return; e.preventDefault();
  const p=pos[n.id]; let ring=p.ring, ns=D.nodes.filter(x=>pos[x.id]&&pos[x.id].ring===ring);
  if(e.key==='ArrowUp'||e.key==='ArrowDown'){ ring=Math.max(0,Math.min(D.rings.length-1, ring+(e.key==='ArrowDown'?1:-1))); ns=D.nodes.filter(x=>pos[x.id]&&pos[x.id].ring===ring); if(!ns.length) return; return focusNode(ns[0].id); }
  const i=ns.findIndex(x=>x.id===n.id); const j=(i+(e.key==='ArrowRight'?1:-1)+ns.length)%ns.length; focusNode(ns[j].id); }
function focusNode(id){ const g=$(`#map .node[data-id="${id}"]`); if(g) g.focus(); }
function selectNode(id){ $$('#map .node').forEach(n=>n.classList.toggle('sel', n.dataset.id===id)); }
drawMap();
const loopBtn=$('#show-loops'); if(loopBtn) loopBtn.addEventListener('click',()=>{ const on=loopBtn.getAttribute('aria-pressed')!=='true'; loopBtn.setAttribute('aria-pressed',String(on));
  $$('#map .loopedge').forEach(x=>x.remove()); if(!on) return; const g=svg.querySelector('g'); D.loopEnts.forEach(ids=>{ for(let i=0;i<ids.length-1;i++){ const a=ST.pos[ids[i]], b=ST.pos[ids[i+1]]; if(a&&b) el('path',{class:'loopedge',d:`M${a.x},${a.y} Q560,500 ${b.x},${b.y}`},g);} }); });
const fm=$('#full-map'); if(fm) fm.addEventListener('click',()=>{ document.body.classList.toggle('fullmap'); fm.textContent=document.body.classList.contains('fullmap')?'Close map':'Open the radial map'; });

/* ---------------- timeline with brush ---------------- */
const tl=$('#tl');
function drawTimeline(){ if(!tl) return; const lanes=D.lanes, W=1000, LH=28, top=24, H=top+lanes.length*LH+26; tl.setAttribute('viewBox',`0 0 ${W} ${H}`);
  const t0=Date.parse(D.tlStart), t1=Date.parse(D.tlEnd), L=150, Rr=W-12, xs=t=>L+(Rr-L)*(t-t0)/(t1-t0);
  lanes.forEach((ln,i)=>{ const y=top+i*LH+LH/2; el('line',{x1:L,x2:Rr,y1:y,y2:y,stroke:'var(--line)'},tl); const tx=el('text',{class:'lane',x:L-8,y:y+4,'text-anchor':'end'},tl); tx.textContent=ln.label; });
  for(let y=2023;y<=2027;y++){ const x=xs(Date.parse(y+'-01-01')); if(x<L||x>Rr) continue; el('line',{x1:x,x2:x,y1:top-6,y2:H-20,stroke:'var(--line)','stroke-dasharray':'2 3'},tl); const t=el('text',{class:'axis',x,y:H-6,'text-anchor':'middle'},tl); t.textContent=y; }
  const brush=el('rect',{class:'brush',x:0,y:top-6,width:0,height:lanes.length*LH+6},tl);
  D.events.forEach(ev=>{ const li=lanes.findIndex(l=>l.key===ev.lane); if(li<0) return; const y=top+li*LH+LH/2, x=xs(Date.parse(ev.date));
    const c=el('circle',{class:'ev',cx:x,cy:y,r:5,fill:ev.kind==='termination'||ev.kind==='restructuring'?'var(--cochineal)':'var(--cobalt)','data-rel':ev.rel,tabindex:0,role:'button','aria-label':ev.date+': '+ev.summary},tl);
    const t=el('title',{},c); t.textContent=ev.date+': '+ev.summary; c.addEventListener('click',()=>openPanel(ev.rel)); c.addEventListener('keydown',e=>{if(e.key==='Enter')openPanel(ev.rel)}); });
  let x0=null; const px=e=>{ const b=tl.getBoundingClientRect(); return (e.clientX-b.left)*W/b.width; };
  const toDate=x=>new Date(t0+(t1-t0)*(Math.max(L,Math.min(Rr,x))-L)/(Rr-L)).toISOString().slice(0,10);
  tl.addEventListener('pointerdown',e=>{ if(e.target.classList.contains('ev')) return; x0=px(e); tl.setPointerCapture(e.pointerId); });
  tl.addEventListener('pointermove',e=>{ if(x0==null) return; const x=px(e); brush.setAttribute('x',Math.min(x0,x)); brush.setAttribute('width',Math.abs(x-x0)); });
  tl.addEventListener('pointerup',e=>{ if(x0==null) return; const x=px(e); if(Math.abs(x-x0)<4){ clearBrush(); } else { F.from=toDate(Math.min(x0,x)); F.to=toDate(Math.max(x0,x)); $('#tl-range').textContent=`Showing ${F.from} to ${F.to}.`; } x0=null; applyFilters(); });
  ST.brush=brush;
}
function clearBrush(){ F.from=F.to=''; if(ST.brush){ST.brush.setAttribute('width',0);} const r=$('#tl-range'); if(r) r.textContent=''; }
drawTimeline();
const tf=$('#tl-from'), tt=$('#tl-to'); if(tf) [tf,tt].forEach(i=>i.addEventListener('change',()=>{ F.from=tf.value; F.to=tt.value; applyFilters(); }));

/* ---------------- stress ---------------- */
const SC=D.scen;
function sliderHTML(sid){ const ps=SC.config[sid].parameters; return Object.keys(ps).filter(k=>ps[k].min!==undefined).map(k=>{ const p=ps[k];
  return `<label>${p.label}: <output id="o-${sid}-${k}">${p.value}</output>${p.basis==='illustrative'?' <span class="analysis">Illustrative</span>':''}<input type="range" min="${p.min}" max="${p.max}" step="${p.step}" value="${p.value}" data-k="${k}" aria-label="${p.label}"></label>`; }).join(''); }
function runScenario(sid){
  ST.scenario=sid; writeHash(); $$('.scen button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.s===sid)));
  const box=$('#sliders'); box.innerHTML=sliderHTML(sid);
  if(sid==='S2'){ const labs=Object.keys(SC.S2); const sel=document.createElement('label'); sel.innerHTML='Lab: <select id="lab">'+labs.map(l=>`<option value="${l}">${(D.ents[l]||{}).n||l}</option>`).join('')+'</select>'; box.prepend(sel);
    const def=labs.includes('ent_openai')?'ent_openai':labs[0]; $('#lab').value=def; $('#lab').addEventListener('change',()=>compute(sid)); }
  $$('input[type=range]',box).forEach(i=>i.addEventListener('input',()=>{ $(`#o-${sid}-${i.dataset.k}`).textContent=i.value; compute(sid); }));
  compute(sid);
}
function val(k){ const i=$(`#sliders input[data-k="${k}"]`); return i?parseFloat(i.value):null; }
function compute(sid){
  const out=$('#stress-out'); let html='', affected=[]; const eq=D.fin.equity, fcf=D.fin.fcf;
  const share=(x,d)=>d?(100*x/d).toFixed(2)+'%':'not computable';
  if(sid==='S1'){ const s=SC.S1, h1=val('h1'); const loss=s.equity_losses.reduce((a,e)=>a+e.value*h1,0); const ead=s.equity_losses.reduce((a,e)=>a+e.value,0);
    affected=s.affected; html=`<p class="big">${money(loss)}</p><p>Loss on ${s.equity_losses.length} neocloud equity stakes worth ${money(ead)} after a ${Math.round(h1*100)}% haircut. That is ${share(loss,eq)} of Nvidia's shareholders' equity and ${share(loss,fcf)} of a year's free cash flow.</p>
      <p>No backstop draw is computable: the contracted floors behind Nvidia's capacity backstops are not disclosed. Guaranties of leases sit outside this scenario.</p>`;
    if(s.not_computable.length) html+=`<details><summary>Not computable (${s.not_computable.length})</summary><ul>${s.not_computable.map(x=>`<li>${x.title||x.relationship}: ${x.reason}</li>`).join('')}</ul></details>`; }
  if(sid==='S2'){ const lab=$('#lab').value, s=SC.S2[lab], h2=val('h2'); const loss=s.equity_losses.reduce((a,e)=>a+e.value*h2,0);
    affected=s.affected; html=`<p class="big">${s.equity_losses.length?money(loss):'Not computable'}</p><p>${s.equity_losses.length?`Equity loss on stakes in ${(D.ents[lab]||{}).n} with a confirmed value, after a ${Math.round(h2*100)}% haircut; ${share(loss,eq)} of Nvidia's equity.`:'No stake in this lab has a confirmed value.'}</p>`;
    (s.not_computable||[]).filter(x=>x.relationship).forEach(x=>html+=`<p>${x.title}: ${x.reason}</p>`);
    (s.guaranties_triggered_by_lab_default||[]).forEach(g=>html+=`<p>Guaranty this lab's default would trigger: ${money(g.cap)} cap${g.in_force?'':', not yet in force'}.</p>`);
    s.lapsed_commitments.forEach(c=>html+=`<p>Other Nvidia commitment to this lab: ${c.title}${c.headline?` (headline ${money(c.headline)}, not counted as exposure)`:''}.</p>`);
    const con=s.at_risk_backlog.filter(x=>x.kind==='contract'), les=s.at_risk_backlog.filter(x=>x.kind==='lease');
    if(con.length){ const soft=con.reduce((a,x)=>a+(x.soft_amount||0),0); html+=`<p>Contracts other companies hold with this lab: up to ${money(con.reduce((a,x)=>a+x.amount,0))} across ${con.length}${soft?`, of which ${money(soft)} is stated as up to, cancellable or terminable`:''}. These are what a funding gap would put at risk for them.</p>`; }
    if(les.length) html+=`<p>Lease obligations of this lab: ${money(les.reduce((a,x)=>a+x.amount,0))}.</p>`; }
  if(sid==='S3'){ const s=SC.S3, v=val('v'); const rows=s.facilities.map(f=>{ const after=f.ltv_before/(1+v); const over=f.covenant_ltv?after>f.covenant_ltv:null;
      return `<tr><td>${(D.ents[f.entity]||{}).n||f.entity}</td><td>${f.facility}</td><td class="num">${(f.ltv_before*100).toFixed(0)}%</td><td class="num">${(after*100).toFixed(0)}%</td><td>${f.covenant_ltv?(f.covenant_ltv*100).toFixed(0)+'%':'not sourced'}</td><td>${over==null?'':over?'Over':'Within'}</td></tr>`; }).join('');
    affected=s.affected; html=`<p>Loan to value on GPU-backed facilities after a ${Math.round(-v*100)}% fall in prior generation GPU values. Collateral repricing hits lenders first; Nvidia's loss is indirect and is not estimated.</p>
      ${rows?`<div class="tbl-wrap"><table><thead><tr><th>Borrower</th><th>Facility</th><th class="num">Before</th><th class="num">After</th><th>Covenant</th><th></th></tr></thead><tbody>${rows}</tbody></table></div>`:''}
      <p class="note">${s.not_computable.length} facilities are not computable: each needs both a sourced balance and a sourced collateral value.</p>`; }
  out.innerHTML=html; $$('#map .node').forEach(n=>n.classList.toggle('hit', affected.includes(n.dataset.id)));
}
$$('.scen button').forEach(b=>b.addEventListener('click',()=>runScenario(b.dataset.s)));

/* ---------------- what changed filter ---------------- */
const cf=$('#change-filter'); if(cf) cf.addEventListener('change',()=>{ $$('#changes li').forEach(li=>li.hidden = !!cf.value && li.dataset.type!==cf.value); });

/* ---------------- view nav state ---------------- */
const io=('IntersectionObserver' in window)? new IntersectionObserver(es=>{ es.forEach(e=>{ if(e.isIntersecting){ $$('nav.views a').forEach(a=>a.setAttribute('aria-current',String(a.getAttribute('href')==='#'+e.target.id))); } }); },{rootMargin:'-45% 0px -50% 0px'}):null;
if(io) $$('section.view').forEach(s=>io.observe(s));
$$('nav.views a').forEach(a=>a.addEventListener('click',()=>{ ST.view=a.getAttribute('href').slice(1); setTimeout(writeHash,600); }));

/* ---------------- restore state from the URL ---------------- */
const h=readHash();
if(h.filter){ F.tile=h.filter; $$('.tile').forEach(x=>x.setAttribute('aria-pressed',String(x.dataset.k===h.filter))); }
applyFilters();
if(h.view){ const v=document.getElementById(h.view); if(v) v.scrollIntoView(); ST.view=h.view; }
runScenario(h.scenario && SC[h.scenario] ? h.scenario : 'S1'); if(!h.scenario){ ST.scenario=null; }
if(h.rel) openPanel(h.rel,false);
writeHash();
})();
"""
