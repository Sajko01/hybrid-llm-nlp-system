import json
import re
import unicodedata
import pandas as pd
from ollama import chat

# MODEL = "llama3.2:3b"
MODEL = "qwen2.5:3b"


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
    "cena", "dostupnost", "preporuka", "lokacija",
    "dostava", "informacije", "radno_vreme", "kontakt", "opste"
]

DOZVOLJENI_USLOVI = [
    "sunce", "senka", "polusenka", "terasa", "balkon",
    "malo vode", "srednje vode", "puno vode",
    "živa ograda", "zimzelena", "saksija", "dvorište",
    "ukrasna", "mirisna", "laka nega", "brz rast",
    "dugo cvetanje", "cvetanje", "medonosna", "kamenjar",
    "mala bašta", "maj", "leto", "otporna", "zacinska"
]


def normalizuj_tekst(tekst):
    if tekst is None:
        return ""

    tekst = str(tekst).lower().strip()
    tekst = unicodedata.normalize("NFD", tekst)
    tekst = "".join(ch for ch in tekst if unicodedata.category(ch) != "Mn")
    tekst = tekst.replace("đ", "dj")
    tekst = re.sub(r"[^\w\s]", " ", tekst)
    tekst = re.sub(r"\s+", " ", tekst)

    return tekst.strip()


def sadrzi(tekst_norm, fraza):
    fraza_norm = normalizuj_tekst(fraza)
    return re.search(r"\b" + re.escape(fraza_norm) + r"\b", tekst_norm) is not None


def dodaj(lista, vrednost):
    if vrednost not in lista:
        lista.append(vrednost)


MAPA_BILJAKA = {
    "lavanda": "lavanda", "lavande": "lavanda", "lavandu": "lavanda",
    "muskatla": "muskatla", "muskatle": "muskatla", "muskatlu": "muskatla",
    "muškatla": "muskatla", "muškatle": "muskatla", "muškatlu": "muskatla",

    "petunija": "petunija", "petunije": "petunija", "petuniju": "petunija",
    "begonija": "begonija", "begonije": "begonija", "begoniju": "begonija",

    "tuja": "tuja smaragd", "tuje": "tuja smaragd", "tuju": "tuja smaragd",
    "tuja smaragd": "tuja smaragd", "smaragd": "tuja smaragd",
    "tuja brabant": "tuja brabant", "brabant": "tuja brabant",

    "ruzmarin": "ruzmarin", "ruzmarina": "ruzmarin", "ruzmarinu": "ruzmarin",
    "ruža": "ruža", "ruže": "ruža", "ružu": "ruža", "ruza": "ruža", "ruze": "ruža",
    "hortenzija": "hortenzija", "hortenzije": "hortenzija", "hortenziju": "hortenzija",
    "lovor višnja": "lovor višnja", "lovor visnja": "lovor višnja",
    "lovor višnje": "lovor višnja", "lovor visnje": "lovor višnja",
    "maćuhica": "maćuhica", "macuhica": "maćuhica",
    "šimšir": "šimšir", "simsir": "šimšir", "simšir": "šimšir",
    "nana": "nana", "menta": "nana",
    "žalfija": "žalfija", "zalfija": "žalfija",
    "timijan": "timijan", "majčina dušica": "timijan", "majcina dusica": "timijan",
    "origano": "origano",
    "kleka": "kleka", "tisa": "tisa", "leylandii": "leylandii",
    "fotinija": "fotinija", "hibiskus": "hibiskus",
    "surfinija": "surfinija", "kadifica": "kadifica",
    "verbena": "verbena", "vinka": "vinka", "lobelija": "lobelija",
    "gazanija": "gazanija", "salvija": "salvija", "dalija": "dalija",
    "hrizantema": "hrizantema", "japanska dunja": "japanska dunja",
    "javor kuglasti": "javor kuglasti", "breza": "breza",
    "katalpa": "katalpa", "kuglasti bagrem": "kuglasti bagrem",
    "crveni javor": "crveni javor", "ukrasna trešnja": "ukrasna trešnja"
}


