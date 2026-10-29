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


# User-requested correction: keep the recipe requirements attached to the edge panel,
# never as a centered/sticky overlay, and force a visible close glyph.
mobile_edge_css = r"""
.modalwrap{
  align-items:flex-start!important;
  justify-content:flex-start!important;
  padding:8px!important;
  background:rgba(7,17,11,.38)!important;
}
.modal{
  width:min(350px,42vw)!important;
  max-width:calc(100vw - 16px)!important;
  max-height:78dvh!important;
  margin:0!important;
}
.mhead{
  min-height:44px!important;
  flex-shrink:0!important;
  padding:5px 8px!important;
  gap:8px!important;
}
.mhead h2{font-size:18px!important;margin:0!important}
#mclose{
  display:flex!important;
  align-items:center!important;
  justify-content:center!important;
  flex:0 0 34px!important;
  width:34px!important;
  min-width:34px!important;
  height:34px!important;
  padding:0!important;
  border:2px solid #fff0c7!important;
  border-radius:7px!important;
  background:#a52d27!important;
  color:#fff!important;
  font-size:0!important;
  line-height:1!important;
  position:relative!important;
  z-index:100!important;
}
#mclose::before,#mclose::after{content:none!important;display:none!important}
#mclose{font-size:0!important}
#mclose:after{
  content:"×"!important;
  display:block!important;
  color:#fff!important;
  font:1000 30px/26px Arial,sans-serif!important;
  text-shadow:0 1px 2px #35100d!important;
}
#mbody{
  min-height:0!important;
  max-height:calc(78dvh - 52px)!important;
  overflow:auto!important;
  padding:6px 7px 8px!important;
  font-size:11px!important;
  overscroll-behavior:contain!important;
}
.rgrid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:4px!important}
.recipe-detail{
  position:static!important;
  inset:auto!important;
  width:auto!important;
  max-height:none!important;
  overflow:visible!important;
  margin:8px 0 0!important;
  padding:7px!important;
  box-shadow:none!important;
}
.recipe-detail .detail{gap:6px!important}
.recipe-detail .big img{width:30px!important;height:30px!important}
.ingredients{grid-template-columns:1fr!important;gap:4px!important}
.ingredient{padding:4px!important;font-size:10px!important}
.ingredient img{width:20px!important;height:20px!important}
.recipe-detail button{min-height:36px!important;padding:7px!important;font-size:11px!important}
@media (orientation:portrait){
  .modalwrap{align-items:flex-start!important;justify-content:flex-start!important}
  .modal{width:min(88vw,350px)!important;max-height:66dvh!important}
  #mbody{max-height:calc(66dvh - 52px)!important}
}
@media (max-height:420px){
  .modal{max-height:72dvh!important;width:min(320px,40vw)!important}
  #mbody{max-height:calc(72dvh - 52px)!important}
}
"""
if '</style>' in s:
    s = s.replace('</style>', mobile_edge_css + '\\n</style>', 1)
else:
    print("NOTE: could not find style closing tag for edge layout patch")
p.write_text(s, encoding='utf-8')
print("Crafting requirements are now in the compact edge panel flow; close icon forced visible.")


# Restore original-size centered crafting panel and add a sword icon overlay.
restore_css = r"""
.modalwrap{align-items:center!important;justify-content:center!important;padding:8px!important;background:rgba(7,17,11,.55)!important}
.modal{width:min(580px,92vw)!important;max-width:calc(100vw - 16px)!important;max-height:88dvh!important;margin:auto!important;border-width:4px!important}
.mhead{min-height:54px!important;flex-shrink:0!important;padding:8px 12px!important;gap:10px!important}
.mhead h2{font-size:22px!important;margin:0!important}
#mclose{display:flex!important;align-items:center!important;justify-content:center!important;flex:0 0 42px!important;width:42px!important;min-width:42px!important;height:42px!important;padding:0!important;border:2px solid #fff0c7!important;border-radius:8px!important;background:#a52d27!important;color:#fff!important;font-size:0!important;position:relative!important;z-index:100!important}
#mclose:after{content:"×"!important;display:block!important;color:#fff!important;font:1000 34px/30px Arial,sans-serif!important;text-shadow:0 1px 2px #35100d!important}
#mbody{min-height:0!important;max-height:calc(88dvh - 62px)!important;overflow:auto!important;padding:10px 12px 12px!important;font-size:13px!important;overscroll-behavior:contain!important}
.rgrid{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:6px!important}
.recipe-detail{position:static!important;inset:auto!important;width:auto!important;max-height:none!important;overflow:visible!important;margin:10px 0 0!important;padding:10px!important;box-shadow:none!important}
.recipe-detail .detail{gap:10px!important}
.recipe-detail .big img{width:42px!important;height:42px!important}
.ingredients{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:6px!important}
.ingredient{padding:6px!important;font-size:12px!important}
.ingredient img{width:28px!important;height:28px!important}
.recipe-detail button{min-height:46px!important;padding:10px!important;font-size:14px!important}
#attackIconOverlay{position:fixed;right:5.5%;bottom:8.5%;width:64px;height:64px;z-index:15;pointer-events:none;background:url("icons/sword.svg") center/contain no-repeat;image-rendering:pixelated;filter:drop-shadow(1px 2px 2px #17120d)}
@media (orientation:portrait){.modal{width:min(92vw,580px)!important;max-height:86dvh!important}#mbody{max-height:calc(86dvh - 62px)!important}.rgrid{grid-template-columns:repeat(2,minmax(0,1fr))!important}#attackIconOverlay{right:5%;bottom:9%;width:56px;height:56px}}
@media (max-height:420px){.modal{max-height:86dvh!important}#mbody{max-height:calc(86dvh - 62px)!important}#attackIconOverlay{width:44px;height:44px}}
"""
if '</style>' in s:
    s = s.replace('</style>', restore_css + '\n</style>', 1)
