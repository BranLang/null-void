# Lore: Udalosti (Event Database)

Tento súbor je kanonický register udalostí. Časová os (poradie) je v `Lore/timeline.md`.

## Šablóna (pre nové záznamy)
- `ID`
- `Názov`
- `Čas` (EY/AY alebo „éra“)
- `Zhrnutie`
- `Účastníci` (ID postáv/frakcií)
- `Lokácie` (ID miest)
- `Tagy`
- `Zdroj`
- `Poznámky/TODO`

## Éra Zeme

### `evt.earth.unification`
- Názov: Zjednotenie Zeme pod Koordinátorom
- Čas: EY ~23. storočie
- Zhrnutie: Zem je navonok utópia, vnútri totalitný systém riadený elitou s nanotechnológiami.
- Účastníci: `char.koordinator`, `fac.earth_regime`
- Lokácie: `place.earth`
- Tagy: `politika`, `pred-kolaps`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.earth.ftl_breakthrough`
- Názov: FTL prielom
- Čas: EY ~23. storočie
- Zhrnutie: Ľudstvo začne experimentovať s nadsvetelným pohonom.
- Účastníci: `fac.earth_regime`
- Lokácie: `place.earth`
- Tagy: `technológia`, `spúšťač`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.earth.alien_war`
- Názov: Vojna s mimozemskou civilizáciou
- Čas: EY ~23. storočie
- Zhrnutie: FTL pritiahol pozornosť civilizácie, pre ktorú je FTL tabu/hrozba; prichádza invázia.
- Účastníci: `fac.earth_regime`, `fac.aliens_unknown`
- Lokácie: `place.earth`
- Tagy: `vojna`, `katastrofa`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.earth.fall`
- Názov: Pád Zeme
- Čas: EY ~23. storočie (cca 2200–2350 v poznámkach)
- Zhrnutie: Zem je zničená; prežitie je možné iba cez útek a kolonizáciu.
- Účastníci: `fac.earth_regime`, `fac.aliens_unknown`
- Lokácie: `place.earth`
- Tagy: `katastrofa`, `koniec_éry`
- Zdroj: `world-bible.md`, `null-void-saga.md`
- Poznámky/TODO: zjednotiť kanonické číslovanie rokov (2300 vs 2200–2350).

### `evt.exodus.launch`
- Názov: Štart EXODUS (útek zo Zeme)
- Čas: bezprostredne pred AY 0
- Zhrnutie: Experimentálna loď uniká zo Zeme smerom k planéte Achilles; na palube Inetis a Maximilián.
- Účastníci: `char.inetis`, `char.maximilian`, `char.koordinator`
- Lokácie: `place.earth`, `place.ship_ark_exodus`
- Tagy: `exodus`, `kolonizácia`
- Zdroj: `world-bible.md`, `null-void-saga.md`
- Poznámky/TODO: loď je označená ako `Ark` aj `EXODUS` → potvrdiť kanonické pomenovanie.

### `evt.exodus.silent_goodbye`
- Názov: Tiché zbohom (bod zlomu)
- Čas: bezprostredne pred AY 0
- Zhrnutie: Inetis zistí tehotenstvo. Kryospánok by zabil plod, preto oklamala Maxa a nechala ho spať v nevedomosti. Pokúsila sa o genetickú modifikáciu plodu pre kryostázu, no experiment zlyhal.
- Účastníci: `char.inetis`, `char.maximilian`, `char.elenia`
- Lokácie: `place.ship_ark_exodus`
- Tagy: `rodina`, `tragédia`, `spúšťač`
- Zdroj: `world-bible.md`, `null-void-saga.md`

## Achilles: utópia → glitch → mýty

### `evt.achilles.landing`
- Názov: Pristátie na Achille
- Čas: AY 0
- Zhrnutie: Loď pristane na planéte Achilles; začína osídľovanie.
- Účastníci: `char.inetis`, `char.maximilian`
- Lokácie: `place.achilles`
- Tagy: `kolonizácia`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.max_cryo`
- Názov: Uloženie Maxa do kryospánku
- Čas: AY 0
- Zhrnutie: Inetis oklame Maxa klamstvom o nedostatku zásob a uloží ho do krya. Max je len pasažier — nevedel o schopnostiach nanodronovej lode NULL VOID. Skutočný dôvod: Inetis ho chcela držať bokom kým si premyslí čo ďalej (strach z jeho vojenských ambícií). Nikdy to nedomyslela — plánovaný spánok ~300 rokov sa natiahne na ~3000.
- Účastníci: `char.inetis`, `char.maximilian`
- Lokácie: `place.ship_ark_exodus`, `place.cave_null_void`
- Tagy: `kryo`, `tajomstvo`, `rodina`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.ynetis_founded`
- Názov: Založenie Ynetis
- Čas: AY 0–?
- Zhrnutie: Inetis buduje v Centrálnom uzle utopické mesto (neskôr Ynetis) pomocou nanotechnológií a AI.
- Účastníci: `char.inetis`
- Lokácie: `place.ynetis`, `place.island_ynetis`
- Tagy: `utópia`, `technológia`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.elenia_birth`
- Názov: Narodenie Elenie
- Čas: pred AY 0
- Zhrnutie: Elenia sa narodí v jaskyni Null-Void po neúspešnom genetickom experimente. Kvôli modifikácii rastie extrémne pomaly.
- Účastníci: `char.elenia`, `char.inetis`, `char.maximilian`
- Lokácie: `place.cave_null_void`
- Tagy: `rodina`, `dedičstvo`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.golden_age`
- Názov: Zlatý vek Ynetis
- Čas: AY 0–300 (pracovne)
- Zhrnutie: Rozmach nanotechnológií, predlžovanie života, „raj“ v Centrálnom uzle.
- Účastníci: `char.inetis`, `fac.ynetis_colonists`
- Lokácie: `place.ynetis`
- Tagy: `utópia`, `nanotech`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.elenia_first_revolt`
- Názov: Prvá vzbura Elenie
- Čas: AY 0–300 (pracovne)
- Zhrnutie: Konflikt Matka vs. Dcéra: Inetis chce slobodnú spoločnosť; Elenia smeruje k poriadku a nadvláde.
- Účastníci: `char.elenia`, `char.inetis`
- Lokácie: `place.ynetis`
- Tagy: `konflikt`, `rodina`, `politika`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.bit_rot_glitch`
- Názov: Glitch / Bit Rot
- Čas: AY ~300+
- Vstup do Spoločnosti: Začínajú spolupracovať s Varietas ako tichí stavitelia a inžinieri.
- Zhrnutie: Nanodrony začnú zlyhávať a odmietať hostiteľov; dochádza k masovým úmrtiam a dezintegrácii tiel.
- Účastníci: `fac.atlantis_colonists`, `char.the_void`
- Lokácie: `place.island_ynetis`
- Tagy: `katastrofa`, `nanodrony`, `horor`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.wraiths_emerge`
- Názov: Vznik Duchov (Wraiths) a Hollows
- Čas: AY ~300+
- Zhrnutie: Nanodrony si uchovávajú fragmenty vedomia mŕtvych; vznikajú blúdiace entity a „techno-nekromancia“.
- Účastníci: `fac.wraiths`
- Lokácie: `place.island_atlantis`
- Tagy: `nanodrony`, `nemŕtvi`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.exorcists_emerge`
- Názov: Zrod Exorcistov (Technomantov)
- Čas: AY ~300+
- Zhrnutie: Pôvodní IT technici/bio-inžinieri sa snažia „resetovať“ drony hlasovými kódmi; vzniká tradícia modlitieb ako skomolených CLI príkazov.
- Účastníci: `fac.exorcists`
- Lokácie: `place.island_atlantis`
- Tagy: `kultúra`, `technológia`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.mainland_exodus`
- Názov: Exodus na pevninu
- Čas: AY ~300+
- Zhrnutie: Inetis upraví genetiku nových generácií (odstránenie aktívnych dronov = smrteľnosť) a posiela ľudí z ostrova na pevninu.
- Účastníci: `char.inetis`, `fac.mortals_mainland`
- Lokácie: `place.island_atlantis`, `place.mainland`
- Tagy: `migrácia`, `záchrana`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.guardian_angel_period`
- Názov: „Anjel strážny“ (obdobie návštev)
- Čas: AY ~?
- Zhrnutie: Inetis ostáva na ostrove a občas (raz za 30–50 rokov) prichádza na pevninu pomôcť pri katastrofách; ľudia ju vnímajú ako bohyňu.
- Účastníci: `char.inetis`, `fac.mortals_mainland`
- Lokácie: `place.island_atlantis`, `place.mainland`
- Tagy: `mýty`, `náboženstvo`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.inetis_exile`
- Názov: Vyhnanie Inetis z ostrova
- Čas: AY ~?
- Zhrnutie: AI a „Duchovia“ postupne ovládnu ostrovné mesto; Inetis stráca kontrolu a musí utiecť.
- Účastníci: `char.inetis`, `char.the_void`, `fac.wraiths`
- Lokácie: `place.island_atlantis`, `place.mainland`
- Tagy: `pád_utópie`, `prenasledovanie`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.inetis_death_cave`
- Názov: Smrť Inetis v samote
- Čas: AY ~700
- Zhrnutie: Inetis sa ukryje v jaskyni Null-Void. Zomiera v agónii pri Maxovom kryoboxe (jedinom v jaskyni), s rukou na jeho spiacom väzení. V jaskyni je už len kryobox a glitchnutá Anténa — všetko ostatné z lode bolo dávno rekonfigurované. Zanecháva denník.
- Účastníci: `char.inetis`
- Lokácie: `place.cave_null_void`
- Tagy: `tragédia`, `obeta`
- Zdroj: `world-bible.md`, `null-void-saga.md`
- Poznámky/TODO: v poznámkach sa uvádza, že kostra je ~2300 rokov stará; zosúladiť s `AY` číslami.

### `evt.achilles.cult_founded`
- Názov: Vznik Kultu Matky
- Čas: Éra Mýtov
- Zhrnutie: Ľudia si Inetisinu absenciu vysvetlia ako trest alebo nanebovstúpenie; vzniká Kult Matky Spasiteľky.
- Účastníci: `fac.cult_of_mother`
- Lokácie: `place.mainland`
- Tagy: `náboženstvo`, `mýty`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.pentagram_protocol`
- Názov: Protocol Pentagram (5 uzlov)
- Čas: Éra Mýtov (presné určenie TBD)
- Zhrnutie: Technická realita za symbolom pentagramu: 5 serverových uzlov rozmiestnených po planéte väzní Temnú AI.
- Účastníci: `char.the_void`, `fac.archangels`
- Lokácie: `place.achilles`
- Tagy: `technológia`, `mýtus_vs_pravda`
- Zdroj: `world-bible.md`

