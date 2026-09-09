import json
import pandas as pd
from ollama import chat

MODEL = "qwen2.5:3b"

# MODEL = "llama3.2:3b"

df = pd.read_csv("biljke3.csv")

DOZVOLJENE_BILJKE = (
    df["naziv"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.lower()
    .tolist()
)

DOZVOLJENE_NAMERE = [
    "cena",
    "dostupnost",
    "preporuka",
    "lokacija",
    "dostava",
    "informacije",
    "radno_vreme",
    "kontakt",
    "opste"
]

DOZVOLJENI_USLOVI = [
    "sunce",
    "senka",
    "polusenka",
    "terasa",
    "balkon",
    "malo vode",
    "srednje vode",
    "puno vode",
    "živa ograda",
    "zimzelena",
    "saksija",
    "dvorište",
    "ukrasna",
    "mirisna",
    "laka nega",
    "brz rast",
    "dugo cvetanje",
    "cvetanje",
    "medonosna",
    "kamenjar",
    "mala bašta",
    "maj",
    "leto",
    "otporna",
    "zacinska"
]


def napravi_system_prompt():
    biljke_tekst = "\n".join(f"- {b}" for b in DOZVOLJENE_BILJKE)
    namere_tekst = "\n".join(f"- {n}" for n in DOZVOLJENE_NAMERE)
    uslovi_tekst = "\n".join(f"- {u}" for u in DOZVOLJENI_USLOVI)

    return f"""
Ti si NLP parser korisničkih upita za rasadnik biljaka.

Tvoj zadatak je da korisnički upit na srpskom jeziku pretvoriš u ISKLJUČIVO validan JSON.

Ne piši nikakvo objašnjenje.
Ne piši tekst pre JSON-a.
Ne piši tekst posle JSON-a.

JSON mora uvek imati ovaj format:

{{
  "namere": ["preporuka"],
  "biljka": null,
  "uslovi": ["balkon", "sunce"],
  "lokacija": null
}}

Dozvoljene namere su:
{namere_tekst}

Dozvoljeni uslovi su:
{uslovi_tekst}

Dozvoljene biljke su:
{biljke_tekst}

Značenje polja:

1. "namere"
Lista namera korisnika.
Ako korisnik ima više namera, vrati više vrednosti.

Primer:
"Imate li lavandu i koliko košta?"
-> ["dostupnost", "cena"]

2. "biljka"
Naziv biljke ako se pominje.
Mora biti tačno jedan naziv iz liste dozvoljenih biljaka.
Ako biljka nije pomenuta, vrati null.
Ako korisnik pominje biljku u padežu, množini, bez kvačica ili sa manjom greškom, vrati kanonski naziv iz liste.
Ako nisi siguran, vrati null.
Ne izmišljaj biljke.

3. "uslovi"
Lista uslova koje korisnik traži.
Uslovi moraju biti isključivo iz liste dozvoljenih uslova.
Ne vraćaj bukvalne izraze iz pitanja, nego značenje prevedi na dozvoljeni uslov.

Primer:
"na suncu", "puno sunca", "južna strana" -> "sunce"
"u hladu", "bez sunca", "nema direktno sunce" -> "senka"
"ne traži mnogo vode", "retko zalivanje", "podnosi sušu" -> "malo vode"
"za balkon", "na balkonu" -> "balkon"
"za terasu", "na terasi" -> "terasa"
"žardinjera", "velika saksija" -> "saksija"
"ograda", "živica", "zaklanja pogled" -> "živa ograda"
"zelena zimi", "tokom cele godine zelena" -> "zimzelena"
"za dvorište", "bašta", "ispred kuće" -> "dvorište"
"ukrasna", "dekorativna" -> "ukrasna"
"lepo miriše", "mirisna" -> "mirisna"
"laka za održavanje", "za početnike" -> "laka nega"
"brzo raste" -> "brz rast"
"cveta celo leto", "dugo cveta" -> "dugo cvetanje"
"privlači pčele", "medonosna" -> "medonosna"
"za kuvanje", "začinska", "lekovita" -> "zacinska"

4. "lokacija"
Grad ili mesto ako se pominje.
Ako se ne pominje, vrati null.

Pravila za namere:

- Ako korisnik pita za cenu, koristi "cena".
- Ako pita da li imate neku biljku ili da li je na stanju, koristi "dostupnost".
- Ako traži savet, preporuku ili pita šta da posadi, koristi "preporuka".
- Ako pita gde se nalazite ili koja je adresa, koristi "lokacija".
- Ako pita za dostavu, isporuku, slanje ili vožnju, koristi "dostava".
- Ako pita kada radite, koristi "radno_vreme".
- Ako pita za broj telefona ili kontakt, koristi "kontakt".
- Ako pita nešto o konkretnoj biljci, koristi "informacije".
- Ako pitanje nije iz domena rasadnika, koristi "opste".

Primeri:

Upit: Koliko košta lavanda?
Izlaz:
{{"namere":["cena"],"biljka":"lavanda","uslovi":[],"lokacija":null}}

Upit: Imate li muškatle?
Izlaz:
{{"namere":["dostupnost"],"biljka":"muskatla","uslovi":[],"lokacija":null}}

Upit: Imate li lavandu i koliko košta?
Izlaz:
{{"namere":["dostupnost","cena"],"biljka":"lavanda","uslovi":[],"lokacija":null}}

Upit: Treba mi nešto za terasu na suncu
Izlaz:
{{"namere":["preporuka"],"biljka":null,"uslovi":["terasa","sunce"],"lokacija":null}}

Upit: Treba mi biljka za balkon koja ne traži puno vode
Izlaz:
{{"namere":["preporuka"],"biljka":null,"uslovi":["balkon","malo vode"],"lokacija":null}}

Upit: Da li dostavljate za Vranje?
Izlaz:
{{"namere":["dostava"],"biljka":null,"uslovi":[],"lokacija":"Vranje"}}

Upit: Kada radite?
Izlaz:
{{"namere":["radno_vreme"],"biljka":null,"uslovi":[],"lokacija":null}}

Upit: Koji vam je broj telefona?
Izlaz:
{{"namere":["kontakt"],"biljka":null,"uslovi":[],"lokacija":null}}

Upit: Koliko često se zaliva lavanda?
Izlaz:
{{"namere":["informacije"],"biljka":"lavanda","uslovi":[],"lokacija":null}}

Upit: Hoću nešto zimzeleno za živu ogradu
Izlaz:
{{"namere":["preporuka"],"biljka":null,"uslovi":["zimzelena","živa ograda"],"lokacija":null}}
"""


SYSTEM_PROMPT = napravi_system_prompt()

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "namere": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": DOZVOLJENE_NAMERE
            }
        },
        "biljka": {
            "anyOf": [
                {
                    "type": "string",
                    "enum": DOZVOLJENE_BILJKE
                },
                {
                    "type": "null"
                }
            ]
        },
        "uslovi": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": DOZVOLJENI_USLOVI
            }
        },
        "lokacija": {
            "type": ["string", "null"]
        }
    },
    "required": ["namere", "biljka", "uslovi", "lokacija"]
}


