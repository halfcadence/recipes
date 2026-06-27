#!/usr/bin/env node
/* Tiny zero-dependency markdown -> riso-styled HTML renderer for local review.
   Renders cafe/*.md into cafe/site/review/ and builds an index hub.
   Run: node cafe/site/build-review.js   (from repo root or anywhere) */
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", ".."); // repo root
const CAFE = path.join(ROOT, "cafe");
const OUT  = path.join(CAFE, "site", "review");
fs.mkdirSync(OUT, { recursive: true });

const esc = s => s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
function inline(s){
  s = esc(s);
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (m,t,u)=>`<a href="${u.replace(/\.md$/,'.html').replace(/^\.\//,'')}">${t}</a>`);
  return s;
}
function mdToHtml(md){
  const lines = md.split("\n");
  let html = "", i = 0, inTable = false, inCode = false, inUL = false, inOL = false, inBQ = false;
  const closeLists = () => { if(inUL){html+="</ul>";inUL=false;} if(inOL){html+="</ol>";inOL=false;} };
  const closeTable = () => { if(inTable){html+="</tbody></table>";inTable=false;} };
  const closeBQ = () => { if(inBQ){html+="</blockquote>";inBQ=false;} };
  while(i < lines.length){
    let ln = lines[i];
    if(/^```/.test(ln)){ if(!inCode){closeLists();closeTable();closeBQ();html+="<pre><code>";inCode=true;} else {html+="</code></pre>";inCode=false;} i++; continue; }
    if(inCode){ html += esc(ln)+"\n"; i++; continue; }
    if(/^\s*---\s*$/.test(ln)){ closeLists();closeTable();closeBQ(); html+="<hr>"; i++; continue; }
    // table
    if(/^\|/.test(ln) && /^\s*\|?[\s:|-]+\|/.test(lines[i+1]||"")){
      closeLists();closeBQ();
      const cells = r => r.replace(/^\||\|$/g,"").split("|").map(c=>c.trim());
      html += '<table><thead><tr>'+cells(ln).map(c=>`<th>${inline(c)}</th>`).join("")+'</tr></thead><tbody>';
      i += 2;
      while(i<lines.length && /^\|/.test(lines[i])){ html += '<tr>'+cells(lines[i]).map(c=>`<td>${inline(c)}</td>`).join("")+'</tr>'; i++; }
      html += '</tbody></table>'; continue;
    }
    let m;
    if((m=ln.match(/^(#{1,6})\s+(.*)/))){ closeLists();closeTable();closeBQ(); const l=m[1].length; html+=`<h${l}>${inline(m[2])}</h${l}>`; i++; continue; }
    if(/^>\s?/.test(ln)){ closeLists();closeTable(); if(!inBQ){html+="<blockquote>";inBQ=true;} html+=inline(ln.replace(/^>\s?/,""))+" "; i++; continue; } else closeBQ();
    if((m=ln.match(/^\s*[-*]\s+(.*)/))){ closeTable(); if(!inUL){closeLists();html+="<ul>";inUL=true;} html+=`<li>${inline(m[1])}</li>`; i++; continue; }
    if((m=ln.match(/^\s*\d+\.\s+(.*)/))){ closeTable(); if(!inOL){closeLists();html+="<ol>";inOL=true;} html+=`<li>${inline(m[1])}</li>`; i++; continue; }
    if(/^\s*$/.test(ln)){ closeLists();closeTable();closeBQ(); i++; continue; }
    closeLists();closeTable();closeBQ();
    html += `<p>${inline(ln)}</p>`; i++;
  }
  closeLists();closeTable();closeBQ();
  return html;
}

const CSS = `
:root{--blue:#0078bf;--pink:#ff48b0;--over:#cc2464;--paper:#fbfaf8;--ink:#435060;--gray:#88898a;--rule:#d2d4d6}
*{box-sizing:border-box}
body{font-family:'Bricolage Grotesque',system-ui,sans-serif;background:var(--paper);color:var(--ink);line-height:1.6;margin:0;font-size:16px}
.inkbar{height:12px;background:linear-gradient(to right,var(--over) 0 20%,var(--pink) 20% 40%,var(--blue) 40% 60%,var(--over) 60% 80%,var(--pink) 80% 100%)}
.wrap{max-width:820px;margin:0 auto;padding:28px 24px 80px}
.back{font-family:ui-monospace,monospace;font-size:13px}
h1{font-size:30px;font-weight:800;color:var(--blue);letter-spacing:-1px;margin:18px 0 4px}
h2{font-size:13px;font-family:ui-monospace,monospace;letter-spacing:2px;text-transform:uppercase;color:var(--over);margin:30px 0 8px;border-bottom:1px solid var(--rule);padding-bottom:5px}
h3{font-size:18px;font-weight:600;color:var(--blue);margin:18px 0 4px}
h4{font-size:15px;font-weight:600;margin:14px 0 4px}
a{color:var(--blue)} a:hover{color:var(--over)}
code{font-family:ui-monospace,monospace;background:#eef0f2;padding:1px 5px;border-radius:3px;font-size:.9em}
pre{background:#222a34;color:#c9ced5;padding:14px 16px;border-radius:6px;overflow:auto;font-size:13px}
pre code{background:none;color:inherit;padding:0}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14.5px}
th,td{border:1px solid var(--rule);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#eef0f2;font-weight:600}
blockquote{border-left:3px solid var(--pink);margin:12px 0;padding:6px 16px;background:#fff;color:var(--ink)}
hr{border:none;border-top:1px solid var(--rule);margin:26px 0}
ul,ol{padding-left:22px}
img{max-width:100%}
.card{display:block;border:1px solid var(--rule);background:#fff;padding:16px 18px;margin:10px 0;text-decoration:none}
.card:hover{border-color:var(--blue)}
.card .t{font-weight:600;color:var(--blue);font-size:18px}
.card .d{color:var(--ink);font-size:14px;margin-top:3px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.assets{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px;margin-top:10px}
.assets figure{margin:0;text-align:center}
.assets img{border:1px solid var(--rule);background:#fbfaf8;width:100%}
.assets figcaption{font-family:ui-monospace,monospace;font-size:11px;color:var(--gray);margin-top:4px}
@media(max-width:620px){.grid2{grid-template-columns:1fr}}
`;
const head = (title) => `<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;800&display=swap" rel="stylesheet"><style>${CSS}</style></head><body><div class="inkbar"></div><div class="wrap">`;
const foot = `</div></body></html>`;

// render markdown docs
const docs = [
  { src: "README.md", title: "Half Cadence — overview" },
  { src: "plan.md", title: "Business + UX Plan" },
  { src: "farmers-market-playbook.md", title: "Farmers-Market Playbook" },
  { src: "water-activity-test-plan.md", title: "Water-Activity Test Plan" },
  { src: "canele-cost.md", title: "Canelé Cost per Unit" },
  { src: "flavor-cost.md", title: "Flavored Canelé Costs" },
  { src: "combo-pricing.md", title: "Combo Pricing — coffee + canelé" },
  { src: "alcohol-in-pastry.md", title: "Alcohol in Pastry — rules + swaps" },
  { src: "experiment-10pct-structure.md", title: "Experiment — structure % × cornstarch" },
  { src: path.join("brand","README.md"), title: "Brand Kit" },
];
for(const d of docs){
  const md = fs.readFileSync(path.join(CAFE, d.src), "utf8");
  const body = mdToHtml(md);
  const outName = d.src.replace(/[\/\\]/g,"__").replace(/\.md$/,".html");
  const html = head(d.title) + `<div class="back"><a href="index.html">&larr; review hub</a></div>` + body + foot;
  fs.writeFileSync(path.join(OUT, outName), html);
}

// brand asset gallery (SVG previews + Nova riso PNGs)
const pngDir = path.join(CAFE,"brand","png");
const pngs = fs.existsSync(pngDir) ? fs.readdirSync(pngDir).filter(f=>f.endsWith(".png")).sort() : [];
let assetCards = pngs.map(p=>`<figure><img src="../../brand/png/${p}" alt="${p}"><figcaption>${p.replace('.png','')}</figcaption></figure>`).join("");
const risoDir = path.join(CAFE,"brand","gen-riso");
const risos = fs.existsSync(risoDir) ? fs.readdirSync(risoDir).filter(f=>f.endsWith(".png")).sort() : [];
assetCards += risos.map(p=>`<figure><img src="../../brand/gen-riso/${p}" alt="${p}"><figcaption>gen-riso/${p.replace('.png','')}</figcaption></figure>`).join("");

// hub
const hub = head("Half Cadence — review hub") +
`<h1>half / cadence</h1>
<p style="font-family:ui-monospace,monospace;color:var(--gray);font-size:13px">local review hub · all the café concept artifacts</p>

<h2>Live site pages</h2>
<div class="grid2">
  <a class="card" href="../index.html"><div class="t">Landing page →</div><div class="d">index.html — the storefront</div></a>
  <a class="card" href="../today.html"><div class="t">Today board →</div><div class="d">today.html — live flavor drop, real glyphs</div></a>
</div>

<h2>Documents</h2>
<div class="grid2">
  <a class="card" href="README.html"><div class="t">Overview</div><div class="d">what this is, the shape of the plan</div></a>
  <a class="card" href="plan.html"><div class="t">Business + UX Plan</div><div class="d">numbers, location, beverage program, brand, floor plan</div></a>
  <a class="card" href="farmers-market-playbook.html"><div class="t">Farmers-Market Playbook</div><div class="d">the validation phase + the WA TCS/cottage reality</div></a>
  <a class="card" href="water-activity-test-plan.html"><div class="t">Water-Activity Test Plan</div><div class="d">chasing the home-kitchen channel — email WSDA first</div></a>
  <a class="card" href="canele-cost.html"><div class="t">Canelé Cost per Unit</div><div class="d">~$0.45/canelé from a Seattle grocery, line by line</div></a>
  <a class="card" href="flavor-cost.html"><div class="t">Flavored Canelé Costs</div><div class="d">choco + tea flavors with real products; $0.38–$0.64/unit</div></a>
  <a class="card" href="combo-pricing.html"><div class="t">Combo Pricing</div><div class="d">coffee + canelé breakfast combo — math, breakeven, why it needs espresso</div></a>
  <a class="card" href="alcohol-in-pastry.html"><div class="t">Alcohol in Pastry</div><div class="d">WA rules (sub-1% = not "liquor") + non-alcoholic tea swaps</div></a>
  <a class="card" href="experiment-10pct-structure.html"><div class="t">Experiment: structure × cornstarch</div><div class="d">2×2 next-batch test — 10% structure, and do you need cornstarch?</div></a>
  <a class="card" href="brand__README.html"><div class="t">Brand Kit</div><div class="d">tokens, voice, the daily ritual</div></a>
</div>

<h2>Brand assets</h2>
<div class="assets">${assetCards}</div>
` + foot;
fs.writeFileSync(path.join(OUT,"index.html"), hub);

console.log("Built review hub:", path.relative(ROOT, path.join(OUT,"index.html")));
console.log("Pages:", docs.length+1, "| assets:", pngs.length);
