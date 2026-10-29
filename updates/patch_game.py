from pathlib import Path

p = Path("app/src/main/assets/index.html")
s = p.read_text(encoding="utf-8")

replacements = [
    (""".bar b{position:relative;font-size:9px;line-height:12px;padding-left:4px;font-weight:900;letter-spacing:.3px}""",
     """.bar b{position:relative;display:block;font-size:10px;line-height:12px;padding-left:4px;font-weight:1000;letter-spacing:.45px;color:#fff;text-shadow:1px 1px 2px #000, -1px -1px 1px #000;white-space:nowrap;z-index:1}"""),
    ("""<div class="bar hp" id="hpBar"><i id="hpFill"></i><b> <span id="hpTxt">100</span></b></div>""",
     """<div class="bar hp" id="hpBar"><i id="hpFill"></i><b>HEALTH <span id="hpTxt">100</span></b></div>"""),
    ("""FOOD <span id="foodTxt">100</span>""", """HUNGER <span id="foodTxt">100</span>"""),
    ("""WATER <span id="waterTxt">100</span>""", """THIRST <span id="waterTxt">100</span>"""),
    ("""let soundOn = true, audioCtx = null, keys = {}, joy = {x:0,y:0}, invSel = -1, craftTab = 'all', confirmNew = false;""",
     """let soundOn = true, audioCtx = null, keys = {}, joy = {x:0,y:0}, invSel = -1, craftTab = 'all', confirmNew = false, selectedRecipe = null;"""),
    ("""g.gain.setValueAtTime(vol,t0); g.gain.exponentialRampToValueAtTime(.001,t0+dur);""",
     """g.gain.setValueAtTime(Math.min(vol*2.2,0.22),t0); g.gain.exponentialRampToValueAtTime(.001,t0+dur);"""),
    ("""g.gain.value=vol; src.connect(f);""", """g.gain.value=Math.min(vol*2.2,0.22); src.connect(f);"""),
    ("""<button class="ibtn" id="soundToggle"></button>""",
     """<button class="ibtn" id="soundToggle" aria-label="Toggle sound" title="Toggle sound">♫</button>"""),
    ("""$('soundToggle').onclick = () => { soundOn=!soundOn; $('soundToggle').textContent=soundOn?'':'×'; if(soundOn){audio(); sfx('open');} say(soundOn?'Sound on':'Sound off'); };""",
     """$('soundToggle').textContent = soundOn ? '♫' : '×';
$('soundToggle').onclick = () => { soundOn=!soundOn; $('soundToggle').textContent=soundOn?'♫':'×'; $('soundToggle').setAttribute('aria-label',soundOn?'Mute sound':'Enable sound'); if(soundOn){audio(); sfx('open');} say(soundOn?'Sound on':'Sound off'); };"""),
    ("""h+=`<div class="near">Nearby: ${['workbench','furnace','cook'].map(t=>STATION_NAME[t]+(near[t]?' ':' ')).join(' ')}</div><div class="rgrid">`;""",
     """h+=`<div class="near">Tap a recipe to inspect ingredients first. Hand recipes work anywhere; other recipes need the named station within 3 tiles. Nearby: ${['workbench','furnace','cook'].map(t=>STATION_NAME[t]+(near[t]?' ✓':' ✕')).join(' · ')}</div><div class="rgrid">`;""")
]
for old, new in replacements:
    if old not in s:
        print("NOTE: source pattern not found; skipped:", old[:70])
    else:
        s = s.replace(old, new, 1)

craft_end = """ body.innerHTML=h+'</div>';
 } else if (modal==='chest'){"""
