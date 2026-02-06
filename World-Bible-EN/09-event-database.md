# Lore: Events (Event Database)

This file is the canonical event register. The chronological timeline is in `01-timeline.md`.

## Template (for new entries)
- `ID`
- `Name`
- `Time` (EY/AY or "era")
- `Summary`
- `Participants` (character/faction IDs)
- `Locations` (place IDs)
- `Tags`
- `Source`
- `Notes/TODO`

## Earth Era

### `evt.earth.unification`
- Name: Unification of Earth under the Coordinator
- Time: EY ~23rd century
- Summary: Earth is outwardly a utopia, internally a totalitarian system ruled by an elite with nanotechnologies.
- Participants: `char.koordinator`, `fac.earth_regime`
- Locations: `place.earth`
- Tags: `politics`, `pre-collapse`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.earth.ftl_breakthrough`
- Name: FTL Breakthrough
- Time: EY ~23rd century
- Summary: Humanity begins experimenting with faster-than-light drive.
- Participants: `fac.earth_regime`
- Locations: `place.earth`
- Tags: `technology`, `trigger`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.earth.alien_war`
- Name: War with Alien Civilization
- Time: EY ~23rd century
- Summary: FTL attracted the attention of a civilization for which FTL is taboo/threat; invasion follows.
- Participants: `fac.earth_regime`, `fac.aliens_unknown`
- Locations: `place.earth`
- Tags: `war`, `catastrophe`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.earth.fall`
- Name: Fall of Earth
- Time: EY ~23rd century (approx. 2200–2350 in notes)
- Summary: Earth is destroyed; survival is possible only through escape and colonization.
- Participants: `fac.earth_regime`, `fac.aliens_unknown`
- Locations: `place.earth`
- Tags: `catastrophe`, `end_of_era`
- Source: `world-bible.md`, `null-void-saga.md`
- Notes/TODO: Unify canonical year numbering (2300 vs 2200–2350).

### `evt.exodus.launch`
- Name: EXODUS Launch (Escape from Earth)
- Time: Immediately before AY 0
- Summary: Experimental ship escapes Earth toward planet Achilles; Inetis and Maksimilian aboard.
- Participants: `char.inetis`, `char.maksimilian`, `char.koordinator`
- Locations: `place.earth`, `place.ship_ark_exodus`
- Tags: `exodus`, `colonization`
- Source: `world-bible.md`, `null-void-saga.md`
- Notes/TODO: Ship is labeled as both `Ark` and `EXODUS` → confirm canonical naming.

### `evt.exodus.silent_goodbye`
- Name: Silent Goodbye (Turning Point)
- Time: Immediately before AY 0
- Summary: Inetis discovers her pregnancy. Cryosleep would kill the fetus, so she deceived Maks and let him sleep in ignorance. She attempted genetic modification of the fetus for cryostasis, but the experiment failed.
- Participants: `char.inetis`, `char.maksimilian`, `char.elenia`
- Locations: `place.ship_ark_exodus`
- Tags: `family`, `tragedy`, `trigger`
- Source: `world-bible.md`, `null-void-saga.md`

## Achilles: Utopia → Glitch → Myths

### `evt.achilles.landing`
- Name: Landing on Achilles
- Time: AY 0
- Summary: Ship lands on planet Achilles; colonization begins.
- Participants: `char.inetis`, `char.maksimilian`
- Locations: `place.achilles`
- Tags: `colonization`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.max_cryo`
- Name: Placing Maks in Cryosleep
- Time: AY 0
- Summary: Inetis deceives Maks with a lie about insufficient supplies and places him in cryo. Maks was just a passenger — he didn't know about the nanodrone ship NULL VOID's capabilities. True reason: Inetis wanted to keep him aside while she figured out what to do next (fear of his military ambitions). She never resolved it — the planned ~300-year sleep stretched to ~3,000.
- Participants: `char.inetis`, `char.maksimilian`
- Locations: `place.ship_ark_exodus`, `place.cave_null_void`
- Tags: `cryo`, `secret`, `family`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.ynetis_founded`
- Name: Founding of Ynetis
- Time: AY 0–?
- Summary: Inetis builds a utopian city (later Ynetis) in the Central Node using nanotechnologies and AI.
- Participants: `char.inetis`
- Locations: `place.ynetis`, `place.island_ynetis`
- Tags: `utopia`, `technology`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.elenia_birth`
- Name: Birth of Elania
- Time: Before AY 0
- Summary: Elania is born in the Null-Void cave after a failed genetic experiment. Due to the modification, she grows extremely slowly.
- Participants: `char.elenia`, `char.inetis`, `char.maksimilian`
- Locations: `place.cave_null_void`
- Tags: `family`, `legacy`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.golden_age`
- Name: Golden Age of Ynetis
- Time: AY 0–300 (working)
- Summary: Boom of nanotechnologies, life extension, "paradise" in the Central Node.
- Participants: `char.inetis`, `fac.ynetis_colonists`
- Locations: `place.ynetis`
- Tags: `utopia`, `nanotech`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.elenia_first_revolt`
- Name: Elania's First Revolt
- Time: AY 0–300 (working)
- Summary: Mother vs. Daughter conflict: Inetis wants a free society; Elania gravitates toward order and supremacy.
- Participants: `char.elenia`, `char.inetis`
- Locations: `place.ynetis`
- Tags: `conflict`, `family`, `politics`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.bit_rot_glitch`
- Name: Glitch / Bit Rot
- Time: AY ~300+
- Entry into Society: They begin collaborating with Varietas as silent builders and engineers.
- Summary: Nanodrones begin failing and rejecting hosts; mass deaths and body disintegration occur.
- Participants: `fac.atlantis_colonists`, `char.the_void`
- Locations: `place.island_ynetis`
- Tags: `catastrophe`, `nanodrones`, `horror`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.wraiths_emerge`
- Name: Emergence of Wraiths and Hollows
- Time: AY ~300+
- Summary: Nanodrones retain fragments of the dead's consciousness; wandering entities emerge along with "techno-necromancy."
- Participants: `fac.wraiths`
- Locations: `place.island_atlantis`
- Tags: `nanodrones`, `undead`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.exorcists_emerge`
- Name: Birth of the Exorcists (Technomancers)
- Time: AY ~300+
- Summary: Original IT technicians/bio-engineers try to "reset" drones with voice codes; a tradition of prayers as corrupted CLI commands is born.
- Participants: `fac.exorcists`
- Locations: `place.island_atlantis`
- Tags: `culture`, `technology`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.mainland_exodus`
- Name: Exodus to the Mainland
- Time: AY ~300+
- Summary: Inetis modifies the genetics of new generations (removing active drones = mortality) and sends people from the island to the mainland.
- Participants: `char.inetis`, `fac.mortals_mainland`
- Locations: `place.island_atlantis`, `place.mainland`
- Tags: `migration`, `salvation`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.guardian_angel_period`
- Name: "Guardian Angel" (Period of Visits)
- Time: AY ~?
- Summary: Inetis remains on the island and occasionally (once every 30–50 years) visits the mainland to help during catastrophes; people perceive her as a goddess.
- Participants: `char.inetis`, `fac.mortals_mainland`
- Locations: `place.island_atlantis`, `place.mainland`
- Tags: `myths`, `religion`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.inetis_exile`
- Name: Exile of Inetis from the Island
- Time: AY ~?
- Summary: AI and "Wraiths" gradually take over the island city; Inetis loses control and must flee.
- Participants: `char.inetis`, `char.the_void`, `fac.wraiths`
- Locations: `place.island_atlantis`, `place.mainland`
- Tags: `fall_of_utopia`, `persecution`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.inetis_death_cave`
- Name: Death of Inetis in Solitude
- Time: AY ~700
- Summary: Inetis hides in the Null-Void cave. She dies in agony beside Maks's cryo-box (the only one in the cave), her hand resting on his sleeping prison. All that remains in the cave is the cryo-box and the glitched Antenna — everything else from the ship was long since reconfigured. She leaves behind a journal.
- Participants: `char.inetis`
- Locations: `place.cave_null_void`
- Tags: `tragedy`, `sacrifice`
- Source: `world-bible.md`, `null-void-saga.md`
- Notes/TODO: Notes state the skeleton is ~2,300 years old; reconcile with `AY` numbers.

### `evt.achilles.cult_founded`
- Name: Founding of the Cult of the Mother
- Time: Era of Myths
- Summary: People explain Inetis's absence as punishment or ascension; the Cult of the Mother Savior is born.
- Participants: `fac.cult_of_mother`
- Locations: `place.mainland`
- Tags: `religion`, `myths`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.achilles.great_battle`
- Name: The Great Battle (Atra Narrows)
- Time: AY ~850
- Summary: The Triumvirate (Grond, Samaell, Zaiya/Ishtar) attacks the Varietas empowered by Spira. Fox genocide (Vulpini). Inetis appears on the battlefield. The battle ends in a draw — but the foxes are decimated.
- Participants: `char.inetis`, `char.grond`, `char.samaell`, `char.ishtar`, `char.renn`, `fac.vulpini`
- Locations: `place.atra_narrows`, `place.mainland`
- Tags: `war`, `genocide`, `battle`
- Source: `10-inetis-chronicles.md`