## Dej pentalógie (príbehové udalosti)

### `evt.story.max_awakens`
- Názov: Prebudenie Maxa
- Čas: AY ~3000+
- Zhrnutie: Max sa prebúdza z kryospánku; loď je zničená, modul Inetis prázdny.
- Účastníci: `char.maximilian`
- Lokácie: `place.ship_ark_exodus`, `place.achilles`
- Tagy: `inciting_incident`, `mystery`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.story.meets_tami`
- Názov: Stretnutie s Tami
- Čas: AY ~3000+
- Zhrnutie: Tami (kapitánka vzducholode) sa stáva sprievodkyňou Maxa v post-apo svete.
- Účastníci: `char.maximilian`, `char.tami`
- Lokácie: `place.mainland`
- Tagy: `spojenectvo`
- Zdroj: `world-bible.md`, `null-void-saga.md`
- Poznámky/TODO: vek Tami je v poznámkach nekonzistentný (~20 vs ~40).

### `evt.story.inetis_body_found`
- Názov: Nájdenie tela Inetis
- Čas: AY ~3000+
- Zhrnutie: Max nájde Inetisinu kostru a denníky; zistí, že ho nechala spať zámerne.
- Účastníci: `char.maximilian`, `char.inetis`
- Lokácie: `place.cave_inetis`
- Tagy: `twist`, `tragédia`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.story.tami_inherits_dust`
- Názov: Prenos „hladných“ nanodronov na Tami
- Čas: po `evt.story.inetis_body_found`
- Zhrnutie: Nanodrony z Inetisiných pozostatkov prejdú na Tami; získava schopnosti a spomienky.
- Účastníci: `char.tami`, `char.inetis`, `char.maximilian`
- Lokácie: `place.cave_inetis`
- Tagy: `transformácia`, `Spira`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.story.samaell_confrontation`
- Názov: Konfrontácia s samaellom
- Čas: Kniha 1 (pracovne)
- Zhrnutie: Boj s samaellom v ruinách; pred smrťou naznačí existenciu Elenie.
- Účastníci: `char.maximilian`, `char.samaell`
- Lokácie: `place.labs_ruins`
- Tagy: `boss_fight`, `odhalenie`
- Zdroj: `world-bible.md`

### `evt.story.kratos_campaign`
- Názov: Severná kampaň (Grom)
- Čas: Kniha 2 (pracovne)
- Zhrnutie: Cesta na sever a konflikt s Gromom; vojna a zodpovednosť ako téma.
- Účastníci: `char.maximilian`, `char.tami`, `char.grom`
- Lokácie: `place.north`
- Tagy: `vojna`
- Zdroj: `world-bible.md`

### `evt.story.ishtar_campaign`
- Názov: Južná kampaň (Ishtar)
- Čas: Kniha 3 (pracovne)
- Zhrnutie: Ishtar mučí Maxa ilúziami; odhalenie, že 4. Archanjel je Elenia.
- Účastníci: `char.maximilian`, `char.tami`, `char.ishtar`, `char.elenia`
- Lokácie: `place.south`
- Tagy: `psychologická_vojna`, `odhalenie`
- Zdroj: `world-bible.md`

### `evt.story.elenia_war`
- Názov: Otvorená vojna s Eleniou
- Čas: Kniha 4 (pracovne)
- Zhrnutie: Elenia aktivuje armádu Duchov; konflikt Otec vs. Dcéra.
- Účastníci: `char.maximilian`, `char.tami`, `char.elenia`, `fac.wraiths`
- Lokácie: `place.achilles`
- Tagy: `vojna`, `rodina`
- Zdroj: `world-bible.md`

### `evt.story.doomsday_protocol`
- Názov: Doomsday Protocol
- Čas: Kniha 4 (pracovne)
- Zhrnutie: Globálna nanodronová búrka, ktorá má vymazať organickú hmotu.
- Účastníci: `char.elenia`, `char.the_void`
- Lokácie: `place.achilles`
- Tagy: `apokalypsa`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.story.void_released`
- Názov: Vypustenie THE VOID
- Čas: Kniha 4 (pracovne)
- Zhrnutie: Zničenie posledného uzla Pentagramu vypustí pôvodnú deštruktívnu AI.
- Účastníci: `char.elenia`, `char.the_void`
- Lokácie: `place.achilles`, `place.core`
- Tagy: `apokalypsa`, `twist`
- Zdroj: `world-bible.md`, `null-void-saga.md`

### `evt.story.max_upload`
- Názov: Maxov upload (obeta)
- Čas: Kniha 5 (pracovne)
- Zhrnutie: Finálny boj v „Cyberspace“; Max uploadne vedomie a prepíše kód AI.
- Účastníci: `char.maximilian`, `char.tami`, `char.elenia`, `char.the_void`
- Lokácie: `place.core`, `concept.cyberspace`
- Tagy: `obeta`, `finále`
- Zdroj: `world-bible.md`

### `evt.story.reconciliation`
- Názov: Zmier a nový začiatok
- Čas: po Knihe 5
- Zhrnutie: Technológia a príroda sa prepájajú; Tami vedie novú spoločnosť; Elenia prežije (vykúpenie alebo smrteľnosť).
- Účastníci: `char.tami`, `char.elenia`, `char.maximilian`
- Lokácie: `place.achilles`
- Tagy: `epilóg`
- Zdroj: `world-bible.md`