MAPIRANJE_USLOVA = {
    "sunce": "sunce", "suncu": "sunce", "sunčano": "sunce", "suncano": "sunce",
    "sunčano mesto": "sunce", "suncano mesto": "sunce",
    "puno sunca": "sunce", "mnogo sunca": "sunce", "podnosi puno sunca": "sunce",

    "hlad": "senka", "hladu": "senka", "hladovina": "senka",
    "hladovinu": "senka", "senka": "senka", "senci": "senka", "u senci": "senka",
    "senku": "senka", "bez sunca": "senka",

    "polusenka": "polusenka", "polusenci": "polusenka",

    "malo vode": "malo vode", "ne traži puno vode": "malo vode",
    "ne trazi puno vode": "malo vode", "ne traži mnogo vode": "malo vode",
    "ne trazi mnogo vode": "malo vode", "malo zalivanja": "malo vode",

    "puno vode": "puno vode", "mnogo vode": "puno vode", "traži puno vode": "puno vode",
    "trazi puno vode": "puno vode",

    "terasa": "terasa", "terasi": "terasa",
    "balkon": "balkon", "balkonu": "balkon",

    "saksija": "saksija", "saksiju": "saksija",
    "žardinjera": "saksija", "žardinjeru": "saksija",
    "zardinjera": "saksija", "zardinjeru": "saksija",

    "živa ograda": "živa ograda", "ziva ograda": "živa ograda",
    "živu ogradu": "živa ograda", "zivu ogradu": "živa ograda",
    "živica": "živa ograda", "živicu": "živa ograda",
    "zivica": "živa ograda", "zivicu": "živa ograda",

    "zimzelena": "zimzelena", "zimzeleno": "zimzelena", "zimzelenu": "zimzelena",

    "dvorište": "dvorište", "dvorištu": "dvorište", "dvoriste": "dvorište",
    "dvoristu": "dvorište", "malo dvorište": "mala bašta", "malo dvoriste": "mala bašta",
    "mala bašta": "mala bašta", "mala basta": "mala bašta",

    "ukrasna": "ukrasna", "ukrasne": "ukrasna", "ukrasno": "ukrasna",
    "mirisna": "mirisna", "lepo miriše": "mirisna", "lepo mirise": "mirisna",

    "laka nega": "laka nega", "lako održavanje": "laka nega",
    "lako odrzavanje": "laka nega",

    "brz rast": "brz rast", "brzo raste": "brz rast",

    "dugo cvetanje": "dugo cvetanje", "dugo cveta": "dugo cvetanje",
    "cvetanje": "cvetanje", "cvetna": "cvetanje",

    "pčele": "medonosna", "pcele": "medonosna", "medonosna": "medonosna",

    "kamenjar": "kamenjar", "kamenjaru": "kamenjar",

    "maj": "maj", "maju": "maj", "leto": "leto", "leta": "leto",

    "otporna": "otporna", "otporne": "otporna", "vetar": "otporna",

    "začinska": "zacinska", "zacinska": "zacinska", "lekovita": "zacinska"
}


MAPA_LOKACIJA = {
    "vranje": "Vranje", "vranju": "Vranje",
    "bujanovac": "Bujanovac", "bujanovcu": "Bujanovac",
    "surdulica": "Surdulica", "surdulicu": "Surdulica",
    "preševo": "Preševo", "presevo": "Preševo",
    "vladičin han": "Vladičin Han", "vladicin han": "Vladičin Han",
    "leskovac": "Leskovac", "leskovcu": "Leskovac",
    "niš": "Niš", "nis": "Niš"
}


def napravi_system_prompt():
    return f"""
Ti si NLP parser za korisničke upite rasadnika biljaka.

Vrati isključivo validan JSON:
{{
  "namere": [],
  "biljka": null,
  "uslovi": [],
  "lokacija": null
}}

Dozvoljene namere: {DOZVOLJENE_NAMERE}
Dozvoljene biljke: {DOZVOLJENE_BILJKE}
Dozvoljeni uslovi: {DOZVOLJENI_USLOVI}

Pravila:
- Ako korisnik traži cenu, dodaj "cena".
- Ako pita da li imate/prodajete/dostupno je, dodaj "dostupnost".
- Ako pita za dostavu/slanje/isporuku, dodaj "dostava".
- Ako pita za adresu ili gde se nalazite, dodaj "lokacija".
- Ako pita kada radite/otvarate, dodaj "radno_vreme".
- Ako pita kako da vas pozove/kontaktira, dodaj "kontakt".
- Ako traži savet/preporuku, dodaj "preporuka".
- Ako pita o nezi, zalivanju, rastu ili osobinama konkretne biljke, dodaj "informacije".
- Ako je pitanje van domena rasadnika, vrati ["opste"].
- Ne izmišljaj biljku kod preporuke ako korisnik nije naveo konkretnu biljku.
- Ne izmišljaj lokaciju ako nije pomenuta.
- Ne dodaj uslove koji nemaju veze sa upitom.

Upit: Koliko košta lavanda?
Izlaz:
{{"namere":["cena"],"biljka":"lavanda","uslovi":[],"lokacija":null}}

"""


SYSTEM_PROMPT = napravi_system_prompt()

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "namere": {
            "type": "array",
            "items": {"type": "string", "enum": DOZVOLJENE_NAMERE}
        },
        "biljka": {
            "anyOf": [
                {"type": "string", "enum": DOZVOLJENE_BILJKE},
                {"type": "null"}
            ]
        },
        "uslovi": {
            "type": "array",
            "items": {"type": "string", "enum": DOZVOLJENI_USLOVI}
        },
        "lokacija": {"type": ["string", "null"]}
    },
    "required": ["namere", "biljka", "uslovi", "lokacija"]
}


