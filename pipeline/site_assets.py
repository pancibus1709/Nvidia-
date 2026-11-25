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
html{scroll-behavior:smooth;overflow-x:clip}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important;animation:none!important}}
body{margin:0;background:var(--wall);color:var(--ink);font:1rem/1.55 var(--sans)}
a{color:var(--cobalt)}a:hover{color:var(--cobalt-deep)}
:focus{outline:none}
:focus-visible{outline:3px solid var(--ochre);outline-offset:2px;box-shadow:0 0 0 2px var(--panel)}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:8px;background:var(--panel);padding:8px;z-index:99}
.skip-in{position:absolute;left:-9999px;font-size:.875rem}.skip-in:focus{position:static;display:inline-block;background:var(--panel);padding:8px;margin:0 0 8px}
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
nav.views a{display:block;padding:10px 12px;font-size:.875rem;color:var(--ink-2);text-decoration:none;white-space:nowrap;border-bottom:2px solid transparent;min-height:44px}
nav.views a[aria-current],nav.views a:hover{color:var(--ink);border-bottom-color:var(--cobalt)}
nav.views a:focus-visible{outline-offset:-3px;box-shadow:none}
@media (max-width:820px){nav.views ul{padding-right:48px;-webkit-mask-image:linear-gradient(to right,#000 88%,transparent);mask-image:linear-gradient(to right,#000 88%,transparent)}}
section.view{padding:34px 0 10px;scroll-margin-top:52px}
section.view:focus,section.view:focus-visible{outline:none;box-shadow:none}
h2{font:600 1.4rem/1.25 var(--serif);margin:0 0 .5em}
h3{font:600 1.05rem/1.3 var(--serif);margin:1.2em 0 .4em}
h4{margin:0}
.lede{font:1.12rem/1.6 var(--serif);max-width:70ch}
.view>p,#method>p,#method>dl{max-width:70ch}
/* summary: the three facts first */
.summary{padding-top:18px}
.summary p{margin:0 0 .55em}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:0 0 8px}
.tilew{background:var(--panel);border:1px solid var(--line);border-radius:6px;display:flex;flex-direction:column;min-width:0}
.tilew.apart{background:transparent;border-style:dashed}
.tilew:has(.tile[aria-pressed=true]){border-color:var(--cobalt);border-style:solid}
.tile{display:flex;flex-direction:column;justify-content:flex-start;align-items:flex-start;width:100%;background:none;border:0;border-radius:6px 6px 0 0;padding:12px 14px 4px;text-align:left;font:inherit;color:inherit;cursor:pointer}
.tile[aria-pressed=true]{box-shadow:inset 0 3px 0 var(--cobalt)}
.tile .k{font-size:.8125rem;color:var(--ink-2);display:block;min-height:2.5em;line-height:1.25}
.tile .v{font:500 1.75rem/1.15 var(--sans);font-variant-numeric:tabular-nums;display:block;margin:2px 0 4px;white-space:nowrap}
.u{font-size:.5em;font-weight:500;color:var(--ink-2)}
.tile .n{font-size:.8125rem;color:var(--ink-2);display:block}
.tn{margin:0!important;padding:0 14px 10px;font:.8125rem/1.45 var(--sans);color:var(--ink-2)}
#tile-note{margin:6px 0 14px}
.more>summary{display:none}
@media (min-width:1100px){
  .summary{display:grid;grid-template-columns:minmax(0,62ch) 1fr;gap:4px 32px;align-items:start}
  .summary .lede{grid-column:1;grid-row:1/span 3}
  .summary .tiles{grid-column:2;grid-row:1;grid-template-columns:1fr 1fr}
  .summary #tile-note{grid-column:2;grid-row:2}
  .tile .k{min-height:0}
}
.note{font-size:.8125rem;color:var(--ink-2)}
.blk{display:block}
.analysis{display:inline-block;font:600 .75rem/1.5 var(--sans);letter-spacing:.03em;color:var(--ink-2);background:var(--cobalt-wash);border-radius:3px;padding:0 6px;vertical-align:middle;text-transform:uppercase}
.illus{display:inline-block;font:600 .75rem/1.5 var(--sans);letter-spacing:.03em;color:var(--ink-2);border:1px solid var(--ink-3);border-radius:3px;padding:0 6px;vertical-align:middle;text-transform:uppercase}
.badge{display:inline-block;font-size:.75rem;border-radius:3px;padding:1px 7px;border:1px solid var(--line);background:var(--panel);color:var(--ink-2);white-space:nowrap}
.badge.t{color:#fff;border-color:transparent}
.badge.wwr{color:var(--cochineal);border-color:var(--cochineal)}
.badge.ended{color:var(--ink);border-color:var(--ink-2)}
.b-EQ,.b-EQ-SPV{background:var(--cobalt)}.b-LP,.b-EQ-C{background:#4F6DB0}.b-BK,.b-GU,.b-RV{background:var(--cochineal)}
.b-LB{background:var(--rosa)}.b-FC{background:var(--cobalt-deep)}.b-PP{background:#8A5A07}.b-LI{background:var(--leaf)}.b-CX{background:var(--ink-2)}
.chip{display:inline-block;font:.75rem/1.5 var(--sans);border:1px solid var(--line);background:var(--cobalt-wash);color:var(--cobalt-deep);border-radius:3px;padding:0 6px;cursor:pointer;text-decoration:none;white-space:nowrap;vertical-align:baseline}
.chip:hover{border-color:var(--cobalt)}
.stale{color:var(--cochineal);font-size:.75rem}
/* constellation */
.map-box{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:8px;position:relative;overflow-x:auto}
#map{width:100%;min-width:980px;height:auto;display:block}
#map .ring{fill:none;stroke:var(--line)}
#map .ringlab{font:600 13px var(--sans);fill:var(--ink-2);letter-spacing:.04em;text-transform:uppercase;paint-order:stroke;stroke:var(--panel);stroke-width:5px;stroke-linejoin:round}
#map .node{cursor:pointer}
#map .node circle.dot{fill:var(--panel);stroke:var(--ink-2);stroke-width:1.5}
#map .node .hitc{fill:transparent;stroke:none}
#map .node .fr,#map .node .fr2,#map .node .hr{fill:none;stroke:none;pointer-events:none}
#map .node.dim{opacity:.18}
#map .node:focus{outline:none}
#map .node:focus-visible{opacity:1;box-shadow:none}
#map .node:focus-visible .fr{stroke:var(--ink);stroke-width:2.5}
#map .node:focus-visible .fr2{stroke:var(--ochre);stroke-width:3}
#map .node:focus-visible text{font-weight:700}
#map .node.sel circle.dot{stroke:var(--ochre);stroke-width:3}
#map .node.hit .hr{stroke:var(--cochineal);stroke-width:3}
#map .node text{font:14px var(--sans);paint-order:stroke;stroke:var(--panel);stroke-width:3px;stroke-linejoin:round;fill:var(--ink)}
#map .edge path{fill:none;stroke-linecap:round}
#map .edge.dim{opacity:.08}
#map .halo{fill:none;stroke-linecap:round;opacity:.18}
#map .halo.dim{opacity:.03}
#map .core circle{fill:var(--ink);stroke:var(--marigold);stroke-width:3}
#map .core .c2{fill:none;stroke:var(--marigold);stroke-width:1.5}
#map .core text{fill:#fff;font:600 15px var(--sans)}
#map .loopedge{stroke:var(--ochre);stroke-width:2;fill:none;stroke-dasharray:2 3}
#map .sat{pointer-events:none}
#map .sat line{stroke:var(--ink-2);stroke-width:1}
#map .sat circle{fill:var(--panel);stroke:var(--ink-2);stroke-width:1.3}
#map .sat text{font:12.5px var(--sans);fill:var(--ink-2);paint-order:stroke;stroke:var(--panel);stroke-width:4px;stroke-linejoin:round}
.legend{font-size:.8125rem;color:var(--ink-2);margin-top:12px}
.legend p{max-width:none;margin:0 0 8px}
.legend ul{list-style:none;padding:0;margin:0 0 10px;columns:3 250px;column-gap:24px}
.legend li{display:flex;align-items:center;gap:8px;margin:0 0 5px;break-inside:avoid}
.legend svg{flex:none}
.controls{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px;align-items:end}
.controls label{font-size:.8125rem;color:var(--ink-2)}
select,input[type=date],input[type=search]{font:inherit;font-size:.875rem;padding:4px 6px;border:1px solid var(--ink-3);border-radius:4px;background:var(--panel);color:var(--ink)}
button.btn{font:inherit;font-size:.875rem;padding:5px 10px;border:1px solid var(--ink-3);border-radius:4px;background:var(--panel);color:var(--ink);cursor:pointer}
button.btn.sm{font-size:.75rem;padding:2px 8px;margin-left:6px}
button.btn[aria-pressed=true]{background:var(--cobalt);color:#fff;border-color:var(--cobalt)}
.tip{position:absolute;pointer-events:none;background:var(--ink);color:#fff;font-size:.8125rem;padding:6px 8px;border-radius:4px;max-width:260px;z-index:5;display:none}
.ranked{display:none;margin-top:14px}
body.show-list .ranked{display:block}
.ranked ol{list-style:none;padding:0;margin:0}
.ranked li{border-bottom:1px solid var(--line);font-size:.9375rem}
.ranked li a{display:block;padding:6px 0;color:var(--ink);text-decoration:none}
.ranked li a b{color:var(--cobalt);text-decoration:underline;text-underline-offset:3px;font-weight:600}
.full-map-btn,.map-close{display:none}
@media (max-width:820px){.tiles{grid-template-columns:repeat(2,1fr)}}
@media (max-width:600px){
  .map-box{display:none}.ranked{display:block}.full-map-btn{display:inline-block}#view-list,#constellation .skip-in{display:none}
  body:not(.filtered) .tnote{display:none}
  h1{font-size:1.85rem}.tile .v{font-size:1.4rem}.tile .k{min-height:2.5em}.tn{padding:0 10px 8px}.tile{padding:10px 10px 2px}
  .more>summary{display:list-item;font:600 .875rem var(--sans);color:var(--cobalt);cursor:pointer;padding:10px 0}
  body.panel-open{overflow:hidden}
}
body.fullmap{overflow:hidden}
body.fullmap .map-box{display:block;position:fixed;inset:0;z-index:60;border-radius:0;border:0;overflow:auto;padding:60px 8px 8px}
body.fullmap #map{width:1300px;min-width:1300px;max-width:none}
body.fullmap .map-close{display:inline-flex;align-items:center;justify-content:center;position:fixed;top:8px;right:8px;z-index:61;min-width:44px;min-height:44px}
/* ledger */
.tbl-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:6px;background:var(--panel)}
.ledger-wrap{max-height:80vh;overflow:auto}
.ledger-wrap.more-right{border-right:3px solid var(--ink-3)}
table{border-collapse:collapse;width:100%;font-size:.8125rem;font-variant-numeric:tabular-nums}
#ledger{border-collapse:separate;border-spacing:0}
th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
thead th{background:var(--panel);font-weight:600;color:var(--ink-2);white-space:nowrap}
tbody th,tfoot th{font-weight:600}
#ledger thead th{position:sticky;top:0;z-index:2;vertical-align:bottom;white-space:normal}
#ledger tbody th,#ledger tfoot th,#ledger thead th:first-child{position:sticky;left:0;background:var(--panel);z-index:1;min-width:164px;max-width:200px;box-shadow:inset -1px 0 0 var(--line)}
#ledger thead th:first-child{z-index:3}
#ledger td,#ledger th{padding:6px 5px}
#ledger .badge{white-space:normal}
th button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
.pth{display:none}
th[data-sort] button::after{content:" \2195";color:var(--ink-3)}
th[aria-sort=ascending] button::after{content:" \25B2";color:var(--ink)}
th[aria-sort=descending] button::after{content:" \25BC";color:var(--ink)}
td.num,th.num{text-align:right}
td.dt{white-space:nowrap}
.rowbtn{font:inherit;font-weight:600;color:var(--ink);background:none;border:0;padding:0;text-align:left;cursor:pointer;text-decoration:underline;text-decoration-color:var(--ink-3);text-decoration-thickness:1px;text-underline-offset:3px}
.rowbtn:hover{color:var(--cobalt)}
.disc{font:inherit;font-size:.75rem;line-height:1;margin-left:6px;border:1px solid var(--line);border-radius:3px;background:var(--panel);color:var(--ink-2);width:22px;height:22px;padding:0;cursor:pointer;vertical-align:middle}
.disc[aria-expanded=true]{background:var(--cobalt-wash);border-color:var(--cobalt)}
.rt{display:block;font-weight:400}
.ns{color:inherit;cursor:pointer;text-decoration:underline;text-decoration-color:var(--cobalt);text-decoration-thickness:1px;text-underline-offset:3px;white-space:nowrap}
.ns:hover{color:var(--cobalt)}
.lb{display:block;font-size:.75rem;color:var(--ink-2)}
tr.row{cursor:pointer}tr.row:hover td,tr.row:hover th{background:#F6F4EE}
tr.row.terminated td,tr.row.terminated th,tr.row.terminated .rowbtn{color:var(--ink-2)}
tr.row.terminated td.num .ns{text-decoration:line-through}
tr.detail>td{padding:0;background:var(--wall)}
tr.detail details>summary{padding:4px 8px;font-size:.75rem;color:var(--ink-2);cursor:pointer}
html.js tr.detail{display:none}
html.js tr.detail.show{display:table-row}
html.js tr.detail.show>td>details>summary{display:none}
tr.detail .pb{padding:12px 14px;max-width:900px}
tfoot td,tfoot th{font-weight:600;border-top:2px solid var(--ink);border-bottom:3px double var(--ink)}
.nc{color:var(--ink-2)}
.nd{font-style:italic}
/* panel */
#scrim{position:fixed;inset:0;background:rgba(27,29,38,.25);z-index:75}
#panel{position:fixed;top:0;right:0;bottom:0;width:min(640px,100vw);background:var(--panel);border-left:1px solid var(--line);z-index:80;overflow-y:auto;transform:translateX(100%);transition:transform .18s ease-out;padding:14px 20px 40px}
#panel.open{transform:none}
#panel .close{position:sticky;top:0;float:right;min-width:44px;min-height:44px;font-size:1.3rem;line-height:1;border:1px solid var(--ink-3);background:var(--panel);border-radius:4px;cursor:pointer;z-index:2;margin-left:8px}
@media (max-width:600px){#panel{width:100vw;padding:12px 14px 40px}}
.pb .cp{font:600 1.3rem/1.2 var(--serif);margin:0 0 6px}
.pb .meta{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.pb .insight{font:1.15rem/1.5 var(--serif);margin:10px 0 14px}
.amts{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:0 0 8px}
.amts.extra{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.amt{border:1px solid var(--line);border-radius:4px;padding:6px 8px;min-width:0}
.amt .k{font-size:.75rem;color:var(--ink-2);display:block}
.amt .v{font:600 1rem var(--sans);font-variant-numeric:tabular-nums;display:block}
.amt .v.nc{color:var(--ink-2);font-weight:500}
.amt .d{font-size:.75rem;color:var(--ink-2);display:block}
@media (max-width:600px){.amts{grid-template-columns:repeat(2,1fr)}}
.dates{font-size:.8125rem;color:var(--ink-2);margin:4px 0 8px}
.sig{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:.8125rem;color:var(--ink-2);margin:0 0 12px}
.sig span{white-space:nowrap}
.sig .bar{flex:1 1 100px;max-width:140px;height:6px;background:var(--line);border-radius:3px;overflow:hidden}
.sig .bar i{display:block;height:100%;background:var(--cobalt)}
.pb details{border-top:1px solid var(--line);padding:6px 0}
.pb details>summary{cursor:pointer;font-weight:600;font-size:.9rem;padding:4px 0}
.pb details[open]>summary{color:var(--cobalt-deep)}
.pb details>p,.pb details>ul,.pb details>dl{max-width:70ch}
.pb .xall{float:right;margin:4px 0 0 8px;font-size:.75rem;padding:6px 8px}
.pb dl{display:grid;grid-template-columns:max-content 1fr;gap:4px 12px;font-size:.875rem;margin:6px 0}
.pb dl.defs{grid-template-columns:minmax(120px,max-content) 1fr}
.pb dt{color:var(--ink-2)}
.pb dd{margin:0}
@media (max-width:600px){.pb dl,.pb dl.defs{grid-template-columns:1fr;gap:0 0}.pb dd{margin:0 0 8px}}
.pb ul.cons{padding-left:1.1em;margin:6px 0}
.pb ul.cons li{margin:0 0 6px}
.loop p,.card p,.card li,.pb details p,.pb ul.cons li{font-size:.9375rem;line-height:1.5}
.lens{font-size:.75rem;color:var(--ink-2);text-transform:uppercase;letter-spacing:.03em;display:block}
ol.srcs{padding-left:1.2em;font-size:.8125rem}
ol.srcs li{margin:0 0 8px;overflow-wrap:anywhere}
ol.srcs q{font-style:italic}
.tier{font-size:.75rem;border-radius:3px;padding:0 5px;margin-right:4px;background:var(--cobalt-wash);color:var(--cobalt-deep);font-weight:600}
cite{font-style:normal}
/* timeline */
.tl-box{overflow-x:auto;background:var(--panel);border:1px solid var(--line);border-radius:6px}
#tl{display:block;width:100%;min-width:720px;touch-action:pan-y;user-select:none;-webkit-user-select:none}
#tl .lane{font:12px var(--sans);fill:var(--ink-2)}
#tl .ev{cursor:pointer}
#tl .ev .hitc{fill:transparent}
#tl .ev:focus-visible{outline:none;box-shadow:none}
#tl .ev:focus-visible .hitc{stroke:var(--ink);stroke-width:2.5;fill:rgba(194,127,10,.25)}
#tl .ev.off>:not(.hitc):not(title){fill:var(--panel);stroke:var(--ink-3);stroke-width:1;opacity:.7}
#tl .brush{fill:var(--cobalt);opacity:.12}
#tl .axis{font:12px var(--sans);fill:var(--ink-2)}
.tl-legend svg{vertical-align:-2px;margin-left:8px}
.tl-list{margin-top:10px}
.tl-list>summary{cursor:pointer;font-weight:600;font-size:.875rem;color:var(--cobalt);padding:6px 0}
.tl-list ol{list-style:none;padding:0;margin:0}
.tl-list li{border-bottom:1px solid var(--line);padding:6px 0;font-size:.875rem;max-width:80ch}
@media (max-width:600px){.tl-box,.tl-legend,.tl-help,#timeline .skip-in{display:none}}
/* loops */
.loops{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(320px,100%),1fr));gap:14px}
.loop{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 14px;min-width:0}
.loop h3{margin:0 0 6px}
.loop ol{list-style:none;padding:0;margin:8px 0;font-size:.8125rem;counter-reset:leg}
.loop li{border-left:3px solid var(--ink-3);padding:2px 0 6px 10px;margin:0 0 6px 4px;counter-increment:leg}
.loop li::before{content:counter(leg) ". ";font-weight:600;color:var(--ink-2)}
.loop li.leg-out{border-left-color:var(--cobalt)}.loop li.leg-back{border-left-color:var(--ochre)}.loop li.leg-rent{border-left-color:var(--rosa)}
.loop li b{font-weight:600}
.loop .dir{font-weight:600;font-size:.75rem;text-transform:uppercase;letter-spacing:.03em;color:var(--ink-2)}
.loop .amtl{display:block;text-align:right;font-weight:600;font-variant-numeric:tabular-nums;color:var(--ink);margin-top:2px}
.loop .amtl .al,.loop .amtl.none{font-weight:400;color:var(--ink-2)}
.loopsvg{display:block;width:100%;max-width:380px;height:auto;margin:8px 0}
.loopsvg text{font:12px var(--sans)}
.loopsvg .lc{fill:#fff;font-weight:600}.loopsvg .le{fill:var(--ink)}.loopsvg .ln{font:600 11px var(--sans);fill:var(--ink)}
/* stress */
.scen{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 12px}
.sliders{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px 18px;margin:0 0 12px}
.sliders label{font-size:.8125rem;color:var(--ink-2);display:block}
.sliders output{color:var(--ink);font-weight:600;font-variant-numeric:tabular-nums}
.sliders input[type=range]{width:100%;accent-color:var(--cobalt)}
.sliders .cap{display:block;font-size:.75rem}
.out{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 14px;font-size:.9rem}
.out .k{font-size:.8125rem;color:var(--ink-2);margin:0}
.out .big{font:600 1.5rem var(--sans);font-variant-numeric:tabular-nums;margin:0 0 6px}
.out .big .chip{font-weight:400}
/* generic */
.cards2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media (max-width:820px){.cards2{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 14px}
.verdict{font-weight:600;color:var(--ink)}
.vm{display:inline-block;width:10px;height:10px;margin-right:7px;background:var(--ink-2)}
.v-Supported{color:var(--leaf)}.v-Supported .vm{background:var(--leaf);border-radius:50%}
.v-Partly .vm{background:var(--ochre)}
.v-Not{color:var(--cochineal)}.v-Not .vm{background:var(--cochineal);transform:rotate(45deg)}
.v-Nottest{color:var(--ink-2)}.v-Nottest .vm{background:none;border:2px solid var(--ink-2)}
ul.changes{list-style:none;padding:0}
ul.changes li{border-bottom:1px solid var(--line);padding:6px 0;font-size:.875rem;overflow-wrap:anywhere}
ul.changes a:not(.chip){text-decoration-thickness:1px;text-underline-offset:3px}
ul.changes.sub{margin:4px 0 0 12px}
ul.changes details>summary{cursor:pointer;color:var(--cobalt);font-weight:600;padding:4px 0}
ul.plain{list-style:none;padding:0;margin:0}ul.plain li{margin:0 0 4px}
details.inl>summary{cursor:pointer}
details.inl>p{margin:4px 0}
footer{border-top:1px solid var(--line);margin-top:40px;padding:20px 0 40px;font-size:.8125rem;color:var(--ink-2)}
dfn{font-style:normal;font-weight:600}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.pop{position:absolute;z-index:90;max-width:calc(100vw - 16px);max-height:70vh;overflow:auto;background:var(--panel);border:1px solid var(--ink-3);border-radius:6px;padding:10px 12px;font-size:.8125rem;box-shadow:0 0 0 1px var(--line)}
.pop .pclose{float:right;margin:0 0 6px 8px}
.pop .ph{margin:0 0 8px;font-size:.875rem}
.pop ol.rows{list-style:none;padding:0;margin:0;clear:both}
.pop ol.rows li{border-top:1px solid var(--line);padding:6px 0}
.pop .pv{float:right;font-weight:600;font-variant-numeric:tabular-nums;margin-left:8px}
.pop .ps{display:block;margin-top:2px}
.pop ol.srcs{clear:both}
@media (max-width:600px){
  #ledger tbody th,#ledger tfoot th,#ledger thead th:first-child{min-width:150px;max-width:170px}
  #ledger .rt{display:none}
  html.js table.stack thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
  html.js table.stack,html.js table.stack tbody{display:block}
  html.js table.stack tr{display:block;border-bottom:2px solid var(--line);padding:6px 0}
  html.js table.stack td,html.js table.stack tbody th{display:block;border:0;padding:3px 10px;text-align:left}
  html.js table.stack tbody th{font-size:.9375rem}
  html.js table.stack td[data-label]::before{content:attr(data-label);display:block;font-size:.75rem;color:var(--ink-2);font-weight:600}
  html.js table.stack td:empty{display:none}
}
@media (pointer:coarse){
  .chip{padding:12px 10px;font-size:.8125rem;margin:2px 0;vertical-align:middle}
  .ranked li a{padding:12px 0}
  button.btn,select,input[type=date]{min-height:44px}
  button.btn.sm{min-height:44px;padding:8px 12px}
  .pb details>summary,.tl-list>summary,ul.changes details>summary,details.inl>summary,.more>summary{padding:12px 0;min-height:44px}
  input[type=range]{height:44px}
  th button{padding:12px 0;min-height:44px}
  .rowbtn{padding:10px 0;min-height:44px}
  .disc{width:44px;height:44px}
  .ns{display:inline-block;padding:10px 0;min-height:44px}
  .tl-list li a{display:block;padding:10px 0 2px}
  .pb .xall{min-height:44px}
  a.pill{padding:11px 12px}
  ol.srcs li a,.pop .ps a,ul.changes li a:not(.chip),.sig a,.builtby{display:inline-block;padding:10px 0}
}
@media print{
  @page{size:A4 landscape;margin:12mm}
  *{print-color-adjust:exact;-webkit-print-color-adjust:exact}
  html,body{background:#fff}
  nav.views,.skip,.skip-in,.controls,#constellation,#timeline,#loops,#stress,#others,#verdict,#changes-view,#method,#scrim,.pop,.noprint,.chip,.xall,#panel .close,.disc,.scroll-hint,#filtered-note,#clear-filters-2,.more>summary,footer .builtby{display:none!important}
  .wrap{max-width:none;padding:0}
  header.site{padding-top:0}
  h1{font-size:20pt}
  .summary{display:block}
  .tiles{grid-template-columns:repeat(4,1fr)!important}
  .lede{font-size:11pt;max-width:none}
  section.view{padding:10px 0 0}
  .tbl-wrap,.ledger-wrap{overflow:visible!important;max-height:none!important;border:0!important}
  table{font-size:8.5pt}
  #ledger{border-collapse:collapse}
  #ledger thead th,#ledger thead th:first-child,#ledger tbody th,#ledger tfoot th{position:static;min-width:0;max-width:none;box-shadow:none}
  #ledger-view{break-before:page}
  .pb details>p,.pb details>ul,.pb details>dl{max-width:none}
  #ledger td,#ledger th{padding:3px 4px}
  th[data-sort] button{display:none}
  .pth{display:inline}
  #ledger tbody th{width:27%}
  table.sub tbody th{width:72%}
  thead{display:table-header-group}
  tfoot{display:table-row-group}
  tr.row{break-inside:avoid}
  tr.detail{display:none!important}
  .ns,.rowbtn{text-decoration:none!important;color:inherit}
  tr.row.terminated td.num .ns{text-decoration:line-through!important}
  #panel{position:static;transform:none;width:auto;border:0;padding:0;overflow:visible;break-after:page}
  #panel .pb{max-width:none}
  #panel details{break-inside:auto}
  #panel details>summary{list-style:none;font-size:11pt}
  body.panel-open [inert]{opacity:1}
  footer{margin-top:10px;padding:8px 0}
}
@media print{#panel details::details-content{content-visibility:visible!important;display:block!important;height:auto!important}}
"""

JS = r"""
(function(){
'use strict';
const D = JSON.parse(document.getElementById('data').textContent);
const $ = (s,el=document)=>el.querySelector(s), $$=(s,el=document)=>Array.from(el.querySelectorAll(s));
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const phone = matchMedia('(max-width:600px)');
const MON=['January','February','March','April','May','June','July','August','September','October','November','December'];
function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function money(v){ if(v==null) return 'Not disclosed'; const a=Math.abs(v); let s,u;
  if(a>=1e12){s=a/1e12;u=' trillion'}else if(a>=1e9){s=a/1e9;u=' billion'}else if(a>=1e6){s=a/1e6;u=' million'}else if(a>=1e3){s=a/1e3;u=' thousand'}else{return (v<0?'-':'')+'$'+a.toFixed(0)}
  let t = s<10? s.toFixed(2): s.toFixed(1); if(t.indexOf('.')>=0) t=t.replace(/0+$/,'').replace(/\.$/,''); return (v<0?'-':'')+'$'+t+u; }
function moneyS(v){ return money(v).replace(' trillion','T').replace(' billion','B').replace(' million','M').replace(' thousand','K'); }
function moneyU(v){ const t=money(v), i=t.lastIndexOf(' '); return i>0? esc(t.slice(0,i))+' <span class="u">'+esc(t.slice(i+1))+'</span>' : esc(t); }
function dateLong(d){ if(!d) return ''; const p=d.split('-'); return parseInt(p[2],10)+' '+MON[parseInt(p[1],10)-1]+' '+p[0]; }
function clean(s){ return esc(String(s||'').replace(/\s*\((?:ev_\d+(?:,\s*|\s+and\s+)?)+\)/g,'').replace(/\s*\bev_\d+\b/g,'').replace(/\b\d{4}-\d\d-\d\d\b/g,m=>dateLong(m)).replace(/\b[a-z]+(?:_[a-z0-9]+)+\b/g,m=>m.replace(/_/g,' '))); }
function plural(n,w){ return n+' '+w+(n===1?'':'s'); }
function go(id,instant){ const v=document.getElementById(id); if(v) v.scrollIntoView({behavior:(instant||reduced)?'instant':'smooth',block:'start'}); return v; }
const REL={}; D.rels.forEach(r=>REL[r.id]=r);
const CORE=D.rels.filter(r=>!r.agg && r.t!=='CX');
const entName=id=>(D.ents[id]||{}).n||id;
const ST = {rel:null,view:null,scenario:null,hl:false,lab:null,stakes:[]};
function store(k,v){try{localStorage.setItem('cbai:'+k,JSON.stringify(v))}catch(e){}}
function load(k,d){try{const v=localStorage.getItem('cbai:'+k);return v?JSON.parse(v):d}catch(e){return d}}

/* ---------------- shareable state in the URL ---------------- */
const F = {cluster:'',type:'',status:'',wwr:'',basis:'',from:'',to:'',tile:''};
const HK=['cluster','type','status','wwr','basis','from','to'];
const TILES=['funded','committed','contingent','headline'];
function readHash(){ const h=new URLSearchParams(location.hash.slice(1)); const o={}; ['rel','view','scenario','filter','lab','p'].concat(HK).forEach(k=>o[k]=h.get(k)||''); o.scenario=o.scenario.toUpperCase(); return o; }
function sliderState(){ const out=[]; $$('#sliders input[type=range]:not([disabled])').forEach(i=>{ if(i.value!==i.defaultValue) out.push(i.dataset.k+':'+i.value); }); return out.join(','); }
function writeHash(){ const p=[]; const add=(k,v)=>p.push(k+'='+encodeURIComponent(v).replace(/%3A/g,':').replace(/%2C/g,','));
  if(ST.rel) add('rel',ST.rel); if(ST.view) add('view',ST.view);
  if(ST.scenario){ add('scenario',ST.scenario); if(ST.scenario==='S2'&&ST.lab) add('lab',ST.lab); const sv=sliderState(); if(sv) add('p',sv); }
  if(F.tile) add('filter',F.tile); HK.forEach(k=>{ if(F[k]) add(k,F[k]); });
  const s=p.join('&'); try{ history.replaceState(history.state,'',s?('#'+s):location.pathname+location.search); }catch(e){} }

/* ---------------- filters shared by tiles, ledger, map, timeline ---------------- */
let VIS=new Set(CORE.map(r=>r.id));
function anyFilter(){ return !!(F.cluster||F.type||F.status||F.wwr||F.basis||F.from||F.to||F.tile); }
function relPass(r,noDate){
  if(F.cluster && r.cl!==F.cluster) return false;
  if(F.type && r.t!==F.type) return false;
  if(F.status && r.s!==F.status) return false;
  if(F.wwr && r.w!==F.wwr) return false;
  if(F.basis && r.b!==F.basis) return false;
  if(!noDate && (F.from||F.to)){ if(!r.d) return false; if(F.from && r.d<F.from) return false; if(F.to && r.d>F.to) return false; }
  if(F.tile){ const x=r.x; if(F.tile==='funded' && !x.funded) return false; if(F.tile==='committed' && !(x.cu||x.csu)) return false;
    if(F.tile==='contingent' && !x.cont) return false; if(F.tile==='headline' && !r.h) return false; }
  return true;
}
const MEAS={
  funded:{l:'Funded and still held',v:r=>r.x.funded,e:r=>r.e.f},
  committed:{l:'Committed',v:r=>r.x.cu+r.x.csu,e:r=>r.e.c},
  contingent:{l:'Contingent maximum',v:r=>r.x.cont,e:r=>r.e.k},
  headline:{l:'Headline announced',v:r=>r.h,e:r=>r.e.h},
  gross:{l:'Gross exposure',v:r=>r.x.gross,e:r=>r.e.f.concat(r.e.c,r.e.k)},
  count:{l:'Relationships',v:r=>r.x.gross+1,e:r=>r.e.f.concat(r.e.c,r.e.k,r.e.h),d:r=>r.x.gross?((r.lb?'at least ':'')+money(r.x.gross)):'not sized'}
};
const tileNotes=$$('.tilew').map(w=>({k:w.querySelector('.tile').dataset.k,cnt:w.querySelector('.cnt'),v:w.querySelector('.v'),note:w.querySelector('.tnote'),orig:w.querySelector('.tnote').textContent}));
const tnText=$('#tile-note-text'), tnOrig=tnText?tnText.textContent:'';
function applyFilters(){
  const on=anyFilter(), dateOn=!!(F.from||F.to);
  document.body.classList.toggle('filtered',on);
  VIS = new Set(D.rels.filter(r=>!r.agg && relPass(r)).map(r=>r.id));
  // ledger rows
  $$('#ledger tbody tr.row').forEach(tr=>{ const ok=VIS.has(tr.dataset.id); tr.hidden=!ok; const d=tr.nextElementSibling;
    if(d&&d.classList.contains('detail')){ d.hidden=!ok; if(!ok && d.classList.contains('show')){ d.classList.remove('show'); const b=$('.disc',tr); if(b){ b.setAttribute('aria-expanded','false'); b.textContent='▸'; } } } });
  // totals and counts from the same visible set
  const t={funded:0,committed:0,contingent:0,headline:0,gross:0,n:0,lb:0}, c={funded:0,committed:0,contingent:0,headline:0};
  CORE.forEach(r=>{ if(!VIS.has(r.id)) return; t.n++; if(r.lb) t.lb++; TILES.forEach(k=>{ const v=MEAS[k].v(r)||0; t[k]+=v; if(v) c[k]++; }); t.gross+=r.x.gross||0; });
  const ft=$('#ledger tfoot'); if(ft){ ft.querySelector('[data-k=n]').textContent=plural(t.n,'relationship');
    [['funded','funded'],['cu','committed'],['cont','contingent'],['gross','gross'],['h','headline']].forEach(([k,m])=>{ const a=ft.querySelector('[data-k='+k+'] a'); if(a){ a.textContent=moneyS(t[m]); a.setAttribute('aria-label',money(t[m])+', total '+MEAS[m].l.toLowerCase()+': sources'); } }); }
  // tiles: value, count and note all follow the filter
  tileNotes.forEach(o=>{ o.v.innerHTML=moneyU(t[o.k]); o.cnt.textContent=plural(c[o.k],'relationship'); o.note.textContent = on ? ('Filtered: '+t.n+' of '+D.count+' relationships.') : o.orig; });
  $$('.tile').forEach(x=>x.setAttribute('aria-pressed', String(F.tile===x.dataset.k)));
  if(tnText){ tnText.textContent = !on ? tnOrig : (t.n ? ('Filters are on: '+t.n+' of '+D.count+' relationships. For this set, funded, committed and contingent add up to gross exposure of '+(t.lb?'at least ':'')+money(t.gross)+(t.lb?('; '+t.lb+' of '+t.n+' have a part that is not disclosed.'):'.')) : ('Filters are on: no relationship of '+D.count+' matches.')); }
  const c2=$('#clear-filters-2'); if(c2) c2.hidden=!on;
  const und = dateOn ? CORE.filter(r=>!r.d && relPass(r,true)).length : 0;
  const fn=$('#filtered-note'); if(fn){ fn.hidden=!on; fn.textContent='Filters are on: '+t.n+' of '+D.count+' relationships shown. Tiles, the map and the totals row show the same set.'+(und?(' '+plural(und,'undated relationship')+' hidden by the date range.'):''); }
  // map
  const ents = new Set(D.rels.filter(r=>VIS.has(r.id)).map(r=>r.to));
  $$('#map .node').forEach(n=>n.classList.toggle('dim', !ents.has(n.dataset.id)));
  $$('#map .edge,#map .halo').forEach(e=>e.classList.toggle('dim', !ents.has(e.dataset.to)));
  $$('#ranked li[data-ent]').forEach(li=>{ li.hidden=!ents.has(li.dataset.ent); });
  $$('#ranked .rgroup').forEach(g=>{ g.hidden=!$$('li',g).some(li=>!li.hidden); });
  // timeline: a mark is lit by its own date and by the other filters on its relationship
  const evOn=(date,rel)=>{ const r=REL[rel]; return (!F.from||date>=F.from) && (!F.to||date<=F.to) && !!r && relPass(r,true); };
  $$('#tl .ev').forEach(g=>g.classList.toggle('off', !evOn(g.dataset.date,g.dataset.rel)));
  $$('#tl-list li').forEach(li=>{ li.hidden = on && !evOn(li.dataset.date,li.dataset.rel); });
  // controls stay in step with the state
  $$('#ledger-filters select').forEach(s=>{ if(s.value!==F[s.name]) s.value=F[s.name]; });
  const tf=$('#tl-from'), tt=$('#tl-to'); if(tf){ tf.value=F.from; tt.value=F.to; }
  drawBrush();
  const rg=$('#tl-range'); if(rg) rg.textContent = dateOn ? ('Showing '+(F.from?dateLong(F.from):'the start')+' to '+(F.to?dateLong(F.to):dateLong(D.tlEnd))+'. '+t.n+' of '+D.count+' relationships.'+(und?(' '+plural(und,'undated relationship')+' hidden.'):'')) : '';
  writeHash();
}
function clearFilters(){ Object.keys(F).forEach(k=>F[k]=''); applyFilters(); }
$$('#ledger-filters select').forEach(s=>s.addEventListener('change',()=>{F[s.name]=s.value; applyFilters();}));
$$('.tile').forEach(b=>b.addEventListener('click',()=>{ const k=b.dataset.k; F.tile = F.tile===k?'':k; applyFilters(); }));
['#clear-filters','#clear-filters-2'].forEach(s=>{ const b=$(s); if(b) b.addEventListener('click',()=>{ clearFilters(); if(s==='#clear-filters-2'){ const t0=$('.tile'); if(t0) t0.focus(); } }); });

/* ---------------- sorting, in-place detail, scroll cue, CSV ---------------- */
$$('#ledger thead th[data-sort] button').forEach(btn=>btn.addEventListener('click',()=>{
  const th=btn.parentElement, key=th.dataset.sort, num=th.classList.contains('num'); const cur=th.getAttribute('aria-sort');
  const dir = cur ? (cur==='descending'?'ascending':'descending') : (num?'descending':'ascending');
  $$('#ledger thead th').forEach(x=>x.removeAttribute('aria-sort')); th.setAttribute('aria-sort',dir);
  const tb=$('#ledger tbody'); const pairs=$$('tr.row',tb).map(tr=>[tr,tr.nextElementSibling]);
  pairs.sort((a,b)=>{ let x=a[0].dataset[key]||'', y=b[0].dataset[key]||''; if(num){x=parseFloat(x)||0;y=parseFloat(y)||0;}else{x=x.toLowerCase();y=y.toLowerCase();} return (x<y?-1:x>y?1:0)*(dir==='ascending'?1:-1); });
  pairs.forEach(([r,d])=>{tb.appendChild(r); if(d) tb.appendChild(d);});
  const st=$('#ledger-status'); if(st) st.textContent='Sorted by '+btn.textContent+', '+dir+'.';
}));
$$('.disc').forEach(b=>{ b.hidden=false; });
function toggleDetail(b){ const tr=b.closest('tr'), d=tr.nextElementSibling; if(!d||!d.classList.contains('detail')) return; const open=!d.classList.contains('show');
  d.classList.toggle('show',open); const det=$('details',d); if(det) det.open=open; b.setAttribute('aria-expanded',String(open)); b.textContent=open?'▾':'▸'; }
const lw=$('#ledger-wrap'); function cue(){ if(!lw) return; const more=lw.scrollLeft < lw.scrollWidth-lw.clientWidth-2; lw.classList.toggle('more-right',more); const h=$('#scroll-hint'); if(h) h.hidden=!more; }
if(lw){ lw.addEventListener('scroll',cue,{passive:true}); }
const csvBtn=$('#csv'); if(csvBtn) csvBtn.addEventListener('click',()=>{
  const cols=['id','counterparty','cluster','type','status','source_strength','funded_still_held','committed_confirmed_unpaid','committed_paid_portion_undisclosed','contingent_max','gross_exposure','headline','announced','last_verified','reconciliation','significance','source_url'];
  if(D.showGrades) cols.splice(14,0,'grade');
  const q=v=>{v=v==null?'':String(v); return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;};
  const rows=[cols.join(',')]; D.rels.filter(r=>!r.agg && relPass(r)).forEach(r=>{ const e=D.ents[r.to]||{};
    const vals=[r.id,e.n,r.cll,r.tl,r.sl,r.bl,r.x.funded,r.x.cu,r.x.csu,r.x.cont,r.x.gross,r.h,r.d,r.lv,r.rc,r.sig,r.src]; if(D.showGrades) vals.splice(14,0,e.g||'');
    rows.push(vals.map(q).join(',')); });
  const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([rows.join('\n')],{type:'text/csv'})); a.download='nvidia-exposure-register.csv'; a.click(); });
function labelStack(root){ $$('table.stack',root).forEach(t=>{ const hs=$$('thead th',t).map(h=>h.textContent.trim()); $$('tbody tr',t).forEach(tr=>{ Array.from(tr.children).forEach((c,i)=>{ if(c.tagName==='TD' && hs[i]) c.setAttribute('data-label',hs[i]); }); }); }); }
labelStack(document);

/* ---------------- panel: a real modal ---------------- */
const panel=$('#panel'), pbody=$('#panel-body'), scrim=$('#scrim'); let lastFocus=null, closeT=null;
const isOpen=()=>panel.classList.contains('open');
function setInert(on){ Array.from(document.body.children).forEach(c=>{ if(c===panel||c===scrim||c.tagName==='SCRIPT'||c.classList.contains('pop')) return; if(on) c.setAttribute('inert',''); else c.removeAttribute('inert'); }); }
function syncXall(c){ const xa=$('.xall',c); if(!xa) return; const all=$$('details[data-sec]',c).every(d=>d.open); xa.dataset.mode=all?'collapse':'expand'; xa.textContent=all?'Collapse all':'Expand all'; }
function openPanel(id, push=true){
  const src=document.getElementById('p-'+id); if(!src) return false;
  clearTimeout(closeT); closePop(false);
  if(!isOpen()) lastFocus=document.activeElement;
  pbody.innerHTML=''; const c=src.cloneNode(true); $$('[id]',c).forEach(x=>x.removeAttribute('id')); c.removeAttribute('id'); c.hidden=false;
  const h=$('.cp',c); if(h){ const h2=document.createElement('h2'); h2.className='cp'; h2.id='panel-title'; h2.innerHTML=h.innerHTML; h.replaceWith(h2); panel.setAttribute('aria-labelledby','panel-title'); panel.removeAttribute('aria-label'); }
  pbody.appendChild(c); labelStack(c);
  const sects=load('sections',{}); $$('details[data-sec]',c).forEach(d=>{ if(sects[d.dataset.sec]) d.open=true; d.addEventListener('toggle',()=>{ const s=load('sections',{}); s[d.dataset.sec]=d.open; store('sections',s); syncXall(c); }); });
  syncXall(c);
  const xa=$('.xall',c); if(xa) xa.addEventListener('click',()=>{ const open=xa.dataset.mode!=='collapse'; $$('details[data-sec]',c).forEach(d=>d.open=open); syncXall(c); });
  panel.hidden=false; scrim.hidden=false; setInert(true); document.body.classList.add('panel-open'); panel.setAttribute('aria-hidden','false');
  void panel.offsetWidth; panel.classList.add('open'); panel.scrollTop=0;
  $('.close',panel).focus(); ST.rel=id; if(push) writeHash(); selectNode(D.relEnt[id]);
  return true;
}
function closePanel(){ if(!isOpen() && panel.hidden) return; closePop(false); panel.classList.remove('open'); panel.setAttribute('aria-hidden','true'); scrim.hidden=true; setInert(false); document.body.classList.remove('panel-open');
  clearTimeout(closeT); closeT=setTimeout(()=>{ panel.hidden=true; pbody.innerHTML=''; },reduced?0:200); ST.rel=null; writeHash(); selectNode(null);
  if(lastFocus && document.contains(lastFocus) && lastFocus.focus) lastFocus.focus(); lastFocus=null; }
$('.close',panel).addEventListener('click',closePanel);
scrim.addEventListener('click',closePanel);
function shown(x){ if(x.checkVisibility && !x.checkVisibility()) return false; if(x.disabled) return false;
  for(let d=x.parentElement&&x.parentElement.closest('details'); d; d=d.parentElement&&d.parentElement.closest('details')){ if(!d.open && !(x.tagName==='SUMMARY' && x.parentElement===d)) return false; }
  return x.getClientRects().length>0; }
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){
    if(pop){ e.preventDefault(); e.stopPropagation(); closePop(true); return; }
    if(isOpen()){ e.preventDefault(); closePanel(); return; }
    if(document.body.classList.contains('fullmap')){ e.preventDefault(); closeFull(); return; }
  }
  if(e.key==='Tab' && isOpen()){ const f=$$('a[href],button,summary,input,select,[tabindex="0"]',panel).filter(shown); if(!f.length){ e.preventDefault(); return; }
    const first=f[0], last=f[f.length-1], a=document.activeElement;
    if(!panel.contains(a)){ e.preventDefault(); first.focus(); }
    else if(e.shiftKey && a===first){ e.preventDefault(); last.focus(); }
    else if(!e.shiftKey && a===last){ e.preventDefault(); first.focus(); } }
});

/* ---------------- popovers: citations and the relationships behind a total ---------------- */
let pop=null, popAnchor=null;
function closePop(refocus){ if(!pop) return; const a=popAnchor; pop.remove(); pop=null; popAnchor=null; if(refocus && a && document.contains(a)) a.focus(); }
function showPop(anchor, inner, label){
  if(pop){ pop.remove(); pop=null; } popAnchor=anchor;
  pop=document.createElement('div'); pop.className='pop'; pop.setAttribute('role','dialog'); pop.setAttribute('aria-modal','false'); pop.setAttribute('aria-label',label);
  pop.innerHTML='<button class="btn pclose" type="button">Close</button>'+inner;
  const inPanel=panel.contains(anchor), w=Math.min(440, innerWidth-16), r=anchor.getBoundingClientRect(); pop.style.width=w+'px';
  if(inPanel){ panel.appendChild(pop); const pr=panel.getBoundingClientRect(); pop.style.top=(r.bottom-pr.top+panel.scrollTop+6)+'px'; pop.style.left=Math.max(8,Math.min(r.left-pr.left, pr.width-w-8))+'px'; }
  else { document.body.appendChild(pop); pop.style.top=(scrollY+r.bottom+6)+'px'; pop.style.left=Math.max(scrollX+8,Math.min(scrollX+r.left, scrollX+document.documentElement.clientWidth-w-8))+'px'; }
  $('.pclose',pop).focus({preventScroll:false});
}
function showCites(anchor, ids){
  const items=ids.map(i=>{ const li=document.getElementById('src-'+i); return li?li.innerHTML:'' }).filter(Boolean);
  showPop(anchor, items.length?('<ol class="srcs">'+items.map(x=>'<li>'+x+'</li>').join('')+'</ol>'):'<p class="ph">No citation is recorded for this figure.</p>', 'Sources');
}
function srcLine(ids){ ids=(ids||[]).filter(i=>document.getElementById('src-'+i)); if(!ids.length) return '<span class="ps note">No amount source recorded; open the relationship for its sources.</span>';
  const li=document.getElementById('src-'+ids[0]), tier=$('.tier',li), pd=$('.pubd',li), a=$('a',li);
  return '<span class="ps">'+(tier?'<span class="tier">'+esc(tier.textContent)+'</span>':'')+esc(pd?pd.textContent:'')+'. <a href="'+esc(a?a.getAttribute('href'):'#')+'" rel="noopener" target="_blank">Open source</a>'
    +(ids.length>1?' <a class="chip" role="button" href="#" data-ev="'+ids.join(' ')+'">All '+ids.length+' sources</a>':'')+'</span>'; }
function rowsHTML(rows){ return '<ol class="rows">'+rows.map(o=>'<li><span class="pv">'+esc(o.d)+'</span><a href="#row-'+o.r.id+'" data-open="'+o.r.id+'"><b>'+esc(entName(o.r.to))+'</b></a><span class="note blk">'+esc(o.r.ti)+(o.sub?(' ('+esc(o.sub)+')'):'')+'</span>'+srcLine(o.ev)+'</li>').join('')+'</ol>'; }
function showMeasure(anchor, chipEl){
  const key=chipEl.dataset.measure, M=MEAS[key]; if(!M) return; const ids=chipEl.dataset.rels?chipEl.dataset.rels.split(' '):null;
  const filtered=!ids && chipEl.dataset.scope==='filtered' && anyFilter();
  let rows=ids?ids.map(i=>REL[i]).filter(Boolean):(filtered?CORE.filter(r=>VIS.has(r.id)):CORE);
  rows=rows.map(r=>({r,v:M.v(r)||0})).filter(o=>o.v>0).sort((a,b)=>b.v-a.v);
  const sum=rows.reduce((a,o)=>a+o.v,0), top=rows.slice(0,ids?12:8).map(o=>({r:o.r,d:M.d?M.d(o.r):money(o.v),ev:M.e(o.r).length?M.e(o.r):o.r.e.a}));
  let head;
  if(ids) head='<p class="ph"><b>'+plural(rows.length,'relationship')+' behind this figure</b>, each with its '+M.l.toLowerCase()+' amount and source.</p>';
  else if(key==='count') head='<p class="ph"><b>'+plural(rows.length,'relationship')+'</b>'+(filtered?' in the filtered set':'')+'. The largest by gross exposure, each with its source.</p>';
  else head='<p class="ph"><b>'+M.l+': '+money(sum)+'</b> across '+plural(rows.length,'relationship')+(filtered?' in the filtered set':'')+'. Largest first, each with its source.</p>';
  let foot='';
  if(rows.length>top.length) foot='<p class="ph">'+(rows.length-top.length)+' more. <button type="button" class="btn" data-ledger="'+(TILES.indexOf(key)>=0?key:'')+'">Show all in the Ledger</button></p>';
  if(chipEl.dataset.ev2) foot+='<p class="ph"><a class="chip" role="button" href="#" data-ev="'+esc(chipEl.dataset.ev2)+'">All sources for this figure</a></p>';
  showPop(anchor, head+(top.length?rowsHTML(top):'<p>No relationship in this set has this amount.</p>')+foot, M.l+': sources');
}
function showStakes(anchor){ const rows=ST.stakes.map(o=>({r:REL[o.relationship],d:money(o.value),sub:{market_value:'market value',funded_remaining:'cost of the part still held',carrying_value:'carrying value'}[o.basis]||'',
    ev:o.basis==='market_value'?REL[o.relationship].e.mv:(o.basis==='carrying_value'?REL[o.relationship].e.cv:REL[o.relationship].e.f)})).filter(o=>o.r);
  showPop(anchor,'<p class="ph"><b>'+plural(rows.length,'stake')+' behind this figure</b>, each at the value the haircut is applied to.</p>'+rowsHTML(rows),'Stakes and sources'); }
document.addEventListener('click',e=>{
  const t=e.target; if(!(t instanceof Element)) return;
  if(t.closest('.pop .pclose')){ closePop(true); return; }
  const lg=t.closest('[data-ledger]'); if(lg){ closePop(false); if(lg.dataset.ledger){ F.tile=lg.dataset.ledger; applyFilters(); } const v=go('ledger-view'); if(v) v.focus({preventScroll:true}); return; }
  const sk=t.closest('[data-stakes]'); if(sk){ e.preventDefault(); showStakes(sk); return; }
  const m=t.closest('[data-measure]'); if(m){ e.preventDefault(); showMeasure(pop&&pop.contains(m)?popAnchor:m, m); return; }
  const ch=t.closest('[data-ev]'); if(ch){ e.preventDefault(); showCites(pop&&pop.contains(ch)?popAnchor:ch, ch.dataset.ev.split(' ')); return; }
  const op=t.closest('[data-open]'); if(op){ e.preventDefault(); closePop(false); openPanel(op.dataset.open); return; }
  if(pop && !pop.contains(t)) closePop(false);
  const dc=t.closest('.disc'); if(dc){ toggleDetail(dc); return; }
  const pl=t.closest('#panel a[href^="#"]'); if(pl){ e.preventDefault(); const id=pl.getAttribute('href').slice(1); closePanel(); const v=go(id); if(v){ v.setAttribute('tabindex','-1'); v.focus({preventScroll:true}); } return; }
  const tr=t.closest('tr.row'); if(tr && tr.dataset.id && (t.closest('.rowbtn') || !t.closest('a,button,summary,details,input,select'))){ openPanel(tr.dataset.id); }
});

/* ---------------- constellation ---------------- */
const svg=$('#map'); const NS='http://www.w3.org/2000/svg';
const COL={EQ:'var(--cobalt)','EQ-SPV':'var(--cobalt)','EQ-C':'#6F8BC8',BK:'var(--cochineal)',GU:'var(--cochineal)',RV:'var(--cochineal)',LB:'var(--rosa)',FC:'var(--cobalt-deep)',PP:'var(--ochre)',LP:'#4F6DB0',LI:'var(--leaf)',CX:'var(--ink-3)'};
function el(n,a,p){ const e=document.createElementNS(NS,n); for(const k in a) e.setAttribute(k,a[k]); if(p) p.appendChild(e); return e; }
const tip=$('#tip'); const CX=560, CY=500, VBX=-90, VBW=1300;
let gS=null, rov=null, selId=null;
/* one drawing per deal type, so color is never the only signal (spec/08 meaning map) */
function drawEdge(g,type,x1,y1,x2,y2,w,r){
  const col=COL[type]||'var(--ink-3)', dx=x2-x1, dy=y2-y1, len=Math.hypot(dx,dy)||1, ux=dx/len, uy=dy/len, nx=-uy, ny=ux, d=`M${x1},${y1} L${x2},${y2}`;
  const P=(a)=>el('path',Object.assign({stroke:col},a),g);
  if(type==='EQ-C'){ const ww=Math.max(w,4.5); P({d,'stroke-width':ww}); el('path',{d,stroke:'#fff','stroke-width':ww*0.4,'stroke-linecap':'butt'},g); }
  else if(type==='BK'||type==='GU'){ P({d,'stroke-width':w,'stroke-dasharray':'7 5','stroke-linecap':'butt'}); }
  else if(type==='RV'){ P({d,'stroke-width':w,'stroke-dasharray':'9 4 2 4','stroke-linecap':'butt'}); }
  else if(type==='LB'){ P({d,'stroke-width':Math.max(w,2.5),'stroke-dasharray':'0.1 '+Math.max(6,w*2)}); }
  else if(type==='FC'){ const tx=x2-ux*(r+3), ty=y2-uy*(r+3), s=7+w, bx=tx-ux*s*1.6, by=ty-uy*s*1.6; P({d:`M${x1},${y1} L${bx},${by}`,'stroke-width':w}); el('path',{d:`M${tx},${ty} L${bx+nx*s*0.7},${by+ny*s*0.7} L${bx-nx*s*0.7},${by-ny*s*0.7} z`,fill:col},g); }
  else if(type==='PP'){ const sw=Math.max(1.5,w/2.6), o=sw/2+1.1; P({d:`M${x1+nx*o},${y1+ny*o} L${x2+nx*o},${y2+ny*o}`,'stroke-width':sw}); P({d:`M${x1-nx*o},${y1-ny*o} L${x2-nx*o},${y2-ny*o}`,'stroke-width':sw}); }
  else if(type==='LP'){ P({d,'stroke-width':Math.max(1.5,w)}); P({d,'stroke-width':Math.max(1.5,w)+8,'stroke-dasharray':'1.6 14','stroke-linecap':'butt'}); }
  else if(type==='LI'){ P({d,'stroke-width':1.2}); }
  else if(type==='CX'){ P({d,'stroke-width':0.8}); }
  else { P({d,'stroke-width':w}); }
}
function drawMap(){
  if(!svg) return; const cx=CX, cy=CY; svg.setAttribute('viewBox',`${VBX} 0 ${VBW} 1000`);
  const rings=D.rings; const R0=105, outer=440;
  const counts=rings.map((_,i)=>D.nodes.filter(n=>n.ring===i).length); const used=counts.map(c=>c?1:0);
  const radii=[]; let acc=0; const tot=used.reduce((a,b)=>a+b,0)||1; rings.forEach((_,i)=>{ radii[i]=R0+30+(outer-R0-30)*(acc/(tot-1||1)); acc+=used[i]; });
  const gE=el('g',{'aria-hidden':'true'},svg), gL=el('g',{'aria-hidden':'true'},svg), gN=el('g',{},svg); gS=el('g',{class:'sat','aria-hidden':'true'},svg);
  const maxG=Math.max(1,...D.nodes.map(n=>n.gross||0));
  const pos={}; const labs=[];
  rings.forEach((ring,ri)=>{ if(!counts[ri]) return; const r=radii[ri]; el('circle',{class:'ring',cx,cy,r},gL);
    const ns=D.nodes.filter(n=>n.ring===ri); const off=0.18+ri*0.37; const step=2*Math.PI/Math.max(ns.length,1);
    ns.forEach((n,i)=>{ const a=(-Math.PI/2)+off+step*i; pos[n.id]={x:cx+r*Math.cos(a),y:cy+r*Math.sin(a),ring:ri,idx:i,a:a}; });
    labs.push({r,ns,off,step,label:ring.label}); });
  /* ring label: in a gap between two nodes of its ring, as near the top as possible, clear of every node and node label */
  const boxes=D.nodes.filter(n=>pos[n.id]).map(n=>{ const p=pos[n.id], rr=n.gross?6+16*Math.sqrt(n.gross/maxG):5, w=n.name.length*7.6+rr+8, right=p.x>=cx; return {x1:right?p.x-rr-2:p.x-w,x2:right?p.x+w:p.x+rr+2,y1:p.y-Math.max(rr,9)-2,y2:p.y+Math.max(rr,9)+2}; });
  labs.forEach(l=>{ let best=null; const hw=l.label.length*4.9+6;
    for(let i=0;i<l.ns.length;i++){ for(const f of [0.5,0.35,0.65]){ const m=(-Math.PI/2)+l.off+l.step*(i+f), x=cx+l.r*Math.cos(m), y=cy+l.r*Math.sin(m);
      const hits=boxes.filter(b=>x+hw>b.x1&&x-hw<b.x2&&y+10>b.y1&&y-10<b.y2).length+labs.filter(o=>o.px!=null&&Math.abs(o.px-x)<hw+o.hw&&Math.abs(o.py-y)<20).length;
      const score=hits*10+Math.abs(Math.atan2(Math.sin(m+Math.PI/2),Math.cos(m+Math.PI/2))); if(best==null||score<best.score) best={score,x,y}; } }
    if(!best) best={x:cx,y:cy-l.r}; l.px=best.x; l.py=best.y; l.hw=hw; });
  D.nodes.forEach(n=>{ const p=pos[n.id]; if(!p) return; const col=COL[n.type]||'var(--ink-3)';
    const w=n.gross?1.5+9*Math.sqrt(n.gross/maxG):1.2; const r=n.gross?6+16*Math.sqrt(n.gross/maxG):5; p.r=r;
    if(n.headline && n.headline>(n.gross||0)){ const hw=1.5+9*Math.sqrt(Math.min(n.headline,maxG*1.2)/maxG)+6; el('path',{class:'halo',d:`M${cx},${cy} L${p.x},${p.y}`,stroke:col,'stroke-width':hw,'data-to':n.id},gE); }
    const g=el('g',{class:'edge','data-to':n.id},gE); drawEdge(g,n.type,cx,cy,p.x,p.y,w,r); });
  labs.forEach(l=>{ const t=el('text',{class:'ringlab',x:l.px,y:l.py+4,'text-anchor':'middle'},gL); t.textContent=l.label; });
  const core=el('g',{class:'core','aria-hidden':'true'},gN); el('circle',{cx,cy,r:44},core); el('circle',{class:'c2',cx,cy,r:50},core); const ct=el('text',{x:cx,y:cy+5,'text-anchor':'middle'},core); ct.textContent='Nvidia';
  D.nodes.forEach((n,ni)=>{ const p=pos[n.id]; if(!p) return; const r=p.r;
    const g=el('g',{class:'node',tabindex:-1,role:'button','data-id':n.id,'aria-label':`${n.name}. ${D.rings[n.ring].label}. ${n.typeLabel}. Gross exposure ${n.gross?(n.lb?'at least ':'')+money(n.gross):'not sized'}.${n.wwr?' Specific wrong-way risk.':''}${n.sat.length?' '+plural(n.sat.length,'related party')+' listed in the panel.':''} Press Enter to open.`},gN);
    el('circle',{class:'hitc',cx:p.x,cy:p.y,r:Math.max(15,r+5)},g);
    el('circle',{class:'fr2',cx:p.x,cy:p.y,r:r+8},g); el('circle',{class:'fr',cx:p.x,cy:p.y,r:r+5},g); el('circle',{class:'hr',cx:p.x,cy:p.y,r:r+3.5},g);
    el('circle',{class:'dot',cx:p.x,cy:p.y,r},g);
    if(n.wwr){ el('path',{d:`M${p.x+r*0.7},${p.y-r*0.7} l7,-7 l3,10 z`,fill:'var(--cochineal)'},g); }
    const right=p.x>=cx; const t=el('text',{x:p.x+(right?r+6:-r-6),y:p.y+5,'text-anchor':right?'start':'end'},g); t.textContent=n.name;
    g.addEventListener('click',()=>openPanel(n.rel)); g.addEventListener('keydown',e=>keyNav(e,n,pos));
    g.addEventListener('mouseenter',()=>{ showTip(n,p); showSats(n.id); }); g.addEventListener('mouseleave',()=>{ tip.style.display='none'; showSats(selId); });
    g.addEventListener('focus',()=>{ setRov(g); showTip(n,p); showSats(n.id); let kb=false; try{ kb=g.matches(':focus-visible'); }catch(e){}
      if(kb) g.scrollIntoView({block:'center',inline:'center',behavior:reduced?'instant':'smooth'}); });
    g.addEventListener('blur',()=>{ tip.style.display='none'; showSats(selId); });
    if(ni===0) setRov(g);
  });
  ST.pos=pos;
  const box=$('#map-box'); if(box && box.scrollWidth>box.clientWidth) box.scrollLeft=(box.scrollWidth-box.clientWidth)/2;
  if(!reduced){ gN.style.opacity=0; gE.style.opacity=0; requestAnimationFrame(()=>{ gN.style.transition=gE.style.transition='opacity .4s ease-out'; gN.style.opacity=1; gE.style.opacity=1; }); }
}
function setRov(g){ if(rov&&rov!==g) rov.setAttribute('tabindex','-1'); rov=g; g.setAttribute('tabindex','0'); }
function showTip(n,p){ const b=svg.getBoundingClientRect(), s=b.width/VBW, box=$('#map-box'); tip.innerHTML=`<b>${esc(n.name)}</b><br>${esc(n.typeLabel)}<br>Gross exposure: ${n.gross?(n.lb?'at least ':'')+money(n.gross):'not sized'}${n.date?'<br>'+esc(n.date):''}${n.wwr?'<br>Specific wrong-way risk':''}`;
  tip.style.display='block'; const bb=box.getBoundingClientRect(); const left=b.left-bb.left+box.scrollLeft+(p.x-VBX)*s+14, top=b.top-bb.top+box.scrollTop+p.y*s+14;
  tip.style.left=Math.max(4,Math.min(left, box.scrollLeft+box.clientWidth-tip.offsetWidth-8))+'px'; tip.style.top=top+'px'; }
/* depth-2 parties: small satellites on the pointed, focused or opened node */
function showSats(id){ if(!gS) return; while(gS.firstChild) gS.removeChild(gS.firstChild); if(!id) return; const n=D.nodes.find(x=>x.id===id), p=ST.pos&&ST.pos[id]; if(!n||!p||!n.sat.length) return;
  const max=6, list=n.sat.slice(0,max), extra=n.sat.length-list.length, k=list.length+(extra?1:0), out=Math.atan2(p.y-CY,p.x-CX), spread=Math.min(2.6,0.62*k), R=p.r+56;
  for(let i=0;i<k;i++){ const a=out+(k===1?0:(-spread/2+spread*i/(k-1))), x=p.x+R*Math.cos(a), y=p.y+R*Math.sin(a), right=Math.cos(a)>=0;
    if(i<list.length){ el('line',{x1:p.x+(p.r+2)*Math.cos(a),y1:p.y+(p.r+2)*Math.sin(a),x2:x,y2:y},gS); el('circle',{cx:x,cy:y,r:4},gS); }
    const t=el('text',{x:x+(right?8:-8),y:y+4,'text-anchor':right?'start':'end'},gS); t.textContent=i<list.length?(list[i].n+(list[i].r?' ('+list[i].r+')':'')):('and '+extra+' more in the panel'); } }
function keyNav(e,n,pos){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); openPanel(n.rel); return; }
  if(!['ArrowRight','ArrowLeft','ArrowUp','ArrowDown'].includes(e.key)) return; e.preventDefault();
  const p=pos[n.id]; const onRing=r=>D.nodes.filter(x=>pos[x.id]&&pos[x.id].ring===r);
  if(e.key==='ArrowUp'||e.key==='ArrowDown'){ const step=e.key==='ArrowDown'?1:-1; let ring=p.ring+step, ns=[]; while(ring>=0&&ring<D.rings.length&&!(ns=onRing(ring)).length) ring+=step; if(!ns.length) return;
    const ad=(a,b)=>Math.abs(Math.atan2(Math.sin(a-b),Math.cos(a-b))); ns.sort((x,y)=>ad(pos[x.id].a,p.a)-ad(pos[y.id].a,p.a)); return focusNode(ns[0].id); }
  const ns=onRing(p.ring); const i=ns.findIndex(x=>x.id===n.id); const j=(i+(e.key==='ArrowRight'?1:-1)+ns.length)%ns.length; focusNode(ns[j].id); }
function focusNode(id){ const g=$(`#map .node[data-id="${id}"]`); if(g) g.focus(); }
function selectNode(id){ selId=id||null; $$('#map .node').forEach(n=>n.classList.toggle('sel', !!id && n.dataset.id===id)); showSats(selId); }
function setHits(ids){ $$('#map .node').forEach(n=>n.classList.toggle('hit', ids.includes(n.dataset.id))); const lg=$('#legend-stress'); if(lg) lg.hidden=!ST.hl; }
drawMap();
const loopBtn=$('#show-loops'); if(loopBtn) loopBtn.addEventListener('click',()=>{ const on=loopBtn.getAttribute('aria-pressed')!=='true'; loopBtn.setAttribute('aria-pressed',String(on));
  $$('#map .loopedge').forEach(x=>x.remove()); if(!on) return; const g=svg.querySelector('g'); D.loopEnts.forEach(ids=>{ for(let i=0;i<ids.length-1;i++){ const a=ST.pos[ids[i]], b=ST.pos[ids[i+1]]; if(a&&b) el('path',{class:'loopedge',d:`M${a.x},${a.y} Q${CX},${CY} ${b.x},${b.y}`},g);} }); });
const clearHit=$('#clear-hit'); if(clearHit) clearHit.addEventListener('click',()=>{ ST.hl=false; setHits([]); const b=$('#show-loops'); if(b) b.focus(); });
const viewList=$('#view-list'); if(viewList) viewList.addEventListener('click',()=>{ const on=!document.body.classList.contains('show-list'); document.body.classList.toggle('show-list',on); viewList.setAttribute('aria-pressed',String(on)); if(on) go('ranked'); });
/* phone: full-screen map with a way out (button, Escape, Back) */
const fm=$('#full-map'), mapClose=$('#map-close');
function openFull(){ if(document.body.classList.contains('fullmap')) return; document.body.classList.add('fullmap'); try{ history.pushState({fullmap:1},''); }catch(e){}
  const box=$('#map-box'); box.scrollLeft=(box.scrollWidth-box.clientWidth)/2; box.scrollTop=Math.max(0,(box.scrollHeight-box.clientHeight)/2-40); mapClose.focus(); }
function closeFull(fromPop){ if(!document.body.classList.contains('fullmap')) return; document.body.classList.remove('fullmap'); tip.style.display='none';
  if(!fromPop && history.state && history.state.fullmap){ try{ history.back(); }catch(e){} } if(fm) fm.focus(); }
if(fm) fm.addEventListener('click',openFull);
if(mapClose) mapClose.addEventListener('click',()=>closeFull(false));
addEventListener('popstate',()=>{ if(document.body.classList.contains('fullmap')) closeFull(true); });

/* ---------------- timeline: one state for brush, dates and caption ---------------- */
const tl=$('#tl'); let evRov=null;
function setRange(from,to){ if(from&&to&&from>to){ const x=from; from=to; to=x; } F.from=from||''; F.to=to||''; applyFilters(); }
function drawBrush(){ if(!ST.brush||!ST.tlx) return; if(!(F.from||F.to)){ ST.brush.setAttribute('width',0); return; }
  const a=ST.tlx(Date.parse(F.from||D.tlStart)), c=ST.tlx(Date.parse(F.to||D.tlEnd)); ST.brush.setAttribute('x',Math.min(a,c)); ST.brush.setAttribute('width',Math.max(2,Math.abs(c-a))); }
function drawTimeline(){ if(!tl) return; while(tl.firstChild) tl.removeChild(tl.firstChild); const box=$('#tl-box');
  const lanes=D.lanes, W=Math.max(720,Math.floor(box.clientWidth||0)), LH=30, top=24, H=top+lanes.length*LH+28; tl.setAttribute('viewBox',`0 0 ${W} ${H}`); tl.setAttribute('height',H);
  const t0=Date.parse(D.tlStart), t1=Date.parse(D.tlEnd), L=176, Rr=W-16, xs=t=>Math.max(L,Math.min(Rr,L+(Rr-L)*(t-t0)/(t1-t0)));
  const bg=el('g',{'aria-hidden':'true'},tl);
  lanes.forEach((ln,i)=>{ const y=top+i*LH+LH/2; el('line',{x1:L,x2:Rr,y1:y,y2:y,stroke:'var(--line)'},bg); const tx=el('text',{class:'lane',x:L-10,y:y+4,'text-anchor':'end'},bg); tx.textContent=ln.label; });
  for(let y=2023;y<=2030;y++){ const tt=Date.parse(y+'-01-01'); if(tt<t0||tt>t1) continue; const x=xs(tt); el('line',{x1:x,x2:x,y1:top-6,y2:H-22,stroke:'var(--line)','stroke-dasharray':'2 3'},bg); const t=el('text',{class:'axis',x:x,y:H-7,'text-anchor':y===2023?'start':'middle'},bg); t.textContent=y; }
  const brush=el('rect',{class:'brush',x:0,y:top-6,width:0,height:lanes.length*LH+6},tl);
  evRov=null;
  D.events.forEach((ev,i)=>{ const li=lanes.findIndex(l=>l.key===ev.lane); if(li<0) return; const y=top+li*LH+LH/2, x=xs(Date.parse(ev.date)); const ended=ev.kind==='termination'||ev.kind==='restructuring';
    const label=dateLong(ev.date)+': '+entName(D.relEnt[ev.rel])+'. '+(ended?'Restructured or ended. ':'')+ev.summary.replace(/\b\d{4}-\d\d-\d\d\b/g,m=>dateLong(m));
    const g=el('g',{class:'ev','data-rel':ev.rel,'data-date':ev.date,'data-i':i,tabindex:-1,role:'button','aria-label':label},tl);
    el('circle',{class:'hitc',cx:x,cy:y,r:11},g);
    if(ended) el('path',{d:`M${x},${y-7} L${x+7},${y} L${x},${y+7} L${x-7},${y} z`,fill:'var(--cochineal)'},g); else el('circle',{cx:x,cy:y,r:5.5,fill:'var(--cobalt)'},g);
    const t=el('title',{},g); t.textContent=label;
    g.addEventListener('click',()=>openPanel(ev.rel));
    g.addEventListener('focus',()=>{ if(evRov&&evRov!==g) evRov.setAttribute('tabindex','-1'); evRov=g; g.setAttribute('tabindex','0'); });
    g.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); openPanel(ev.rel); return; }
      if(e.key==='ArrowRight'||e.key==='ArrowLeft'||e.key==='Home'||e.key==='End'){ e.preventDefault(); const all=$$('#tl .ev'); let j=all.indexOf(g)+(e.key==='ArrowRight'?1:-1); if(e.key==='Home') j=0; if(e.key==='End') j=all.length-1; j=Math.max(0,Math.min(all.length-1,j)); all[j].focus(); } });
    if(!evRov){ evRov=g; g.setAttribute('tabindex','0'); } });
  ST.brush=brush; ST.tlx=xs;
  if(!ST.tlBound){ ST.tlBound=true; let x0=null; const px=e=>{ const b=tl.getBoundingClientRect(), vb=tl.viewBox.baseVal; return (e.clientX-b.left)*vb.width/b.width; };
    const toDate=x=>{ const g=ST.geo; return new Date(g.t0+(g.t1-g.t0)*(Math.max(g.L,Math.min(g.Rr,x))-g.L)/(g.Rr-g.L)).toISOString().slice(0,10); };
    tl.addEventListener('pointerdown',e=>{ if(e.target.closest('.ev')) return; x0=px(e); try{ tl.setPointerCapture(e.pointerId); }catch(err){} e.preventDefault(); });
    tl.addEventListener('pointermove',e=>{ if(x0==null) return; const x=px(e); ST.brush.setAttribute('x',Math.min(x0,x)); ST.brush.setAttribute('width',Math.abs(x-x0)); });
    const end=e=>{ if(x0==null) return; const x=px(e), a=x0; x0=null; if(Math.abs(x-a)<4) setRange('',''); else setRange(toDate(Math.min(a,x)),toDate(Math.max(a,x))); };
    tl.addEventListener('pointerup',end); tl.addEventListener('pointercancel',()=>{ x0=null; drawBrush(); }); }
  ST.geo={t0,t1,L,Rr};
}
drawTimeline();
const tf=$('#tl-from'), tt=$('#tl-to'); if(tf) [tf,tt].forEach(i=>i.addEventListener('change',()=>setRange(tf.value,tt.value)));
const tlc=$('#tl-clear'); if(tlc) tlc.addEventListener('click',()=>setRange('',''));
let rzT=null, lastW=innerWidth; addEventListener('resize',()=>{ clearTimeout(rzT); rzT=setTimeout(()=>{ cue(); if(innerWidth!==lastW){ lastW=innerWidth; drawTimeline(); applyFilters(); } },150); });

/* ---------------- stress ---------------- */
const SC=D.scen;
const EFFECT={S1:{h1:1},S2:{h2:1},S3:{v:1}};
const PCT={d:1,p:1,h1:1,h2:1,v:1};
function fmtParam(k,v){ v=parseFloat(v); if(PCT[k]) return Math.round(v*100)+'%'; if(k==='quarters') return plural(v,'quarter'); if(k==='months') return plural(v,'month'); return String(v); }
function sliderHTML(sid){ const ps=SC.config[sid].parameters; return Object.keys(ps).filter(k=>ps[k].min!==undefined).map(k=>{ const p=ps[k], on=!!EFFECT[sid][k];
  return `<label>${esc(p.label)}: <output id="o-${sid}-${k}">${fmtParam(k,p.value)}</output>${p.basis==='illustrative'?' <span class="illus">Illustrative</span>':''}<input type="range" min="${p.min}" max="${p.max}" step="${p.step}" value="${p.value}" data-k="${k}" aria-label="${esc(p.label)}" aria-valuetext="${fmtParam(k,p.value).replace('-','minus ').replace('%',' percent')}"${on?'':' disabled aria-disabled="true"'}>${on?'':'<span class="cap">No effect yet: the inputs this would move are not disclosed.</span>'}</label>`; }).join(''); }
function runScenario(sid, user, vals){
  if(!SC[sid]) return; ST.shown=sid; if(user){ ST.scenario=sid; ST.hl=true; }
  $$('.scen button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.s===sid)));
  const box=$('#sliders'); box.innerHTML=sliderHTML(sid);
  if(sid==='S2'){ const labs=Object.keys(SC.S2); const sel=document.createElement('label'); sel.innerHTML='Lab: <select id="lab">'+labs.map(l=>`<option value="${l}">${esc(entName(l))}</option>`).join('')+'</select>'; box.prepend(sel);
    const def=labs.includes(ST.lab)?ST.lab:(labs.includes('ent_openai')?'ent_openai':labs[0]); $('#lab').value=def; ST.lab=def; $('#lab').addEventListener('change',()=>{ ST.lab=$('#lab').value; ST.scenario=sid; compute(sid); writeHash(); }); }
  $$('input[type=range]',box).forEach(i=>{ if(vals && vals[i.dataset.k]!=null && !i.disabled){ i.value=vals[i.dataset.k]; }
    const upd=()=>{ const t=fmtParam(i.dataset.k,i.value); $(`#o-${sid}-${i.dataset.k}`).textContent=t; i.setAttribute('aria-valuetext',t.replace('-','minus ').replace('%',' percent')); }; upd();
    i.addEventListener('input',()=>{ upd(); ST.scenario=sid; compute(sid); writeHash(); }); });
  compute(sid); writeHash();
}
function val(k){ const i=$(`#sliders input[data-k="${k}"]`); return i?parseFloat(i.value):null; }
function evChip(ids,label,what){ ids=(ids||[]).filter(i=>document.getElementById('src-'+i)); if(!ids.length) return ''; return ' <a class="chip" role="button" href="#sources" data-ev="'+ids.join(' ')+'" aria-label="'+plural(ids.length,'source')+(what?' for '+esc(what):'')+'">'+(label||'Source')+(ids.length>1?' ('+ids.length+')':'')+'</a>'; }
const stakeChip=' <a class="chip" role="button" href="#ledger-view" data-stakes="1" aria-label="Stakes and sources behind this figure">Sources</a>';
function compute(sid){
  const out=$('#stress-out'); let html='', affected=[]; const eq=D.fin.equity, fcf=D.fin.fcf; ST.stakes=[];
  const share=(x,d)=>d?(100*x/d).toFixed(2)+'%':'not computable';
  const lab0='<p class="k">Loss in this scenario <span class="analysis">Analysis</span></p>';
  const ncTitle=x=>clean(x.title||(REL[x.relationship]||{}).ti||x.facility||'Record');
  if(sid==='S1'){ const s=SC.S1, h1=val('h1'); const loss=s.equity_losses.reduce((a,e)=>a+e.value*h1,0); const ead=s.equity_losses.reduce((a,e)=>a+e.value,0); ST.stakes=s.equity_losses;
    affected=s.affected; html=`${lab0}<p class="big">${money(loss)}${stakeChip}</p><p>Loss on ${s.equity_losses.length} neocloud equity stakes worth ${money(ead)}${stakeChip} after a ${Math.round(h1*100)}% haircut. That is ${share(loss,eq)} of Nvidia's shareholders' equity${evChip(D.fin.equityEv,'Source','shareholders\' equity')} and ${share(loss,fcf)} of a year's free cash flow${evChip(D.fin.fcfEv,'Source','free cash flow')}.</p>
      <p>No backstop draw is computable: the contracted floors behind Nvidia's capacity backstops are not disclosed. Guaranties of leases sit outside this scenario.</p>`;
    if(s.not_computable.length) html+=`<details><summary>Not computable (${s.not_computable.length})</summary><ul>${s.not_computable.map(x=>`<li>${ncTitle(x)}: ${clean(x.reason)}</li>`).join('')}</ul></details>`; }
  if(sid==='S2'){ const lab=$('#lab').value, s=SC.S2[lab], h2=val('h2'); const loss=s.equity_losses.reduce((a,e)=>a+e.value*h2,0); ST.stakes=s.equity_losses;
    affected=s.affected; html=`${lab0}<p class="big">${s.equity_losses.length?money(loss)+stakeChip:'Not computable'}</p><p>${s.equity_losses.length?`Equity loss on stakes in ${esc(entName(lab))} with a confirmed value, after a ${Math.round(h2*100)}% haircut; ${share(loss,eq)} of Nvidia's equity${evChip(D.fin.equityEv,'Source','shareholders\' equity')}.`:'No stake in this lab has a confirmed value.'}</p>`;
    (s.not_computable||[]).filter(x=>x.relationship).forEach(x=>{ const r=REL[x.relationship]||{e:{a:[]}}; html+=`<p>${ncTitle(x)}: ${clean(x.reason)}${evChip(r.e.c.concat(r.e.f).length?r.e.c.concat(r.e.f):r.e.a,'Source','this relationship')}</p>`; });
    (s.guaranties_triggered_by_lab_default||[]).forEach(g=>{ const r=REL[g.relationship]; html+=`<p>Guaranty this lab's default would trigger: ${money(g.cap)} cap${g.in_force?'':', not yet in force'}.${r?evChip(r.e.k,'Source','the guaranty cap'):''}</p>`; });
    s.lapsed_commitments.forEach(c=>{ const r=REL[c.relationship]; html+=`<p>Other Nvidia commitment to this lab: ${clean(c.title)}${c.headline?` (headline ${money(c.headline)}, not counted as exposure)`:''}.${r?evChip(r.e.h.length?r.e.h:r.e.a,'Source','this commitment'):''}</p>`; });
    const con=s.at_risk_backlog.filter(x=>x.kind==='contract'), les=s.at_risk_backlog.filter(x=>x.kind==='lease'); const evs=l=>Array.from(new Set(l.reduce((a,x)=>a.concat(x.evidence||[]),[])));
    if(con.length){ const soft=con.reduce((a,x)=>a+(x.soft_amount||0),0); html+=`<p>Contracts other companies hold with this lab: up to ${money(con.reduce((a,x)=>a+x.amount,0))} across ${con.length}${soft?`, of which ${money(soft)} is stated as up to, cancellable or terminable`:''}. These are what a funding gap would put at risk for them.${evChip(evs(con),'Sources','these contracts')}</p>`; }
    if(les.length) html+=`<p>Lease obligations of this lab: ${money(les.reduce((a,x)=>a+x.amount,0))}.${evChip(evs(les),'Sources','these leases')}</p>`; }
  if(sid==='S3'){ const s=SC.S3, v=val('v'); const rows=s.facilities.map(f=>{ const after=f.ltv_before/(1+v); const over=f.covenant_ltv?after>f.covenant_ltv:null;
      return `<tr><th scope="row">${esc(entName(f.entity))}</th><td>${clean(f.facility)}</td><td class="num">${(f.ltv_before*100).toFixed(0)}%${evChip(D.projEv[f.project],'Source','this facility')}</td><td class="num">${isFinite(after)?(after*100).toFixed(0)+'%':'not computable'}</td><td>${f.covenant_ltv?(f.covenant_ltv*100).toFixed(0)+'%':'not sourced'}</td><td>${over==null?'':over?'Over':'Within'}</td></tr>`; }).join('');
    affected=s.affected; html=`<p class="k">Result <span class="analysis">Analysis</span></p><p>Loan to value on GPU-backed facilities after a ${Math.round(-v*100)}% fall in prior generation GPU values. Collateral repricing hits lenders first; Nvidia's loss is indirect and is not estimated.</p>
      ${rows?`<div class="tbl-wrap"><table class="stack"><thead><tr><th scope="col">Borrower</th><th scope="col">Facility</th><th scope="col" class="num">Before</th><th scope="col" class="num">After</th><th scope="col">Covenant</th><th scope="col">Against covenant</th></tr></thead><tbody>${rows}</tbody></table></div>`:''}
      <details><summary>${s.not_computable.length} facilities are not computable</summary><p class="note">Each needs both a sourced balance and a sourced collateral value.</p><ul>${s.not_computable.map(x=>`<li>${ncTitle(x)}</li>`).join('')}</ul></details>`; }
  out.innerHTML=html; labelStack(out); ST.affected=affected; setHits(ST.hl?affected:[]);
}
$$('.scen button').forEach(b=>b.addEventListener('click',()=>runScenario(b.dataset.s,true)));

/* ---------------- what changed filter ---------------- */
const cf=$('#change-filter'); if(cf) cf.addEventListener('change',()=>{ $$('#changes-list > li').forEach(li=>li.hidden = !!cf.value && li.dataset.type!==cf.value); });

/* ---------------- view nav state ---------------- */
const navLinks=$$('nav.views a');
function setCurrent(id){ navLinks.forEach(a=>{ if(a.getAttribute('href')==='#'+id){ a.setAttribute('aria-current','location'); const ul=a.closest('ul'); if(ul && ul.scrollWidth>ul.clientWidth) ul.scrollLeft=Math.max(0,a.offsetLeft-ul.offsetLeft-40); } else a.removeAttribute('aria-current'); }); }
const io=('IntersectionObserver' in window)? new IntersectionObserver(es=>{ es.forEach(e=>{ if(e.isIntersecting) setCurrent(e.target.id); }); },{rootMargin:'-60px 0px -70% 0px'}):null;
if(io) $$('section.view').forEach(s=>io.observe(s));
function navTo(id){ const v=go(id); if(!v) return; ST.view=id; writeHash(); v.focus({preventScroll:true}); setCurrent(id); }
navLinks.forEach(a=>a.addEventListener('click',e=>{ e.preventDefault(); navTo(a.getAttribute('href').slice(1)); }));
const pillc=$('a.pill[href^="#"]'); if(pillc) pillc.addEventListener('click',e=>{ e.preventDefault(); navTo(pillc.getAttribute('href').slice(1)); });
$$('.skip-in').forEach(a=>a.addEventListener('click',e=>{ e.preventDefault(); navTo(a.getAttribute('href').slice(1)); }));

/* ---------------- phone folds, print ---------------- */
function phoneSync(){ const m=$('details.more'); if(m) m.open=!phone.matches; const l=$('#tl-list'); if(l && phone.matches) l.open=true; }
if(phone.addEventListener) phone.addEventListener('change',phoneSync); phoneSync();
let printState=null;
addEventListener('beforeprint',()=>{ printState={open:$$('details').filter(d=>d.open),moved:false}; const m=$('details.more'); if(m) m.open=true;
  if(isOpen()){ $$('details',panel).forEach(d=>d.open=true); document.body.insertBefore(panel,document.body.firstChild); printState.moved=true; } });
addEventListener('afterprint',()=>{ if(!printState) return; if(printState.moved){ document.body.insertBefore(panel,$('#sources-lib')); $$('details',panel).forEach(d=>{ d.open=printState.open.includes(d); }); }
  const m=$('details.more'); if(m) m.open=printState.open.includes(m)||!phone.matches; printState=null; });

/* ---------------- restore state from the URL, and follow it when it changes ---------------- */
function parseP(s){ const o={}; (s||'').split(',').forEach(kv=>{ const i=kv.indexOf(':'); if(i>0){ const v=parseFloat(kv.slice(i+1)); if(isFinite(v)) o[kv.slice(0,i)]=v; } }); return o; }
function applyState(h, initial){
  HK.forEach(k=>{ F[k]=h[k]||''; }); F.tile=TILES.indexOf(h.filter)>=0?h.filter:'';
  ['from','to'].forEach(k=>{ if(F[k] && !/^\d{4}-\d\d-\d\d$/.test(F[k])) F[k]=''; });
  if(h.scenario && SC[h.scenario] && h.scenario!=='config'){ ST.scenario=h.scenario; ST.hl=true; if(h.lab) ST.lab=h.lab; runScenario(h.scenario,false,parseP(h.p)); }
  else if(initial){ ST.scenario=null; ST.hl=false; runScenario('S1',false); }
  applyFilters();
  if(h.view && document.getElementById(h.view)){ ST.view=h.view; go(h.view,true); }
  if(h.rel){ if(ST.rel!==h.rel || !isOpen()){ if(!openPanel(h.rel,false)){ ST.rel=null; } } } else if(isOpen()) closePanel();
  writeHash();
}
applyState(readHash(), true);
addEventListener('hashchange',()=>applyState(readHash(), false));
cue();
})();
"""