else:
    print("WARNING: style tag not found; crafting CSS not applied")
if 'id="attackIconOverlay"' not in s:
    if '<body' in s:
        body_end = s.find('>', s.find('<body'))
        s = s[:body_end+1] + '\n<div id="attackIconOverlay" aria-hidden="true"></div>\n' + s[body_end+1:]
    else:
        print("WARNING: body tag not found; attack icon overlay not inserted")
p.write_text(s, encoding='utf-8')
print("Restored centered crafting layout and added sword icon overlay.")


# Final crafting layout fix: make the selected recipe panel span the available
# right-side columns and keep ingredient names/counts on one readable line.
readable_crafting_css = r"""
.modal{width:min(760px,94vw)!important;max-width:calc(100vw - 16px)!important;max-height:90dvh!important}
#mbody{max-height:calc(90dvh - 62px)!important;padding:12px 14px 14px!important;font-size:14px!important}
.rgrid{grid-template-columns:repeat(3,minmax(0,1fr))!important;align-items:start!important;gap:8px!important}
.recipe-detail{grid-column:2 / -1!important;grid-row:1 / span 20!important;min-width:0!important;width:100%!important;box-sizing:border-box!important;margin:0!important;padding:12px!important;overflow:visible!important}
.recipe-detail .detail{display:flex!important;align-items:center!important;gap:12px!important;min-width:0!important}
.recipe-detail .txt{min-width:0!important;font-size:15px!important;line-height:1.35!important;overflow-wrap:anywhere!important}
.recipe-detail .big img{width:48px!important;height:48px!important;object-fit:contain!important}
.recipe-detail .sec{font-size:14px!important;letter-spacing:.8px!important;margin:12px 0 7px!important}
.ingredients{display:flex!important;flex-direction:column!important;gap:7px!important;width:100%!important;min-width:0!important}
.ingredient{display:flex!important;align-items:center!important;justify-content:space-between!important;gap:10px!important;width:100%!important;min-width:0!important;box-sizing:border-box!important;padding:8px 10px!important;font-size:14px!important;line-height:1.25!important;white-space:normal!important}
.ingredient span{display:flex!important;align-items:center!important;gap:8px!important;min-width:0!important;flex:1 1 auto!important;overflow-wrap:anywhere!important}
.ingredient span img{width:30px!important;height:30px!important;flex:0 0 30px!important;object-fit:contain!important}
.ingredient b{flex:0 0 auto!important;white-space:nowrap!important;font-size:14px!important;line-height:1.2!important;margin-left:auto!important}
.recipe-detail button{min-height:50px!important;font-size:15px!important;white-space:normal!important;line-height:1.25!important}
#attackIconOverlay{position:fixed!important;right:6.1%!important;bottom:11%!important;width:58px!important;height:58px!important;background:url("icons/sword.svg") center/78% 78% no-repeat!important;transform:rotate(-8deg)!important;filter:drop-shadow(2px 2px 1px #17120d)!important;pointer-events:none!important}
@media (orientation:portrait){
 .modal{width:94vw!important;max-height:88dvh!important}
 #mbody{max-height:calc(88dvh - 62px)!important}
 .rgrid{grid-template-columns:minmax(0,1fr) minmax(0,1.35fr)!important}
 .recipe-detail{grid-column:2!important;grid-row:1 / span 30!important}
 .rcp{font-size:12px!important;padding:6px!important}
 .ingredient{padding:7px 8px!important;font-size:13px!important}
 .ingredient b{font-size:13px!important}
 #attackIconOverlay{right:6.5%!important;bottom:11%!important;width:54px!important;height:54px!important}
}
@media (max-height:420px){
 .modal{max-height:88dvh!important}
 #mbody{max-height:calc(88dvh - 62px)!important}
 .recipe-detail .big img{width:38px!important;height:38px!important}
}
"""
if '</style>' in s:
    s = s.replace('</style>', readable_crafting_css + '\\n</style>', 1)
else:
    print("WARNING: could not append readable crafting CSS")
p.write_text(s, encoding='utf-8')
print("Fixed clipped ingredient counts, expanded crafting panel, and refined sword icon.")


