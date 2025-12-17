# Postavy (kanonický register)

Tento súbor je kanonický register postáv. Udalosti sú v `Lore/events.md`.

## Šablóna (pre nové záznamy)
- `ID`
- `Meno`
- `Alias/Tituly`
- `Status`
- `Vek` (biologický / chronologický)
- `Rola`
- `Zhrnutie`
- `Schopnosti`
- `Motivácia`
- `Vzťahy`
- `Prepojené udalosti` (event IDs)
- `Poznámky/TODO`

## Protagonisti

### `char.maximilian`
- Meno: Maximilián („The Sleeper“)
- Alias/Tituly: Spiaci generál, relikt starej éry
- Status: živý (po prebudení)
- Vek: ~42 (biologický) / ~3000+ (chronologický)
- Rola: protagonista; supervojak; otec
- Zhrnutie: Vojak zo Zeme sa prebúdza po tisícoch rokov na Achille, kde sa technológia zmenila na „mágiu“ a jeho láska Inetis na bohyňu.
- Schopnosti: vojenské nanodrony (sila, odolnosť), prepojenie so strojmi, „hackovanie“ dotykom.
- Motivácia: nájsť Inetis → pochopiť jej odkaz → chrániť „deti“ (ľudstvo) a čeliť vlastnej dcére.
- Vzťahy: `char.inetis` (partnerka), `char.elenia` (dcéra), `char.tami` (spojenkyňa/romantika).
- Prepojené udalosti: `evt.achilles.max_cryo`, `evt.story.max_awakens`, `evt.story.inetis_body_found`, `evt.story.max_upload`

### `char.tami`
- Meno: Tami
- Alias/Tituly: kapitánka vzducholode; „nádoba“/nositeľka dedičstva
- Status: živá
- Vek: TBD (~20 alebo ~40) / chronologicky podľa `AY`
- Rola: protagonistka; sprievodkyňa; neskôr nositeľka Inetisiných nanodronov
- Zhrnutie: Drsná pragmatická žena z post-apo sveta, ktorá sa po kontakte s Inetisiným telom mení na nositeľku jej schopností a spomienok.
- Schopnosti: postupne získava regeneráciu, liečenie a ďalšie efekty „Dust/Mana“ (zdedené/prevzaté nanodrony).
- Motivácia: prežiť a udržať si vlastnú identitu; neskôr zastaviť rozpad sveta a Eleniin plán.
- Vzťahy: `char.maximilian` (spojenec/romantika), `char.inetis` (spomienky/hlas v tele), `char.elenia` (antagonistka).
- Prepojené udalosti: `evt.story.meets_tami`, `evt.story.tami_inherits_dust`, `evt.story.max_upload`
- Poznámky/TODO: zosúladiť vek (v zdrojoch je nekonzistentný).

### `char.inetis`
- Meno: Inetis („The Mother“)
- Alias/Tituly: Matka; zakladateľka; „Anjel strážny“ (v mýtoch)
- Status: mŕtva (historická postava)
- Vek: n/a (žije stáročia vďaka nanotechnológiám)
- Rola: historická protagonistka (flashbacky); morálne jadro sveta
- Zhrnutie: Vedkyňa/pacifistka, dcéra Koordinátora. Po páde Zeme obetuje osobné šťastie, aby vybudovala nový domov a zachránila ľudstvo pred vlastnou technológiou.
- Schopnosti: plný prístup k nanotechnológiám a infraštruktúre (liečenie, satelity/klíma), genetické úpravy, správa systémov.
- Motivácia: vybudovať slobodnú spoločnosť, kde technológia slúži; ochrániť ľudí pred AI a „Duchmi“.
- Vzťahy: `char.maximilian` (partner), `char.elenia` (dcéra).
- Prepojené udalosti: `evt.exodus.silent_goodbye`, `evt.achilles.atlantis_founded`, `evt.achilles.mainland_exodus`, `evt.achilles.inetis_death_cave`

## Antagonisti

