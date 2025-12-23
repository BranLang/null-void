# The Pentagram Arc (Mermaid)

## Pentagram: Prečo to funguje (UI Metafora)

Inetis bola génius. Vedela, že nemôže vysvetľovať kvantovú fyziku a nanoinžinierstvo bežným ľuďom (alebo nesôr Chimérám). **Pentagram nie je magický symbol. Je to zjednodušené „užívateľské rozhranie“ (UI) pre ovládanie reality.**

Predstav si to ako operačný systém:
- **Pod povrchom**: Milióny riadkov kódu (nanoboty).
- **Na povrchu**: Ikony elementov, na ktoré „mág“ kliká svojou vôľou.

Inetis vytvorila tento systém, aby mohla učiť Elaniu bez toho, aby musela chápať matematiku za tým.

### Kultúrny a príbehový dopad
- **Elaniine kresby v jaskyni**: To, čo Kael pôvodne videl ako detské čmáranice a „šialené rovnice galaxií“, boli v skutočnosti Elaniine lekcie o manipulácii priestoru a času.
- **Chiméry**: Veria, že pentagram je posvätný symbol Hviezdnej Matky. Nerozumejú vede, nosia ho ako amulet.
- **Max (Skeptik)**: Cíti odpor k degradácii vedy na okultizmus. Inetisinu UI pomôcku vníma ako známku jej šialenstva v izolácii.
- **Archanjeli**: Pohŕdajú pentagramom ako „detskou hračkou“, pretože používajú abstraktnejšie a čistejšie rozhrania Citadely.

---

## Pentalógia: tok kníh (Pentagram)

```mermaid
graph TD
    %% Definicia uzlov
    B1(Kniha 1: ZEM<br>Prach)
    B2(Kniha 2: OHEŇ<br>Plamene Impéria)
    B3(Kniha 3: VODA<br>Slzy Matky)
    B4(Kniha 4: VZDUCH<br>Búrka Strojov)
    B5(Kniha 5: KVINTESENCIA<br>Null Void)

    %% Vztahy a tok pribehu
    B1 -->|Hľadanie pravdy| B2
    B2 -->|Odhalenie minulosti| B3
    B3 -->|Konfrontácia s rodinou| B4
    B4 -->|Apokalypsa| B5
    B5 -->|Nový Začiatok| B1

    %% Styling (Cyberpunk farby)
    style B1 fill:#4a3b3b,stroke:#f00,stroke-width:2px,color:#fff
    style B2 fill:#802b00,stroke:#f00,stroke-width:2px,color:#fff
    style B3 fill:#003366,stroke:#f00,stroke-width:2px,color:#fff
    style B4 fill:#2d2d2d,stroke:#f00,stroke-width:2px,color:#fff
    style B5 fill:#000000,stroke:#0ff,stroke-width:4px,color:#fff,stroke-dasharray: 5 5
```

## Systém: THE VOID (core) a archanjeli




```mermaid
graph BT
    %% Definicie
    subgraph "THE NULL VOID (Root Access)"
        AI((THE VOID<br>Corrupted Core AI))
    end

    subgraph "THE GATEKEEPER (Admin)"
        ELENIA[ELENIA<br>Archanjel Zradenej Krvi<br>Dcéra Maxa & Inetis]
    end

    subgraph "THE EXECUTORS (Services)"
        AZ[samaell<br>Archanjel Tieňov<br>Lokácia: Labs]
        KR[KRATOS<br>Archanjel Vojny<br>Lokácia: Sever]
        IS[ISHTAR<br>Archanjel Pôžitku<br>Lokácia: Juh]
    end

    subgraph "THE HOSTS (Hardware)"
        GHOSTS(Armáda Duchov<br>Nanodrone Wraiths)
        CULT(Kult Matky<br>Ľudskí prisluhovači)
    end

    %% Prepojenia
    AI -->|Ovláda| ELENIA
    ELENIA -->|Rozkazuje| AZ
    ELENIA -->|Rozkazuje| KR
    ELENIA -->|Rozkazuje| IS
    
    AZ -->|Programuje| GHOSTS
    KR -->|Velí| GHOSTS
    IS -->|Manipuluje| CULT

    %% Styling
    style AI fill:#000,stroke:#f00,stroke-width:4px,color:#fff
    style ELENIA fill:#330000,stroke:#f00,stroke-width:2px,color:#fff
```