# Put the crafting UI at the bottom of the screen as requested, with a large,
# readable panel that respects the phone's safe area.
bottom_crafting_css = r"""
.modalwrap{
  align-items:flex-end!important;
  justify-content:center!important;
  padding:8px 8px max(8px,env(safe-area-inset-bottom))!important;
}
.modal{
  width:min(760px,94vw)!important;
  max-width:calc(100vw - 16px)!important;
  max-height:76dvh!important;
  margin:0 auto!important;
  border-radius:16px 16px 12px 12px!important;
}
.mhead{min-height:52px!important;padding:7px 12px!important}
.mhead h2{font-size:22px!important}
#mbody{max-height:calc(76dvh - 60px)!important;padding:10px 12px max(12px,env(safe-area-inset-bottom))!important}
.rgrid{align-items:start!important}
.recipe-detail{max-height:none!important;overflow:visible!important}
.ingredients{display:flex!important;flex-direction:column!important;gap:7px!important}
.ingredient{display:flex!important;align-items:center!important;justify-content:space-between!important;gap:10px!important;min-width:0!important;width:100%!important;box-sizing:border-box!important;padding:8px 10px!important;font-size:14px!important;line-height:1.3!important}
.ingredient span{display:flex!important;align-items:center!important;gap:8px!important;min-width:0!important;flex:1 1 auto!important;overflow-wrap:anywhere!important}
.ingredient b{flex:0 0 auto!important;white-space:nowrap!important;font-size:14px!important;margin-left:auto!important}
.recipe-detail button{min-height:48px!important;font-size:14px!important}
@media (orientation:portrait){
 .modal{width:94vw!important;max-height:72dvh!important}
 #mbody{max-height:calc(72dvh - 60px)!important}
 .rgrid{grid-template-columns:minmax(0,1fr) minmax(0,1.35fr)!important}
 .recipe-detail{grid-column:2!important;grid-row:1 / span 30!important}
}
@media (max-height:420px){
 .modal{max-height:70dvh!important}
 #mbody{max-height:calc(70dvh - 60px)!important}
}
"""
if '</style>' in s:
    s = s.replace('</style>', bottom_crafting_css + '\\n</style>', 1)
else:
    print("WARNING: style tag not found for bottom crafting layout")
p.write_text(s, encoding='utf-8')
print("Moved crafting panel to bottom and kept ingredient counts readable.")


# Definitive bottom-anchored crafting layout: prevent any earlier CSS overrides
# from pulling the panel back to the top, and use a compact but readable height.
bottom_final_css = r"""
.modalwrap{
 position:absolute!important;inset:0!important;display:none;align-items:flex-end!important;
 justify-content:center!important;padding:8px 8px max(8px,env(safe-area-inset-bottom))!important;
 box-sizing:border-box!important;
}
.modalwrap[style*="display: flex"],.modalwrap[style*="display:flex"]{
 align-items:flex-end!important;justify-content:center!important;
}
.modal{
 width:min(760px,94vw)!important;max-width:calc(100vw - 16px)!important;
 max-height:64dvh!important;margin:0 auto 0!important;
 border-radius:14px 14px 10px 10px!important;
}
.mhead{min-height:46px!important;padding:6px 10px!important;flex-shrink:0!important}
.mhead h2{font-size:20px!important;line-height:1.15!important}
#mbody{
 max-height:calc(64dvh - 54px)!important;min-height:0!important;
 overflow:auto!important;overscroll-behavior:contain!important;
 padding:8px 10px max(10px,env(safe-area-inset-bottom))!important;
}
.rgrid{gap:6px!important;align-items:start!important}
.recipe-detail{
 position:static!important;top:auto!important;bottom:auto!important;
 max-height:none!important;overflow:visible!important;margin:0!important;
 padding:9px!important;box-sizing:border-box!important;
}
.ingredients{display:flex!important;flex-direction:column!important;gap:6px!important;width:100%!important}
.ingredient{
 display:flex!important;align-items:center!important;justify-content:space-between!important;
 width:100%!important;min-width:0!important;box-sizing:border-box!important;
 padding:7px 9px!important;font-size:13px!important;line-height:1.25!important;
}
.ingredient span{min-width:0!important;flex:1 1 auto!important;overflow-wrap:anywhere!important}
.ingredient b{flex:0 0 auto!important;white-space:nowrap!important;font-size:13px!important}
.recipe-detail button{min-height:44px!important;font-size:14px!important}
@media (orientation:portrait){
 .modal{width:94vw!important;max-height:62dvh!important}
 #mbody{max-height:calc(62dvh - 54px)!important}
 .rgrid{grid-template-columns:minmax(0,1fr) minmax(0,1.25fr)!important}
 .recipe-detail{grid-column:2!important;grid-row:1 / span 40!important}
}
@media (max-height:420px){
 .modal{max-height:58dvh!important}
 #mbody{max-height:calc(58dvh - 54px)!important}
}
"""
if '</style>' in s:
    s = s.replace('</style>', bottom_final_css + '\\n</style>', 1)
p.write_text(s, encoding='utf-8')
print("Forced crafting UI to bottom with a more compact height and readable ingredient counts.")