detail = """ if (selectedRecipe !== null && RECIPES[selectedRecipe]) {
  const r=RECIPES[selectedRecipe], st=r.st||'hand', d=ITEMS[r.id], ready=canCraft(r,near);
  const ingredients=Object.entries(r.cost).map(([id,n])=>{const have=countItem(id);return `<div class="ingredient"><span>${iconImg(id)} ${ITEMS[id].n}</span><b class="${have<n?'no':''}">${have} / ${n}</b></div>`;}).join('');
  h+=`<div class="recipe-detail"><div class="detail"><span class="big">${iconImg(r.id)}</span><span class="txt"><b>${d.n}${r.n>1?' ×'+r.n:''}</b><br>${st==='hand'?'Hand crafting — available anywhere':'Station required: '+STATION_NAME[st]}</span></div><div class="sec">REQUIRED INGREDIENTS</div><div class="ingredients">${ingredients}</div><button class="pbtn ${ready?'':'alt'}" data-craft-selected="${selectedRecipe}" style="width:100%;margin-top:8px">${ready?'CRAFT '+d.n.toUpperCase():'Missing ingredients or station'}</button></div>`;
 }
 body.innerHTML=h+'</div>';
 } else if (modal==='chest'){"""
if craft_end in s:
    s=s.replace(craft_end, detail, 1)
else:
    print("NOTE: craft detail insertion point not found")

old_click = """ if (b.dataset.r!=null){
 const r=RECIPES[+b.dataset.r], near=nearStations(), st=r.st||'hand';
 if (!near[st]){ say('Needs a '+STATION_NAME[st]+' within 3 tiles'); sfx('error'); return; }
 if (!canCraft(r,near)){ say('Not enough materials'); sfx('error'); return; }
 for (const id in r.cost) removeItem(id,r.cost[id]);
 const left=addItem(r.id,r.n||1); if (r.ret) for (const id in r.ret) addItem(id,r.ret[id]);
 stat('craft_'+r.id); stat('got_'+r.id,r.n||1); if(st==='cook') stat('cooked');
 gainXp(2); sfx('craft'); say('Crafted '+ITEMS[r.id].n+(left?' (bag full!)':'')); renderModal(); return;
 }"""
new_click = """ if (b.dataset.r!=null){
  selectedRecipe=+b.dataset.r; sfx('open'); renderModal(); return;
 }
 if (b.dataset.craftSelected!=null){
  const r=RECIPES[+b.dataset.craftSelected], near=nearStations(), st=r.st||'hand';
  if (!near[st]){ say('Needs a '+STATION_NAME[st]+' within 3 tiles'); sfx('error'); return; }
  if (!canCraft(r,near)){ say('Not enough materials'); sfx('error'); return; }
  for (const id in r.cost) removeItem(id,r.cost[id]);
  const left=addItem(r.id,r.n||1); if (r.ret) for (const id in r.ret) addItem(id,r.ret[id]);
  stat('craft_'+r.id); stat('got_'+r.id,r.n||1); if(st==='cook') stat('cooked');
  gainXp(2); sfx('craft'); say('Crafted '+ITEMS[r.id].n+(left?' (bag full!)':'')); selectedRecipe=null; renderModal(); return;
 }"""
if old_click in s:
    s=s.replace(old_click, new_click, 1)
else:
    print("NOTE: craft click handler pattern not found")

s=s.replace('.rcp.off{opacity:.55;filter:saturate(.4)}',
            '.rcp.off{opacity:.75;filter:saturate(.4)}\n.recipe-detail{margin-top:10px;padding:9px;background:#efe0bb;border:2px solid #b69663;border-radius:8px;color:#34452c}.ingredients{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:5px}.ingredient{display:flex;align-items:center;justify-content:space-between;gap:5px;background:#fff6de;border:1px solid #c5a36a;border-radius:5px;padding:4px;font-size:11px;font-weight:800}.ingredient span{display:flex;align-items:center;gap:5px}.ingredient img{width:24px;height:24px;object-fit:contain;image-rendering:pixelated}.ingredient .no{color:#b8342c}')
p.write_text(s, encoding="utf-8")
print("Wildwood HUD, crafting details, ingredient images, and louder sound patch applied.")