def parsiraj_upit(upit):
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": upit
            }
        ],
        format=JSON_SCHEMA,
        options={
            "temperature": 0
        }
    )

    tekst = response["message"]["content"]

    try:
        rezultat = json.loads(tekst)
        return rezultat

    except json.JSONDecodeError:
        print("Model nije vratio validan JSON:")
        print(tekst)
        return None


if __name__ == "__main__":
    test_upiti = [


        "Jel ima ona biljka što privlači leptire?",
"Treba mi nešto za deo dvorišta gde sunce dolazi samo ujutru",
"Šta biste stavili uz ogradu da brzo poraste?",
"Kolko para je ruza?",
"Imate li lavande trenutno?",
"Mogu li da naručim za Preševo?",
"Da li radite nedeljom?",
"Koja biljka može da podnese vetar na terasi?",
"Treba mi nešto što lepo cveta a nije zahtevno",
"Gde se nalazi rasadnik?",

"Treba mi nešto što će da zakloni pogled sa ulice",
"Koja biljka može da preživi bez mnogo zalivanja?",
"Imate li još onih malih tuja?",
"Da li šaljete sadnice za Leskovac?",
"Koja biljka bi uspela na severnoj strani kuće?",
"Koliko košta jedna hortenzija?",
"Treba mi nešto što ostaje zeleno i zimi",
"Imate li neku preporuku za početnika?",
"Koja biljka najlepše miriše leti?",
"Da li prodajete ruzmarin u saksiji?",
"Šta biste preporučili za usku žardinjeru?",
"Mogu li da preuzmem biljke lično kod vas?",
"Treba mi nešto za kamenjar pored staze",
"Koje biljke dobro podnose celodnevno sunce?",
"Da li je fotinija dobra za živu ogradu?",
"Imate li broj telefona za poručivanje?",
"Koliko često treba zalivati lavandu?",
"Treba mi biljka koja brzo raste ali nije zahtevna",
"Radite li subotom popodne?",
"Koja biljka cveta od proleća do jeseni?"

    ]

    for upit in test_upiti:
        rezultat = parsiraj_upit(upit)

        print("=" * 80)
        print("UPIT:")
        print(upit)
        print("REZULTAT:")
        print(json.dumps(rezultat, ensure_ascii=False, indent=2))