# Scope the bottom-sheet layout ONLY to the crafting modal (identified by its
# recipe grid). All other dialogs keep their normal centered placement.
crafting_only_bottom_sheet = r"""
/* Reset generic dialogs so inventory, sleep, death, and settings are unaffected. */
.modalwrap{
 position:absolute!important;inset:0!important;
 align-items:center!important;justify-content:center!important;
 padding:8px!important;box-sizing:border-box!important;
 background:#07130eb0!important;
}
/* Only the crafting modal slides up from the bottom when the recipe grid exists. */
.modalwrap:has(.rgrid){
 align-items:flex-end!important;justify-content:center!important;
 padding:8px 8px max(8px,env(safe-area-inset-bottom))!important;
 background:linear-gradient(180deg,rgba(4,12,8,.05),rgba(4,12,8,.48))!important;
}
.modalwrap:has(.rgrid) .modal{
 width:min(720px,94vw)!important;max-width:calc(100vw - 16px)!important;
 height:auto!important;max-height:46dvh!important;min-height:0!important;
 margin:0 auto!important;overflow:hidden!important;
 border:3px solid #d0ae70!important;border-radius:16px 16px 10px 10px!important;
 box-shadow:0 5px 0 #503522,0 12px 30px #07100b88!important;
 animation:craftSheetIn .18s ease-out both!important;
}
.modalwrap:has(.rgrid) .mhead{
 min-height:44px!important;padding:6px 10px!important;
 background:linear-gradient(135deg,#fff3d0,#f0d9a8)!important;
 border-bottom:2px solid #d2b77f!important;
}
.modalwrap:has(.rgrid) .mhead h2{font-size:19px!important;line-height:1.1!important;letter-spacing:.2px!important}
.modalwrap:has(.rgrid) #mclose{
 width:36px!important;min-width:36px!important;height:36px!important;flex-basis:36px!important;
 border-radius:10px!important;background:#a52d27!important;border:2px solid #ffe7b0!important;
 font-size:0!important;box-shadow:0 2px 0 #572a20!important;
}
.modalwrap:has(.rgrid) #mclose:after{content:"×"!important;font:1000 29px/28px Arial,sans-serif!important;color:#fff!important}
.modalwrap:has(.rgrid) #mbody{
 max-height:calc(46dvh - 50px)!important;min-height:0!important;
 overflow:auto!important;padding:8px 9px max(10px,env(safe-area-inset-bottom))!important;
 font-size:12px!important;overscroll-behavior:contain!important;
}
.modalwrap:has(.rgrid) .rgrid{
 display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;
 gap:6px!important;align-items:start!important;
}
.modalwrap:has(.rgrid) .rcp{
 min-width:0!important;padding:6px!important;border-radius:8px!important;
 font-size:11px!important;line-height:1.2!important;
}
.modalwrap:has(.rgrid) .recipe-detail{
 grid-column:1 / -1!important;grid-row:auto!important;
 position:static!important;inset:auto!important;min-width:0!important;width:100%!important;
 max-height:none!important;overflow:visible!important;margin:2px 0 0!important;padding:9px!important;
 border:2px solid #b99a62!important;border-radius:11px!important;
 background:linear-gradient(135deg,#f8e9c5,#efdbad)!important;
 box-sizing:border-box!important;
}
.modalwrap:has(.rgrid) .recipe-detail .detail{display:flex!important;align-items:center!important;gap:8px!important;min-width:0!important}
.modalwrap:has(.rgrid) .recipe-detail .big img{width:36px!important;height:36px!important;object-fit:contain!important}
.modalwrap:has(.rgrid) .recipe-detail .txt{font-size:13px!important;line-height:1.25!important;min-width:0!important;overflow-wrap:anywhere!important}
.modalwrap:has(.rgrid) .recipe-detail .sec{font-size:11px!important;letter-spacing:.7px!important;margin:7px 0 5px!important}
.modalwrap:has(.rgrid) .ingredients{display:flex!important;flex-direction:column!important;gap:4px!important;width:100%!important;min-width:0!important}
.modalwrap:has(.rgrid) .ingredient{
 display:flex!important;align-items:center!important;justify-content:space-between!important;
 gap:7px!important;width:100%!important;min-width:0!important;box-sizing:border-box!important;
 padding:5px 7px!important;border-radius:7px!important;font-size:12px!important;line-height:1.2!important;
}
.modalwrap:has(.rgrid) .ingredient span{display:flex!important;align-items:center!important;gap:6px!important;flex:1 1 auto!important;min-width:0!important;overflow-wrap:anywhere!important}
.modalwrap:has(.rgrid) .ingredient img,.modalwrap:has(.rgrid) .ingredient span img{width:24px!important;height:24px!important;flex:0 0 24px!important;object-fit:contain!important}
.modalwrap:has(.rgrid) .ingredient b{flex:0 0 auto!important;white-space:nowrap!important;font-size:12px!important;margin-left:auto!important}
.modalwrap:has(.rgrid) .recipe-detail button{min-height:40px!important;padding:7px 9px!important;font-size:13px!important;line-height:1.2!important}
@keyframes craftSheetIn{from{transform:translateY(16px);opacity:.7}to{transform:translateY(0);opacity:1}}
@media (orientation:portrait){
 .modalwrap:has(.rgrid) .modal{width:94vw!important;max-height:48dvh!important}
 .modalwrap:has(.rgrid) #mbody{max-height:calc(48dvh - 50px)!important}
 .modalwrap:has(.rgrid) .rgrid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
 .modalwrap:has(.rgrid) .recipe-detail{grid-column:1 / -1!important;grid-row:auto!important}
}
@media (max-height:420px){
 .modalwrap:has(.rgrid) .modal{max-height:52dvh!important}
 .modalwrap:has(.rgrid) #mbody{max-height:calc(52dvh - 50px)!important}
 .modalwrap:has(.rgrid) .mhead{min-height:38px!important}
 .modalwrap:has(.rgrid) #mclose{width:30px!important;min-width:30px!important;height:30px!important;flex-basis:30px!important}
}
"""
if '</style>' in s:
    s = s.replace('</style>', crafting_only_bottom_sheet + '\\n</style>', 1)
p.write_text(s, encoding='utf-8')
print("Scoped compact bottom-sheet styling to crafting only; other dialogs remain centered.")


