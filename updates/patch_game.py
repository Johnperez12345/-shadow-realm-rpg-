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
