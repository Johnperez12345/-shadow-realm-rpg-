from pathlib import Path

p = Path("app/src/main/assets/index.html")
s = p.read_text(encoding="utf-8")

replacements = [
    ('.bar b{position:relative;font-size:9px;line-height:12px;padding-left:4px;font-weight:900;letter-spacing:.3px}',
     '.bar b{position:relative;display:block;font-size:10px;line-height:12px;padding-left:4px;font-weight:1000;letter-spacing:.45px;color:#fff;text-shadow:1px 1px 2px #000, -1px -1px 1px #000;white-space:nowrap;z-index:1}'),
    ('<div class="bar hp" id="hpBar"><i id="hpFill"></i><b> <span id="hpTxt">100</span></b></div>',
     '<div class="bar hp" id="hpBar"><i id="hpFill"></i><b>HEALTH <span id="hpTxt">100</span></b></div>'),
    ('FOOD <span id="foodTxt">100</span>', 'HUNGER <span id="foodTxt">100</span>'),
    ('WATER <span id="waterTxt">100</span>', 'THIRST <span id="waterTxt">100</span>'),
    ('<button class="ibtn" id="soundToggle"></button>',
     '<button class="ibtn" id="soundToggle" aria-label="Toggle sound" title="Toggle sound">♫</button>'),
    ("$('soundToggle').onclick = () => { soundOn=!soundOn; $('soundToggle').textContent=soundOn?'':'×'; if(soundOn){audio(); sfx('open');} say(soundOn?'Sound on':'Sound off'); };",
     "$('soundToggle').textContent = soundOn ? '♫' : '×';\n$('soundToggle').onclick = () => { soundOn=!soundOn; $('soundToggle').textContent=soundOn?'♫':'×'; $('soundToggle').setAttribute('aria-label',soundOn?'Mute sound':'Enable sound'); if(soundOn){audio(); sfx('open');} say(soundOn?'Sound on':'Sound off'); };"),
    ('const cost=Object.entries(r.cost).map(([id,n])=>{ const have=countItem(id); return `<span class="${have<n?\'no\':\'\'}">${ITEMS[id].i}${have}/${n}</span>`; }).join(\' \');',
     'const cost=Object.entries(r.cost).map(([id,n])=>{ const have=countItem(id); return `<span class="${have<n?\'no\':\'\'}">${ITEMS[id].n} ${have}/${n}</span>`; }).join(\' · \');'),
    ('h+=`<div class="near">Nearby: ${[\'workbench\',\'furnace\',\'cook\'].map(t=>STATION_NAME[t]+(near[t]?\' \':\' \')).join(\' \')}</div><div class="rgrid">`;',
     'h+=`<div class="near">Ingredients show owned/required amounts. Hand recipes work anywhere; other recipes need the named station within 3 tiles. Nearby: ${[\'workbench\',\'furnace\',\'cook\'].map(t=>STATION_NAME[t]+(near[t]?\' ✓\':\' ✕\')).join(\' · \')}</div><div class="rgrid">`;')
]

for old, new in replacements:
    if old not in s:
        print("NOTE: source pattern not found; skipped:", old[:70])
    else:
        s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")
print("Wildwood HUD and crafting UI patch applied.")