# Adventurer's Pouch-inspired inventory theme. Keep the real game inventory/data
# and actions; only restyle the existing inventory dialog (no fake demo items).
pouch_inventory_css = r"""
.modalwrap.pouch-theme{align-items:center!important;justify-content:center!important;padding:10px!important;background:rgba(9,8,5,.76)!important}
.modalwrap.pouch-theme .modal{
 width:min(680px,94vw)!important;max-width:calc(100vw - 16px)!important;
 max-height:82dvh!important;overflow:hidden!important;
 color:#fff5d8!important;background:#6a4a2c!important;
 border:4px solid #3b2812!important;border-radius:10px!important;
 box-shadow:inset 0 0 0 3px #8a6339,0 12px 34px #000b!important;
}
.modalwrap.pouch-theme .mhead{
 background:linear-gradient(#7a5733,#5e4126)!important;
 border-bottom:3px solid #3b2812!important;color:#f6c619!important;
 min-height:48px!important;padding:7px 10px!important;
}
.modalwrap.pouch-theme .mhead h2,.modalwrap.pouch-theme .mhead b{
 color:#f6c619!important;text-shadow:2px 2px 0 #3b2000!important;letter-spacing:.04em!important;
}
.modalwrap.pouch-theme #mclose{
 display:flex!important;align-items:center!important;justify-content:center!important;
 width:38px!important;min-width:38px!important;height:38px!important;flex:0 0 38px!important;
 background:#b02a2a!important;color:#fff!important;border:3px solid #3b0d0d!important;
 border-radius:5px!important;font-size:25px!important;line-height:1!important;
}
.modalwrap.pouch-theme #mbody{
 max-height:calc(82dvh - 54px)!important;overflow:auto!important;
 background:#c9a46a!important;color:#fff5d8!important;padding:9px!important;
}
.modalwrap.pouch-theme .igrid,
.modalwrap.pouch-theme .invgrid,
.modalwrap.pouch-theme .inv-grid,
.modalwrap.pouch-theme .inventory-grid,
.modalwrap.pouch-theme .itemgrid,
.modalwrap.pouch-theme .item-grid{
 display:grid!important;grid-template-columns:repeat(6,minmax(0,1fr))!important;
 gap:clamp(4px,1.3vw,8px)!important;padding:8px!important;margin:0 0 9px!important;
 background:#d1b07a!important;border:3px solid #8a6339!important;border-radius:5px!important;
}
.modalwrap.pouch-theme .slot,
.modalwrap.pouch-theme .invslot,
.modalwrap.pouch-theme .inv-slot,
.modalwrap.pouch-theme .item-slot,
.modalwrap.pouch-theme .invitem{
 min-width:0!important;aspect-ratio:1!important;position:relative!important;
 display:grid!important;place-items:center!important;
 background:#2b2118!important;border:3px solid #777!important;border-radius:5px!important;
 box-shadow:inset 0 0 0 2px #0006!important;padding:2px!important;
}
.modalwrap.pouch-theme .slot.sel,
.modalwrap.pouch-theme .slot.selected,
.modalwrap.pouch-theme .invslot.sel,
.modalwrap.pouch-theme .inv-slot.selected,
.modalwrap.pouch-theme .item-slot.selected{
 outline:3px solid #fff!important;outline-offset:1px!important;border-color:#f6c619!important;
}
.modalwrap.pouch-theme .slot img,
.modalwrap.pouch-theme .invslot img,
.modalwrap.pouch-theme .inv-slot img,
.modalwrap.pouch-theme .item-slot img,
.modalwrap.pouch-theme .invitem img{width:70%!important;height:70%!important;object-fit:contain!important;image-rendering:pixelated!important}
.modalwrap.pouch-theme .q,
.modalwrap.pouch-theme .qty,
.modalwrap.pouch-theme .count,
.modalwrap.pouch-theme .stack{
 position:absolute!important;right:3px!important;bottom:1px!important;
 color:#fff!important;font-weight:900!important;text-shadow:1px 1px 2px #000!important;
}
.modalwrap.pouch-theme .det,
.modalwrap.pouch-theme .item-detail,
.modalwrap.pouch-theme .inv-detail,
.modalwrap.pouch-theme .details{
 margin:8px 0!important;background:#33261a!important;border:3px solid #6a4a2c!important;
 border-radius:6px!important;padding:10px!important;color:#fff5d8!important;
}
.modalwrap.pouch-theme .det .lab,
.modalwrap.pouch-theme .item-detail .lab{
 color:#f6c619!important;background:#6a4a2c!important;
}
.modalwrap.pouch-theme button{touch-action:manipulation}
@media(max-width:420px){
 .modalwrap.pouch-theme .modal{width:min(420px,88vw)!important;max-width:calc(100vw - 16px)!important;max-height:76dvh!important}
 .modalwrap.pouch-theme #mbody{max-height:calc(76dvh - 48px)!important;padding:7px!important}
 .modalwrap.pouch-theme .igrid,.modalwrap.pouch-theme .invgrid,.modalwrap.pouch-theme .inv-grid,
 .modalwrap.pouch-theme .inventory-grid,.modalwrap.pouch-theme .itemgrid,.modalwrap.pouch-theme .item-grid{gap:4px!important;padding:6px!important}
}
"""
if '</style>' in s:
    s = s.replace('</style>', pouch_inventory_css + '\\n</style>', 1)
else:
    print("WARNING: style tag not found; pouch inventory CSS skipped")

pouch_inventory_script = r"""
<script>
(function(){
  function themeInventory(){
    const wrap=document.getElementById('modalwrap');
    if(!wrap) return;
    wrap.classList.remove('pouch-theme');
    if(!wrap.offsetParent && getComputedStyle(wrap).display==='none') return;
    const modal=wrap.querySelector('.modal');
    const body=wrap.querySelector('#mbody');
    if(!modal||!body) return;
    const text=(modal.innerText||modal.textContent||'').toLowerCase();
    const isCraft=!!modal.querySelector('.rgrid');
    const isInventory=!isCraft && /inventory|backpack|adventurer.?s pouch|your bag|item details/.test(text);
    if(isInventory) wrap.classList.add('pouch-theme');
  }
  const start=()=> {
    const wrap=document.getElementById('modalwrap');
    if(wrap){
      new MutationObserver(()=>requestAnimationFrame(themeInventory))
        .observe(wrap,{subtree:true,childList:true,attributes:true,characterData:true});
      themeInventory();
    }
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',start,{once:true}); else start();
})();
</script>
"""
if '</body>' in s and 'function themeInventory()' not in s:
    s=s.replace('</body>', pouch_inventory_script + '\\n</body>',1)