# Mobile UI polish: larger close control, scrollable recipe panel, and sleep overlay.
s = s.replace(
    '#mclose{border:0;background:#8b613b;color:#fff;width:32px;height:30px;border-radius:6px;font-size:16px;font-weight:900}',
    '#mclose{display:flex;align-items:center;justify-content:center;flex:0 0 38px;min-width:38px;height:38px;border:2px solid #f5dfad;background:#8b352d;color:#fff;border-radius:8px;font-size:28px;line-height:1;font-weight:1000;box-shadow:0 2px 0 #512a20;z-index:5}'
)
s = s.replace('.modal{width:min(580px,100%);max-height:96%;',
              '.modal{width:min(580px,100%);max-height:88dvh;')
s = s.replace('#mbody{overflow:auto;padding:8px 10px 10px;font-size:12px;',
              '#mbody{overflow:auto;overscroll-behavior:contain;padding:8px 10px 10px;font-size:12px;')
s = s.replace('.recipe-detail{margin-top:10px;',
              '.recipe-detail{position:sticky;bottom:0;z-index:3;margin-top:10px;')
s = s.replace("function closeModal(){ if(modal==='death') return; modal=null;",
              "function closeModal(){ if(modal==='death') return; selectedRecipe=null; modal=null;")
s = s.replace("selectedRecipe=+b.dataset.r; sfx('open'); renderModal(); return;",
              "selectedRecipe=+b.dataset.r; sfx('open'); renderModal(); requestAnimationFrame(()=>document.querySelector('.recipe-detail')?.scrollIntoView({behavior:'smooth',block:'nearest'})); return;")

if 'id="sleepFx"' not in s:
    s = s.replace('<div class="modalwrap" id="modalwrap">',
        '<div id="sleepFx" aria-hidden="true"><div class="sleep-card"><div class="sleep-bed">🛏️</div><div class="sleep-person">●━━━━</div><b>Sleeping...</b><div class="sleep-stars">✦ ⋆ ✦</div></div></div><div class="modalwrap" id="modalwrap">', 1)
    sleep_css = '#sleepFx{position:absolute;inset:0;display:none;align-items:center;justify-content:center;background:#071326b8;z-index:30;pointer-events:none}#sleepFx.show{display:flex;animation:nightFade 1.6s ease-in-out forwards}.sleep-card{position:relative;text-align:center;padding:20px 28px;border:3px solid #d9bd7b;border-radius:12px;background:#213047;color:#fff2c7;box-shadow:0 6px 0 #111b2a;min-width:190px}.sleep-bed{font-size:44px;animation:bedRock .65s ease-in-out infinite alternate}.sleep-person{font-size:22px;letter-spacing:1px;animation:lieDown .65s ease-in-out forwards}.sleep-stars{font-size:18px;color:#ffe28a;animation:starsTwinkle .6s infinite alternate}@keyframes lieDown{from{transform:rotate(-25deg) translateY(-5px)}to{transform:rotate(0) translateY(3px)}}@keyframes bedRock{from{transform:rotate(-2deg)}to{transform:rotate(2deg)}}@keyframes starsTwinkle{from{opacity:.35;transform:translateY(2px)}to{opacity:1;transform:translateY(-3px)}}@keyframes nightFade{0%{opacity:0}12%{opacity:1}75%{opacity:1}100%{opacity:0}}'
    s = s.replace('</style>', sleep_css + '</style>', 1)
sleep_before = 'if (S.time>.06) S.day++;'
sleep_after = "const sleepFx=document.getElementById('sleepFx');if(sleepFx){sleepFx.classList.remove('show');void sleepFx.offsetWidth;sleepFx.classList.add('show');setTimeout(()=>sleepFx.classList.remove('show'),1650);} if (S.time>.06) S.day++;"
if sleep_before in s and 'sleepFx.classList.add' not in s:
    s = s.replace(sleep_before, sleep_after, 1)

p.write_text(s, encoding='utf-8')
print("Wildwood patch complete.")