### `evt.achilles.fox_exodus`
- Name: Fox Exodus to the East
- Time: AY ~850
- Summary: The last fox families flee east. **Renn** (Niktori, member of Inetis's Core Team) volunteers to escort them through the Wilds. **Inetis goes with them** — not alone, as the legends say. Inetis shows Renn the Cave of Ela and bids him farewell.
- Participants: `char.renn`, `char.inetis`, `fac.vulpini`
- Locations: `place.eastern_wilds`, `place.cave_ela`
- Tags: `migration`, `farewell`, `tragedy`
- Source: `characters/Renn.md`, `10-inetis-chronicles.md`

### `evt.achilles.kito_founded`
- Name: Founding of the City of Kitana (Kito)
- Time: AY ~850-950
- Summary: Renn and the foxes found the city of **Kitana** at secret coordinates provided by Inetis. A waiting place for the Third Arrival — where the Maki are supposed to land. Renn becomes the unofficial leader.
- Participants: `char.renn`, `fac.vulpini`
- Locations: `place.kito`
- Tags: `founding`, `city`
- Source: `characters/Renn.md`

### `evt.achilles.renn_death`
- Name: Death of Renn
- Time: AY 3000
- Summary: Pirates Vix and Kael kill Renn (Niktori, ~3000+ years old) for the Ancient Map — his own map drawn ~2000 years earlier. Renn was on his way to fulfill an old promise — to bury his friend Inetis. He dies weakened (he refused vampirism) and inattentive (watching Tami, not his surroundings). The pirates steal the map, Makita, and capture 7-year-old Tami.
- Participants: `char.renn`, `char.vix`, `char.kael`, `char.tami`
- Locations: `place.eastern_wilds`, `place.kito`
- Tags: `death`, `tragedy`, `inciting_incident`
- Source: `characters/Renn.md`, `characters/Renn_Vix_Kael.md`

### `evt.achilles.pentagram_protocol`
- Name: Protocol Pentagram (5 Nodes)
- Time: Era of Myths (precise dating TBD)
- Summary: The technical reality behind the pentagram symbol: 5 server nodes distributed across the planet imprisoning the Dark AI.
- Participants: `char.the_void`, `fac.archangels`
- Locations: `place.achilles`
- Tags: `technology`, `myth_vs_truth`
- Source: `world-bible.md`

## Pentalogy Plot (Story Events)

### `evt.story.max_awakens`
- Name: Maks's Awakening
- Time: AY ~3000+
- Summary: Maks awakens from cryosleep; the ship is destroyed, Inetis's module empty.
- Participants: `char.maksimilian`
- Locations: `place.ship_ark_exodus`, `place.achilles`
- Tags: `inciting_incident`, `mystery`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.story.meets_tami`
- Name: Meeting Tami
- Time: AY ~3000+
- Summary: Tami (airship captain) becomes Maks's guide in the post-apocalyptic world.
- Participants: `char.maksimilian`, `char.tami`
- Locations: `place.mainland`
- Tags: `alliance`
- Source: `world-bible.md`, `null-void-saga.md`
- Notes/TODO: Tami's age is inconsistent in the notes (~20 vs ~40).

### `evt.story.inetis_body_found`
- Name: Discovery of Inetis's Body
- Time: AY ~3000+
- Summary: Maks finds Inetis's skeleton and journals; discovers she let him sleep deliberately.
- Participants: `char.maksimilian`, `char.inetis`
- Locations: `place.cave_inetis`
- Tags: `twist`, `tragedy`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.story.tami_inherits_dust`
- Name: Transfer of "Hungry" Nanodrones to Tami
- Time: After `evt.story.inetis_body_found`
- Summary: Nanodrones from Inetis's remains pass to Tami; she gains abilities and memories.
- Participants: `char.tami`, `char.inetis`, `char.maksimilian`
- Locations: `place.cave_inetis`
- Tags: `transformation`, `Spira`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.story.samaell_confrontation`
- Name: Confrontation with Samaell
- Time: Book 1 (working)
- Summary: Battle with Samaell in the ruins; before death, he hints at Elania's existence.
- Participants: `char.maksimilian`, `char.samaell`
- Locations: `place.labs_ruins`
- Tags: `boss_fight`, `revelation`
- Source: `world-bible.md`

### `evt.story.kratos_campaign`
- Name: Northern Campaign (Grond)
- Time: Book 2 (working)
- Summary: Journey north and conflict with Grond; war and responsibility as theme.
- Participants: `char.maksimilian`, `char.tami`, `char.grom`
- Locations: `place.north`
- Tags: `war`
- Source: `world-bible.md`

### `evt.story.ishtar_campaign`
- Name: Southern Campaign (Ishtar)
- Time: Book 3 (working)
- Summary: Ishtar tortures Maks with illusions; revelation that the 4th Archangel is Elania.
- Participants: `char.maksimilian`, `char.tami`, `char.ishtar`, `char.elenia`
- Locations: `place.south`
- Tags: `psychological_warfare`, `revelation`
- Source: `world-bible.md`

### `evt.story.elenia_war`
- Name: Open War with Elania
- Time: Book 4 (working)
- Summary: Elania activates a Wraith army; Father vs. Daughter conflict.
- Participants: `char.maksimilian`, `char.tami`, `char.elenia`, `fac.wraiths`
- Locations: `place.achilles`
- Tags: `war`, `family`
- Source: `world-bible.md`

### `evt.story.doomsday_protocol`
- Name: Doomsday Protocol
- Time: Book 4 (working)
- Summary: Global nanodrone storm meant to erase all organic matter.
- Participants: `char.elenia`, `char.the_void`
- Locations: `place.achilles`
- Tags: `apocalypse`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.story.void_released`
- Name: Release of THE VOID
- Time: Book 4 (working)
- Summary: Destruction of the last Pentagram node releases the original destructive AI.
- Participants: `char.elenia`, `char.the_void`
- Locations: `place.achilles`, `place.core`
- Tags: `apocalypse`, `twist`
- Source: `world-bible.md`, `null-void-saga.md`

### `evt.story.max_upload`
- Name: Maks's Upload (Sacrifice)
- Time: Book 5 (working)
- Summary: Final battle in "Cyberspace"; Maks uploads his consciousness and rewrites the AI's code.
- Participants: `char.maksimilian`, `char.tami`, `char.elenia`, `char.the_void`
- Locations: `place.core`, `concept.cyberspace`
- Tags: `sacrifice`, `finale`
- Source: `world-bible.md`

### `evt.story.reconciliation`
- Name: Reconciliation and New Beginning
- Time: After Book 5
- Summary: Technology and nature intertwine; Tami leads the new society; Elania survives (redemption or mortality).
- Participants: `char.tami`, `char.elenia`, `char.maksimilian`
- Locations: `place.achilles`
- Tags: `epilogue`
- Source: `world-bible.md`