p.write_text(s, encoding='utf-8')
print("Applied Adventurer's Pouch visual theme to the existing game inventory without replacing inventory data.")


# Compact bottom-sheet crafting layout; keep backpack styling unchanged.
compact_craft_css = r"""
.modalwrap:has(.rgrid){align-items:center!important;justify-content:center!important;padding:8px!important}
.modalwrap:has(.rgrid) .modal{width:min(420px,88vw)!important;max-width:calc(100vw - 16px)!important;max-height:76dvh!important;height:auto!important;margin:auto!important;overflow:hidden!important;border-radius:13px!important}
.modalwrap:has(.rgrid) .mhead{min-height:42px!important;padding:5px 9px!important}
.modalwrap:has(.rgrid) .mhead h2{font-size:clamp(16px,4.4vw,20px)!important;line-height:1.15!important}
.modalwrap:has(.rgrid) #mclose{width:34px!important;min-width:34px!important;height:34px!important;flex:0 0 34px!important;font-size:0!important}
.modalwrap:has(.rgrid) #mclose:after{content:"×"!important;font:900 28px/28px Arial,sans-serif!important}
.modalwrap:has(.rgrid) #mbody{max-height:calc(76dvh - 48px)!important;overflow:auto!important;padding:7px!important}
.modalwrap:has(.rgrid) .rgrid{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:5px!important}
.modalwrap:has(.rgrid) .rcp{min-width:0!important;padding:5px!important;font-size:11px!important;line-height:1.2!important}
.modalwrap:has(.rgrid) .recipe-detail{grid-column:1/-1!important;grid-row:auto!important;position:static!important;inset:auto!important;width:100%!important;max-height:none!important;overflow:visible!important;margin:2px 0 0!important;padding:8px!important;box-sizing:border-box!important}
.modalwrap:has(.rgrid) .recipe-detail .big img{width:34px!important;height:34px!important;object-fit:contain!important}
.modalwrap:has(.rgrid) .recipe-detail .txt{font-size:12px!important;line-height:1.25!important;overflow-wrap:anywhere!important}
.modalwrap:has(.rgrid) .ingredients{display:flex!important;flex-direction:column!important;gap:4px!important;width:100%!important}
.modalwrap:has(.rgrid) .ingredient{display:flex!important;align-items:center!important;justify-content:space-between!important;gap:7px!important;width:100%!important;min-width:0!important;padding:5px 7px!important;font-size:12px!important;line-height:1.2!important;box-sizing:border-box!important}
.modalwrap:has(.rgrid) .ingredient span{min-width:0!important;flex:1 1 auto!important;overflow-wrap:anywhere!important}
.modalwrap:has(.rgrid) .ingredient b{flex:0 0 auto!important;white-space:nowrap!important;font-size:12px!important}
.modalwrap:has(.rgrid) .recipe-detail button{min-height:39px!important;padding:6px 8px!important;font-size:13px!important}
@media(max-width:430px){.modalwrap:has(.rgrid) .modal{width:min(420px,88vw)!important;max-height:76dvh!important}.modalwrap:has(.rgrid) #mbody{max-height:calc(76dvh - 48px)!important}.modalwrap:has(.rgrid) .rgrid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.modalwrap:has(.rgrid) .recipe-detail{grid-column:1/-1!important;grid-row:auto!important}}
@media(max-height:430px){.modalwrap:has(.rgrid) .modal{max-height:76dvh!important}.modalwrap:has(.rgrid) #mbody{max-height:calc(76dvh - 48px)!important}}
"""
if '</style>' in s:
    s = s.replace('</style>', compact_craft_css + '\\n</style>', 1)
else:
    print("WARNING: style tag not found; compact crafting CSS skipped")
p.write_text(s, encoding='utf-8')
print("Added compact crafting-station layout.")


# Final UI sizing pass: compact and center game dialogs.
ui_size_css = r"""
/* Compact, centered dialogs for phone screens */
.modalwrap{
  align-items:center!important;
  justify-content:center!important;
  padding:8px!important;
  background:rgba(5,12,8,.48)!important;
}
.modal{
  width:min(420px,88vw)!important;
  max-width:calc(100vw - 16px)!important;
  max-height:76dvh!important;
  margin:auto!important;
  border-width:3px!important;
  box-shadow:0 4px 0 #422d1f!important;
}
.mhead{min-height:40px!important;padding:5px 8px!important;gap:7px!important}
.mhead h2{font-size:clamp(15px,2.5vw,18px)!important;line-height:1.15!important}
#mbody{
  max-height:calc(76dvh - 48px)!important;
  padding:7px 8px 8px!important;
  font-size:12px!important;
  overflow:auto!important;
}
.rgrid{grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:5px!important}
.rcp{min-width:0!important;padding:5px!important;font-size:11px!important}
.recipe-detail{position:static!important;inset:auto!important;margin:7px 0 0!important;padding:7px!important}
.ingredients{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:4px!important}
.ingredient{padding:4px!important;font-size:10px!important}
.ingredient img{width:22px!important;height:22px!important}
.recipe-detail button{min-height:36px!important;padding:7px!important;font-size:12px!important}
@media (orientation:portrait){
 .modal{width:min(88vw,420px)!important;max-height:76dvh!important}
 #mbody{max-height:calc(76dvh - 48px)!important}
 .rgrid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
}
@media (max-height:420px){
 .modal{width:min(400px,84vw)!important;max-height:76dvh!important}
 #mbody{max-height:calc(76dvh - 48px)!important}
}
"""
if '</style>' in s:
    s = s.replace('</style>', ui_size_css + '\\n</style>', 1)