# Final mobile crafting layout and visible combat feedback.
s = s.replace(
    '.modalwrap{position:absolute;inset:0;display:none;align-items:center;justify-content:center;background:#0b1712b0;padding:8px;z-index:20}',
    '.modalwrap{position:absolute;inset:0;display:none;align-items:flex-end;justify-content:flex-start;background:#0b17127a;padding:8px;z-index:20;pointer-events:auto}'
)
s = s.replace(
    '.modal{width:min(580px,100%);max-height:96%;display:flex;flex-direction:column;background:var(--panel);color:var(--ink);border:4px solid var(--wood);border-radius:10px;box-shadow:0 6px 0 #422d1f;text-shadow:none}',
    '.modal{width:min(370px,42vw);max-height:78dvh;display:flex;flex-direction:column;background:var(--panel);color:var(--ink);border:3px solid var(--wood);border-radius:10px;box-shadow:0 4px 0 #422d1f;text-shadow:none}'
)
s = s.replace(
    '#mclose{border:0;background:#8b613b;color:#fff;width:32px;height:30px;border-radius:6px;font-size:16px;font-weight:900}',
    '#mclose{position:relative;display:flex!important;align-items:center;justify-content:center;flex:0 0 34px;width:34px;height:34px;border:2px solid #fff0c7!important;background:#a52d27!important;color:#fff!important;border-radius:7px;font-size:0!important;font-weight:1000;box-shadow:0 2px 0 #512a20;z-index:30}#mclose:before{content:"×";display:block;color:#fff;font-size:30px;line-height:26px;font-family:Arial,sans-serif;text-shadow:0 1px 2px #35100d}'
)
s = s.replace(
    '.mhead{display:flex;align-items:center;justify-content:space-between;padding:6px 10px;border-bottom:2px solid #d8c49a}',
    '.mhead{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:5px 8px;border-bottom:2px solid #d8c49a;min-height:40px;flex-shrink:0}'
)
s = s.replace(
    '#mbody{overflow:auto;padding:8px 10px 10px;font-size:12px;-webkit-overflow-scrolling:touch;touch-action:pan-y}',
    '#mbody{overflow:auto;min-height:0;padding:6px 7px 8px;font-size:11px;-webkit-overflow-scrolling:touch;touch-action:pan-y}'
)
# Keep detail visible and size the crafting list for the smaller side panel.
s = s.replace('.rgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:5px}',
              '.rgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px}')
s = s.replace('.rcp{', '.rcp{font-size:10px;min-width:0;')
s = s.replace('.recipe-detail{margin-top:10px;', '.recipe-detail{margin-top:6px;')
# On portrait phones, use a compact panel near the left/bottom edge instead of a centered full-screen modal.
if '@media (orientation:portrait)' not in s:
    s = s.replace('</style>',
        '@media (orientation:portrait){.modalwrap{align-items:flex-end;justify-content:flex-start;padding:6px}.modal{width:min(88vw,370px);max-height:68dvh}.rgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.mhead h2{font-size:15px}}@media (max-height:420px){.modal{max-height:72dvh;width:min(350px,40vw)}}\n</style>', 1)
# Make the arm/tool swing last a little longer and use a wider arc.
s = s.replace('swingT = .25;', 'swingT = .34;')
s = s.replace('const k=swingT>0?swingT/.25:0; ctx.rotate((P.fx<0?1:-1)*(k*1.8-.3));',
              'const k=swingT>0?swingT/.34:0; ctx.rotate((P.fx<0?1:-1)*(k*2.35-.48));')
# Stronger hit feedback so the player can see when an attack lands.
s = s.replace("burst(m.x,m.y,m.t==='hollow'?'#6a5a8a':'#b03030',5,50);",
              "burst(m.x,m.y,m.t==='hollow'?'#6a5a8a':'#b03030',9,72); shake=Math.max(shake,2.5);")
p.write_text(s, encoding='utf-8')
print("Applied compact edge-anchored crafting UI, visible close icon, and stronger swing/hit feedback.")