def pozovi_llm(upit):
    try:
        response = chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": upit}
            ],
            format=JSON_SCHEMA,
            options={"temperature": 0}
        )

        return json.loads(response["message"]["content"])

    except Exception:
        return {
            "namere": [],
            "biljka": None,
            "uslovi": [],
            "lokacija": None
        }


def biljka_iz_upita(upit):
    tekst = normalizuj_tekst(upit)

    for forma, biljka in sorted(MAPA_BILJAKA.items(), key=lambda x: len(x[0]), reverse=True):
        if sadrzi(tekst, forma) and biljka in DOZVOLJENE_BILJKE:
            return biljka

    return None


def uslovi_iz_upita_rules(upit):
    tekst = normalizuj_tekst(upit)
    uslovi = []

    for fraza, uslov in sorted(MAPIRANJE_USLOVA.items(), key=lambda x: len(x[0]), reverse=True):
        if sadrzi(tekst, fraza) and uslov in DOZVOLJENI_USLOVI:
            dodaj(uslovi, uslov)

    if "malo vode" in uslovi and "puno vode" in uslovi:
        if any(sadrzi(tekst, f) for f in ["ne trazi puno vode", "ne trazi mnogo vode", "ne traži puno vode"]):
            uslovi.remove("puno vode")

    if "mala bašta" in uslovi and "dvorište" in uslovi:
        uslovi.remove("dvorište")

    return uslovi


def lokacija_iz_upita(upit):
    tekst = normalizuj_tekst(upit)

    for forma, lokacija in sorted(MAPA_LOKACIJA.items(), key=lambda x: len(x[0]), reverse=True):
        if sadrzi(tekst, forma):
            return lokacija

    return None


def namere_rules(upit, biljka):
    tekst = normalizuj_tekst(upit)
    namere = []

    if any(sadrzi(tekst, f) for f in ["posto", "koliko kosta", "cena", "kolika je cena"]):
        dodaj(namere, "cena")

    if any(sadrzi(tekst, f) for f in ["imate li", "da li imate", "prodajete", "prodajete li", "dostupna", "dostupno", "na stanju"]):
        dodaj(namere, "dostupnost")

    if any(sadrzi(tekst, f) for f in ["dostava", "dostavljate", "dostavite", "vrsite dostavu", "poslati", "posaljete", "isporuka"]):
        dodaj(namere, "dostava")

    if any(sadrzi(tekst, f) for f in ["gde se nalazite", "gde ste", "adresa", "adresi", "na kojoj adresi", "kako da dodjem"]):
        dodaj(namere, "lokacija")

    if any(sadrzi(tekst, f) for f in ["kada radite", "kad radite", "radno vreme", "radite li", "otvarate", "kada otvarate", "subotom"]):
        dodaj(namere, "radno_vreme")

    if any(sadrzi(tekst, f) for f in ["telefon", "kontakt", "pozovem", "pozvati", "kako mogu da vas pozovem"]):
        dodaj(namere, "kontakt")

    if any(sadrzi(tekst, f) for f in ["treba mi", "zelim", "trazim", "preporuka", "preporucujete", "koja biljka", "sta da posadim"]):
        dodaj(namere, "preporuka")

    if biljka is not None and any(sadrzi(tekst, f) for f in ["kako se neguje", "neguje", "nega", "trazi puno vode", "traži puno vode", "koliko se zaliva", "koliko vode"]):
        dodaj(namere, "informacije")

    return namere


def spoji_namere(upit, llm_rezultat, biljka):
    llm_namere = [
        n for n in llm_rezultat.get("namere", [])
        if n in DOZVOLJENE_NAMERE
    ]

    rule_namere = namere_rules(upit, biljka)

    namere = []

    for n in llm_namere:
        dodaj(namere, n)

    for n in rule_namere:
        dodaj(namere, n)

    if "opste" in namere and len(namere) > 1:
        namere.remove("opste")

    if not namere:
        namere = ["opste"]

    return namere


def finalna_biljka(upit, llm_rezultat):
    biljka_rules = biljka_iz_upita(upit)

    if biljka_rules is not None:
        return biljka_rules

    biljka_llm = llm_rezultat.get("biljka")

    if biljka_llm is None:
        return None

    biljka_llm = str(biljka_llm).lower().strip()

    tekst = normalizuj_tekst(upit)

    # Ako korisnik traži opštu preporuku, LLM ne sme da bira konkretnu biljku.
    if any(sadrzi(tekst, f) for f in ["treba mi", "zelim", "trazim", "preporuka", "koja biljka", "sta da posadim"]):
        return None

    if biljka_llm in DOZVOLJENE_BILJKE:
        return biljka_llm

    return None