else:
    print("WARNING: no style closing tag found for compact UI sizing")
p.write_text(s, encoding='utf-8')
print("Applied final compact centered UI sizing.")


# Keep backpack and crafting dialogs compact like the main menu/map.
small_panels_css = r"""
.modalwrap.pouch-theme .modal,
.modalwrap:has(.rgrid) .modal{
  width:min(340px,82vw)!important;
  max-width:calc(100vw - 28px)!important;
  max-height:64dvh!important;
  height:auto!important;
  margin:auto!important;
  overflow:hidden!important;
}
.modalwrap.pouch-theme #mbody,
.modalwrap:has(.rgrid) #mbody{
  max-height:calc(64dvh - 46px)!important;
  overflow-y:auto!important;
  overscroll-behavior:contain!important;
  padding:6px!important;
}
.modalwrap.pouch-theme .igrid,
.modalwrap.pouch-theme .invgrid,
.modalwrap.pouch-theme .inv-grid,
.modalwrap.pouch-theme .inventory-grid,
.modalwrap.pouch-theme .itemgrid,
.modalwrap.pouch-theme .item-grid{
  grid-template-columns:repeat(5,minmax(0,1fr))!important;
  gap:4px!important;
  padding:4px!important;
}
.modalwrap.pouch-theme .mhead,
.modalwrap:has(.rgrid) .mhead{min-height:38px!important;padding:4px 7px!important}
.modalwrap.pouch-theme .mhead h2,
.modalwrap:has(.rgrid) .mhead h2{font-size:16px!important;line-height:1.15!important}
@media(max-width:380px){
 .modalwrap.pouch-theme .modal,.modalwrap:has(.rgrid) .modal{width:84vw!important;max-height:62dvh!important}
 .modalwrap.pouch-theme #mbody,.modalwrap:has(.rgrid) #mbody{max-height:calc(62dvh - 44px)!important}
}
"""
if '</style>' in s:
    s = s.replace('</style>', small_panels_css + '\\n</style>', 1)
else:
    print("WARNING: no style closing tag found for small panel sizing")
p.write_text(s, encoding="utf-8")
print("Reduced backpack and crafting dialogs to compact centered panels.")


