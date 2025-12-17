# Worldbuilding plan (Null Void / Hviezda z Popola)

## Ciele
- Vyťažiť a normalizovať lore z existujúcich zdrojov (`world-bible.md`, `null-void-saga.md`, `the-pentagram-arc.md`) 
- Vytvoriť „jediný zdroj pravdy“ pre: postavy, udalosti, časovú os, miesta, frakcie/kultúry, predmety/technológie, zvieratá, zvyky/rituály.
- Odstrániť duplicity tým, že nový obsah v priečinkoch `Lore/` a `Characters/` bude kanonický; staré súbory môžu ostať ako archívne poznámky.

## Konvencie (aby sa dalo deduplikovať)
- Každá entita má stabilné `ID`:
  - `char.*`, `evt.*`, `item.*`, `fac.*`, `place.*`, `species.*`, `custom.*`, `concept.*`
- Čas:
  - `EY` = Earth Years (približné)
  - `AY` = Achilles Years (od pristátia = 0)
- Každá položka má aspoň: `ID`, `Názov`, `Zhrnutie`, `Tagy`, `Zdroj`, `Nejasnosti/TODO`.

## Kroky (multi-step)
1. Import Gemini konverzácie
   - Vložiť transcript do súboru `Sources/gemini-c9b6dd236dd0.md` (alebo premenovať podľa potreby).
2. Extrakcia entít
   - Označiť mená, udalosti, frakcie, predmety, miesta, zvieratá, zvyky.
3. Normalizácia/deduplikácia
   - Zlúčiť synonymá (napr. loď Ark/EXODUS), zjednotiť názvy, rozhodnúť o vekoch/rokoch.
4. Dopĺňanie prázdnych miest
   - Kultúry, zvyky, fauna, ekonomika, náboženstvo, politika, geografia.
5. Údržba
   - Každý nový nápad zapisovať iba do kanonických súborov v `Lore/` a `Characters/`.
6. (Voliteľné) Archivácia existujúcich biblí
   - Presunúť `world-bible.md`, `null-void-saga.md`, `the-pentagram-arc.md` do `Archive/` a nechať v root-e iba odkazy/index.

## Otázky na rozhodnutie (blokujú kanonizáciu)
- Ako sa volá loď: `Ark`, `EXODUS`, alebo sú to dve rôzne lode?
- Aký je kanonický vek Tami na začiatku príbehu: ~20 alebo ~40?
- Chceš používať absolútne roky (EY/AY) alebo len éry (Zlatý vek, Temnota, Mýty)?
- Má byť jazyk databázy primárne SK alebo EN?

## Stav po tomto kroku
- Založené kanonické súbory: `Lore/timeline.md`, `Lore/events.md`, `Characters/characters.md` + doplnkové zoznamy.
- Gemini transcript ešte chýba → po dodaní ho doplním a deduplikujem.