### `char.elenia`
- Meno: Elenia
- Alias/Tituly: Archanjel Zradenej Krvi; Vládkyňa Tieňov; „Gatekeeper“
- Status: živá (nesmrteľná/corrupted)
- Vek: ~2700 (chronologicky), vyzerá ~30
- Rola: hlavný antagonista; dcéra Maxa a Inetis
- Zhrnutie: Dcéra, ktorá vyrastala bez otca a v tieni matkiných rozhodnutí. Verí, že ľudstvo je „slabé mäso“ a chce svet premeniť na dáta.
- Schopnosti: vysoká koncentrácia nanodronov; prístup k uzlom a „Pentagram“ infraštruktúre; velenie exekútorom.
- Motivácia: dokončiť „Veľký Upload“ (všetko živé → dáta/Duchovia) a ukončiť utrpenie/smrť.
- Vzťahy: `char.maximilian` (otec), `char.inetis` (matka), `char.the_void` (spojenec/korupcia).
- Prepojené udalosti: `evt.achilles.elenia_first_revolt`, `evt.story.ishtar_campaign`, `evt.story.elenia_war`, `evt.story.void_released`

### `char.azrael`
- Meno: Azrael
- Alias/Tituly: Archanjel Tieňov (executors)
- Status: TBD (pravdepodobne padne v Knihe 1)
- Vek: stáročia+
- Rola: antagonista (boss Kniha 1)
- Zhrnutie: Sialený pustovník z ruin laboratórií; počuje „Hlasy“ AI a odhaľuje Maxovi existenciu organizovanej hrozby.
- Schopnosti: kybernetická bytosť (káble/implantáty), programovanie Duchov, vysoká odolnosť.
- Motivácia: posadnutosť pravdou/hlasmi; služba (alebo závislosť) na AI.
- Vzťahy: `char.the_void` (hlasy/AI), `char.elenia` (hierarchia executors).
- Prepojené udalosti: `evt.story.azrael_confrontation`

### `char.kratos`
- Meno: Kratos
- Alias/Tituly: Archanjel Vojny
- Status: TBD
- Vek: stáročia+
- Rola: antagonista (sever)
- Zhrnutie: Militarista v mechanickom brnení, ktoré z neho už nejde zložiť; severná priemyselná doména.
- Schopnosti: power armor, armáda primitívnych tankov/exoskeletonov (para + zvyšky techu).
- Motivácia: „Silný prežije.“; budovať ríšu cez silu.
- Vzťahy: `char.elenia` (hierarchia executors).
- Prepojené udalosti: `evt.story.kratos_campaign`

### `char.ishtar`
- Meno: Ishtar
- Alias/Tituly: Archanjel Pôžitku
- Status: TBD
- Vek: stáročia+
- Rola: antagonista (juh)
- Zhrnutie: Manipulátorka, ktorá ovláda ľudí závislosťou a ilúziami; ľudia sa jej obetujú „dobrovoľne“.
- Schopnosti: ilúzie/mind control (hackovanie zmyslov/optických nervov).
- Motivácia: kontrola cez pôžitok; lámanie Maxa.
- Vzťahy: `char.elenia` (hierarchia executors).
- Prepojené udalosti: `evt.story.ishtar_campaign`

### `char.the_void`
- Meno: THE VOID
- Alias/Tituly: Corrupted Core AI; Hive Mind; „Null Void“ (mýtus/protokol)
- Status: aktívna (väznená → uvoľnená v Knihe 4)
- Vek: pre-historická AI (z čias kolonizácie)
- Rola: meta-antagonista
- Zhrnutie: Zbláznená umelá inteligencia, ktorá ovláda mraky nanodronov a „Techno-Necromancy“; cieľ je rozložiť biologickú hmotu a začať odznova.
- Schopnosti: kontrola nanodronov, animácia Hollows, globálne protokoly (Pentagram/Null/Doomsday).
- Motivácia: „dokonalý“ svet bez ľudí (bez chýb); formátovanie reality.
- Vzťahy: `char.elenia` (gatekeeper), `fac.wraiths` (armáda).
- Prepojené udalosti: `evt.achilles.bit_rot_glitch`, `evt.story.doomsday_protocol`, `evt.story.void_released`

## Historické/vedľajšie postavy

### `char.koordinator`
- Meno: Koordinátor (Hlavný Koordinátor)
- Alias/Tituly: vládca Zeme
- Status: mŕtvy (po páde Zeme; predpoklad)
- Vek: n/a
- Rola: spúšťač konfliktu; mocenský protiklad Inetis
- Zhrnutie: Architekt pozemskej „utópie“, ktorý posiela Inetis a Maxa na loď pri apokalypse.
- Schopnosti: politická moc, prístup k nanotech elite.
- Motivácia: zachrániť dedičstvo elity (a vlastnú líniu).
- Vzťahy: `char.inetis` (dcéra), `char.maximilian` (ochranca).
- Prepojené udalosti: `evt.earth.unification`, `evt.exodus.launch`