# Clean, unified backpack/crafting layout with lightweight motion and clearer recipe cards.
clean_panels_css = r"""
@keyframes wwPanelIn{from{opacity:0;transform:translateY(8px) scale(.975)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes wwCardIn{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:translateY(0)}}
.modalwrap.pouch-theme .modal,
.modalwrap:has(.rgrid) .modal{
  width:min(340px,82vw)!important;
  max-width:calc(100vw - 28px)!important;
  max-height:64dvh!important;
  display:flex!important;flex-direction:column!important;
  border-radius:12px!important;
  animation:wwPanelIn .18s ease-out both!important;
  transform-origin:center center!important;
}
.modalwrap.pouch-theme #mbody,
.modalwrap:has(.rgrid) #mbody{
  flex:1 1 auto!important;min-height:0!important;
  max-height:calc(64dvh - 46px)!important;
  overflow-y:auto!important;overflow-x:hidden!important;
  overscroll-behavior:contain!important;
  scrollbar-width:thin!important;
  padding:7px!important;
}
.modalwrap:has(.rgrid) .rgrid{
  display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;
  align-items:stretch!important;gap:6px!important;
}
.modalwrap:has(.rgrid) .rcp{
  min-width:0!important;min-height:52px!important;height:auto!important;
  display:flex!important;align-items:center!important;justify-content:flex-start!important;
  gap:6px!important;padding:7px!important;box-sizing:border-box!important;
  white-space:normal!important;overflow-wrap:anywhere!important;text-align:left!important;
  border-radius:8px!important;line-height:1.2!important;
  animation:wwCardIn .16s ease-out both!important;
  transition:transform .14s ease,filter .14s ease,background-color .14s ease!important;
}
.modalwrap:has(.rgrid) .rcp:active{transform:scale(.97)!important;filter:brightness(1.08)!important}
.modalwrap:has(.rgrid) .recipe-detail{
  grid-column:1/-1!important;grid-row:auto!important;
  position:static!important;inset:auto!important;float:none!important;
  width:100%!important;max-width:100%!important;max-height:none!important;
  overflow:visible!important;box-sizing:border-box!important;
  margin:6px 0 0!important;padding:9px!important;border-radius:9px!important;
  display:block!important;
}
.modalwrap:has(.rgrid) .recipe-detail .big{display:flex!important;align-items:center!important;gap:8px!important;min-width:0!important}
.modalwrap:has(.rgrid) .recipe-detail .big img{width:32px!important;height:32px!important;object-fit:contain!important;flex:0 0 32px!important}
.modalwrap:has(.rgrid) .recipe-detail .txt{min-width:0!important;font-size:12px!important;line-height:1.3!important;overflow-wrap:anywhere!important}
.modalwrap:has(.rgrid) .ingredients{display:flex!important;flex-direction:column!important;gap:4px!important;width:100%!important;margin:7px 0!important}
.modalwrap:has(.rgrid) .ingredient{display:flex!important;align-items:center!important;justify-content:space-between!important;gap:8px!important;width:100%!important;min-width:0!important;box-sizing:border-box!important;padding:6px 8px!important;border-radius:6px!important;font-size:12px!important;line-height:1.25!important}
.modalwrap:has(.rgrid) .ingredient span{flex:1 1 auto!important;min-width:0!important;overflow-wrap:anywhere!important}
.modalwrap:has(.rgrid) .ingredient b{flex:0 0 auto!important;white-space:nowrap!important}
.modalwrap:has(.rgrid) .recipe-detail button{width:100%!important;min-height:42px!important;margin-top:5px!important;border-radius:8px!important;font-size:13px!important;transition:transform .14s ease,filter .14s ease!important}
.modalwrap:has(.rgrid) .recipe-detail button:active{transform:scale(.98)!important;filter:brightness(1.08)!important}
.modalwrap.pouch-theme .igrid,.modalwrap.pouch-theme .invgrid,.modalwrap.pouch-theme .inv-grid,
.modalwrap.pouch-theme .inventory-grid,.modalwrap.pouch-theme .itemgrid,.modalwrap.pouch-theme .item-grid{
  grid-template-columns:repeat(5,minmax(0,1fr))!important;gap:5px!important;padding:4px!important;
}
.modalwrap.pouch-theme .igrid>*,.modalwrap.pouch-theme .invgrid>*,.modalwrap.pouch-theme .inv-grid>*,
.modalwrap.pouch-theme .inventory-grid>*,.modalwrap.pouch-theme .itemgrid>*,.modalwrap.pouch-theme .item-grid>*{
  min-width:0!important;box-sizing:border-box!important;transition:transform .14s ease,filter .14s ease!important;
}
.modalwrap.pouch-theme .igrid>*:active,.modalwrap.pouch-theme .invgrid>*:active,.modalwrap.pouch-theme .inv-grid>*:active,
.modalwrap.pouch-theme .inventory-grid>*:active,.modalwrap.pouch-theme .itemgrid>*:active,.modalwrap.pouch-theme .item-grid>*:active{transform:scale(.96)!important;filter:brightness(1.08)!important}
.modalwrap.pouch-theme button,.modalwrap:has(.rgrid) button{touch-action:manipulation}
@media(max-width:380px){
 .modalwrap.pouch-theme .modal,.modalwrap:has(.rgrid) .modal{width:84vw!important;max-height:62dvh!important}
 .modalwrap.pouch-theme #mbody,.modalwrap:has(.rgrid) #mbody{max-height:calc(62dvh - 44px)!important}
 .modalwrap:has(.rgrid) .rcp{min-height:48px!important;padding:6px!important;font-size:11px!important}
}
@media(prefers-reduced-motion:reduce){
 .modalwrap.pouch-theme .modal,.modalwrap:has(.rgrid) .modal,.modalwrap:has(.rgrid) .rcp{animation:none!important;transition:none!important}
}
"""
if '</style>' in s:
    s = s.replace('</style>', clean_panels_css + '\\n</style>', 1)
else:
    print("WARNING: no style closing tag found for clean panel UI")

# Crafting station visibility: hand recipes stay separate from workbench recipes.
old_tabs = """let h=`<div class="tabs">${['all','hand','workbench','furnace','cook'].map(t=>`<button class="tab ${craftTab===t?'on':''}" data-tab="${t}">${t==='all'?' All':STATION_NAME[t]}</button>`).join('')}</div>`;"""
new_tabs = """const craftTabs=['hand',...(near.workbench?['workbench']:[]),...(near.furnace?['furnace']:[]),...(near.cook?['cook']:[])];
  if(!craftTabs.includes(craftTab)) craftTab=near.workbench?'workbench':near.furnace?'furnace':near.cook?'cook':'hand';
  let h=`<div class="tabs">${craftTabs.map(t=>`<button class="tab ${craftTab===t?'on':''}" data-tab="${t}">${t==='hand'?'Hand Crafting':STATION_NAME[t]}</button>`).join('')}</div>`;"""
if old_tabs in s:
    s=s.replace(old_tabs,new_tabs,1)
else:
    print("WARNING: crafting tab source pattern not found; station tabs not changed")
old_filter = """const list=RECIPES.map((r,i)=>({r,i})).filter(({r})=>craftTab==='all'||(r.st||'hand')===craftTab).map(o=>({...o,ok:canCraft(o.r,near)})).sort((a,b)=>b.ok-a.ok);"""
new_filter = """const list=RECIPES.map((r,i)=>({r,i})).filter(({r})=>(r.st||'hand')===craftTab).map(o=>({...o,ok:canCraft(o.r,near)})).sort((a,b)=>b.ok-a.ok);"""
if old_filter in s:
    s=s.replace(old_filter,new_filter,1)
else:
    print("WARNING: recipe filter source pattern not found")
old_close = """function closeModal(){ if(modal==='death') return; selectedRecipe=null; modal=null;"""
new_close = """function closeModal(){ if(modal==='death') return; selectedRecipe=null; craftTab='all'; modal=null;"""
if old_close in s:
    s=s.replace(old_close,new_close,1)
else:
    print("WARNING: closeModal reset pattern not found")

p.write_text(s, encoding="utf-8")
print("Applied clean compact backpack/crafting UI and lightweight animations.")