def finalni_uslovi(upit, llm_rezultat, namere):
    if any(n in namere for n in ["cena", "dostupnost", "dostava", "lokacija", "radno_vreme", "kontakt", "opste", "informacije"]):
        return []

    uslovi = []

    # 1. Prvo zadrži LLM uslove ako su dozvoljeni
    for u in llm_rezultat.get("uslovi", []):
        u = str(u).lower().strip()
        if u in DOZVOLJENI_USLOVI:
            dodaj(uslovi, u)

    # 2. Zatim dopuni rules uslovima
    for u in uslovi_iz_upita_rules(upit):
        dodaj(uslovi, u)

    # 3. Očisti kontradikcije
    if "malo vode" in uslovi and "puno vode" in uslovi:
        tekst = normalizuj_tekst(upit)
        if any(sadrzi(tekst, f) for f in ["ne trazi puno vode", "ne trazi mnogo vode", "ne traži puno vode"]):
            uslovi.remove("puno vode")

    if "mala bašta" in uslovi and "dvorište" in uslovi:
        uslovi.remove("dvorište")

    return uslovi


def finalna_lokacija(upit, llm_rezultat, namere):
    lok_rules = lokacija_iz_upita(upit)

    if lok_rules is not None:
        return lok_rules

    lok_llm = llm_rezultat.get("lokacija")

    if lok_llm is None:
        return None

    lok_llm_norm = normalizuj_tekst(lok_llm)

    zabranjene = ["srbija", "beograd", "opste", "nije navedeno", "rasadnik"]

    if lok_llm_norm in zabranjene:
        return None

    if "dostava" in namere:
        return str(lok_llm).strip().title()

    return None


def parsiraj_upit(upit):
    llm_rezultat = pozovi_llm(upit)

    biljka = finalna_biljka(upit, llm_rezultat)
    namere = spoji_namere(upit, llm_rezultat, biljka)
    uslovi = finalni_uslovi(upit, llm_rezultat, namere)
    lokacija = finalna_lokacija(upit, llm_rezultat, namere)

    rezultat = {
        "namere": namere,
        "biljka": biljka,
        "uslovi": uslovi,
        "lokacija": lokacija,
        "namera": namere[0]
    }

    return rezultat


if __name__ == "__main__":
    test_upiti = [
        # "Želim biljku za žardinjeru na terasi",
        # "Imate li ukrasne biljke za sunčano mesto?",
        # "Da li prodajete lovor višnju?",
        # "Kolika je cena muškatle?",
        # "Dostavljate li u Vladičin Han?",
        # "Na kojoj adresi se nalazite?",
        # "Kada otvarate ujutru?",
        # "Kako mogu da vas pozovem?",
        # "Da li ruzmarin traži puno vode?",
        # "Preporuka za zimzelenu živicu?",
        # "Imate li hortenzije?",
        # "Koja biljka uspeva u senci?",
        # "Može li dostava za Leskovac?",
        # "Šta preporučujete za malo dvorište?",
        # "Koliko je visok Kopaonik?"

        
    # "Treba mi nešto što će lepo izgledati pored kapije",
    # "Koje biljke podnose baš jaku žežu leti?",
    # "Imate li možda još ostalo nešto od žalfije?",
    # "Da li šaljete sadnice za Vladičin Han?",
    # "Koliko izađe jedna fotinija visine oko 80 cm?",
    # "Treba mi nešto što neće da se osuši ako zaboravim zalivanje",
    # "Gde vas mogu pronaći?",
    # "Radite li sutra popodne?",
    # "Hteo bih neku biljku koja miriše kada procveta",
    # "Da li lovor višnja može da ide uz ogradu?",
    # "Koja biljka je dobra za pčele?",
    # "Imate li broj mobilnog?",
    # "Šta biste preporučili za mesto koje je ceo dan na suncu?",
    # "Može li porudžbina za Bujanovac?",
    # "Da li je ostala neka hortenzija?",
    # "Treba mi nešto za žardinjeru",
    # "Kako održavati lavandu tokom leta?",
    # "Hoće li tuja smaragd uspeti u saksiji?",
    # "Koje biljke brzo zatvaraju pogled od komšija?",
    # "Tražim nešto za mali prostor ispred kuće",
    # "Da li prodajete ruzmarin?",
    # "Koliko često treba zalivati muškatle?",
    # "Imate li nešto što ostaje zeleno cele godine?",
    # "Šta bi moglo da uspeva na severnoj strani kuće?",
    # "Da li radite vikendom?",
    # "Treba mi nešto dekorativno za balkon",
    # "Može li dostava za Leskovac?",
    # "Imate li biljke koje ne zahtevaju puno pažnje?",
    # "Koja biljka cveta najduže?",
    # "Koliko stanovnika ima Niš?"
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