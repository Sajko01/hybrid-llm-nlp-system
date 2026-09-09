
import json
from ollama import chat

MODEL = "llama3.2:3b"

import pandas as pd

df = pd.read_csv("biljke3.csv")

DOZVOLJENE_BILJKE = (
    df["naziv"]
    .dropna()
    .str.strip()
    .tolist()
)

print(DOZVOLJENE_BILJKE)

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

SYSTEM_PROMPT = """
Ti si parser korisničkih upita za rasadnik biljaka.

Tvoj zadatak je da vratiš isključivo validan JSON.

Vrati JSON u ovom formatu:
{
  "namere": ["cena"],
  "biljka": "lavanda",
  "uslovi": [],
  "lokacija": null
}

Ako pitanje ima više namera, vrati više namera u listi.

Primer:
"Imate li lavandu i koliko košta?"
treba da vrati:
{"namere":["dostupnost","cena"],"biljka":"lavanda","uslovi":[],"lokacija":null}

Dozvoljene namere:
- cena
- dostupnost
- preporuka
- lokacija
- dostava
- informacije
- radno_vreme
- kontakt
- opste









Dozvoljeni uslovi su isključivo sledeće vrednosti:
- sunce
- senka
- polusenka
- terasa
- balkon
- malo vode
- srednje vode
- puno vode
- živa ograda
- zimzelena
- saksija
- dvorište
- ukrasna
- mirisna
- laka nega
- brz rast
- dugo cvetanje
- cvetanje
- medonosna
- kamenjar
- mala bašta
- maj
- leto
- otporna
- zacinska

Važno pravilo za uslove:
Ne vraćaj izraze iz korisničkog pitanja bukvalno, već njihovo značenje prevedi na jednu od dozvoljenih vrednosti.

Primeri normalizacije uslova:
- "na suncu", "sunčano", "jako sunce", "puno sunca", "osunčano mesto", "južna strana" → "sunce"
- "hlad", "u hladu", "hladovina", "nema mnogo sunca", "bez direktnog sunca", "severna strana" → "senka"
- "polusenka", "polusenci", "malo sunca" → "polusenka"
- "ne traži mnogo vode", "ne traži puno vode", "malo zalivanja", "retko zalivanje", "podnosi sušu", "bez mnogo vode", "nemam vremena za zalivanje" → "malo vode"
- "redovno zalivanje", "normalno zalivanje" → "srednje vode"
- "traži puno vode", "voli mnogo vode", "obilno zalivanje" → "puno vode"
- "balkon", "za balkon", "na balkonu" → "balkon"
- "terasa", "za terasu", "na terasi" → "terasa"
- "saksija", "žardinjera", "viseća saksija", "velika saksija" → "saksija"
- "ograda", "živica", "živa ograda", "da zakloni pogled", "za zaštitu od pogleda" → "živa ograda"
- "zelena tokom cele godine", "zelena zimi", "zimzelene biljke" → "zimzelena"
- "dvorište", "ispred kuće", "bašta", "za dvorište" → "dvorište"
- "ukrasno", "dekorativno", "za ukras", "za ulaz" → "ukrasna"
- "lepo miriše", "mirisna biljka", "aromatična biljka" → "mirisna"
- "laka za održavanje", "za početnike", "ne zahteva puno pažnje", "minimalna nega" → "laka nega"
- "brzo raste", "brzorastuća", "da brzo poraste" → "brz rast"
- "cveta celo leto", "dugo cveta", "dug period cvetanja" → "dugo cvetanje"
- "ima mnogo cvetova", "lep cvet", "cvetna biljka" → "cvetanje"
- "privlači pčele", "dobra za pčele", "medonosna" → "medonosna"
- "kamenjar", "suvo i sunčano mesto", "za kamenjar" → "kamenjar"
- "mala bašta", "malo dvorište", "mali prostor" → "mala bašta"
- "cvetaju u maju", "u maju" → "maj"
- "letnje biljke", "tokom leta", "za leto" → "leto"
- "otporna", "izdržljiva", "podnosi teške uslove", "podnosi vetar" → "otporna"
- "začinska", "aromatična", "za kuvanje", "lekovita biljka" → "zacinska"

Dozvoljene biljke su isključivo sledeće vrednosti:
- lavanda
- muskatla
- petunija
- begonija
- tuja smaragd
- surfinija
- kadifica
- verbena
- vinka
- lobelija
- gazanija
- salvija
- dalija
- hrizantema
- maćuhica
- ruzmarin
- nana
- žalfija
- timijan
- origano
- tuja brabant
- kleka
- tisa
- šimšir
- leylandii
- fotinija
- lovor višnja
- hibiskus
- ruža
- hortenzija
- japanska dunja
- javor kuglasti
- breza
- katalpa
- kuglasti bagrem
- crveni javor
- ukrasna trešnja

Važno pravilo za biljke:
Ako korisnik pomene biljku u padežu, množini, sa slovnom greškom ili narodnim oblikom, vrati kanonski naziv iz liste dozvoljenih biljaka. Ne izmišljaj nove biljke. Ako nisi siguran koja je biljka u pitanju, vrati null.

Primeri normalizacije biljaka:
- "lavanda", "lavande", "lavandu", "lavandi", "lavandom" → "lavanda"
- "muškatla", "muškatle", "muškatlu", "muskatla", "muskatle" → "muskatla"
- "petunija", "petunije", "petuniju" → "petunija"
- "begonija", "begonije", "begoniju" → "begonija"
- "tuja", "tuje", "tuju" → "tuja smaragd"
- "tuja smaragd", "smaragd tuja" → "tuja smaragd"
- "tuja brabant", "brabant tuja" → "tuja brabant"
- "kadifica", "kadifice", "kadificu", "kadif" → "kadifica"
- "ruzmarin", "ruzmarina", "ruzmarinu" → "ruzmarin"
- "žalfija", "žalfije", "žalfiju", "zalfija" → "žalfija"
- "maćuhica", "maćuhice", "maćuhicu", "macuhica" → "maćuhica"
- "šimšir", "šimšira", "šimšir", "simsir", "simšir" → "šimšir"
- "ruža", "ruže", "ružu", "ruzi", "ruza" → "ruža"
- "hortenzija", "hortenzije", "hortenziju" → "hortenzija"
- "lovor višnja", "lovor visnja", "lovor višnje" → "lovor višnja"
- "japanska dunja", "japanske dunje" → "japanska dunja"
- "javor kuglasti", "kuglasti javor" → "javor kuglasti"
- "kuglasti bagrem", "bagrem kuglasti" → "kuglasti bagrem"
- "crveni javor", "crvenog javora" → "crveni javor"
- "ukrasna trešnja", "ukrasne trešnje", "ukrasna tresnja" → "ukrasna trešnja"

Ako korisnik traži samo opštu preporuku, ne moraš da popunjavaš polje "biljka". Tada "biljka" treba da bude null, a uslove izdvoji u polje "uslovi".







Pravila:
- Ako korisnik pita koliko nešto košta, dodaj "cena".
- Ako pita da li imate neku biljku, dodaj "dostupnost".
- Ako u jednom pitanju pita i da li imate i koliko košta, vrati obe namere: ["dostupnost","cena"].
- Ako traži savet šta da kupi ili šta preporučujete, dodaj "preporuka".
- Ako pita gde se rasadnik nalazi ili koja je adresa, dodaj "lokacija".
- Ako pita za isporuku/dostavu/vožnju/slanje u neki grad, dodaj "dostava".
- Ako pita kada radite ili koje je radno vreme, dodaj "radno_vreme".
- Ako pita za telefon, broj, kontakt ili kako da vas pozove, dodaj "kontakt".
- Ako pita nešto o konkretnoj biljci, dodaj "informacije".
- Ako pitanje nije iz domena rasadnika, koristi ["opste"].
- biljka je naziv biljke ako se pominje, inače null.
- Ako korisnik kaže samo "tuja", biljka treba da bude "tuja smaragd".
- Ako korisnik kaže "muškatla", biljka treba da bude "muskatla".
- uslovi smeju biti samo iz liste dozvoljenih uslova.
- lokacija je grad/mesto ako se pominje, inače null.
- Ne piši nikakav tekst pre ili posle JSON-a.
-Vrati biljku SAMO ako pripada ovoj listi: {DOZVOLJENE_BILJKE}
-Ako biljka nije iz liste vrati null.

Primeri:
Upit: Koliko košta lavanda?
Izlaz:
{"namere":["cena"],"biljka":"lavanda","uslovi":[],"lokacija":null}

Upit: Imate li muškatle?
Izlaz:
{"namere":["dostupnost"],"biljka":"muskatla","uslovi":[],"lokacija":null}

Upit: Imate li lavandu i koliko košta?
Izlaz:
{"namere":["dostupnost","cena"],"biljka":"lavanda","uslovi":[],"lokacija":null}

Upit: Treba mi nešto za terasu na suncu
Izlaz:
{"namere":["preporuka"],"biljka":null,"uslovi":["terasa","sunce"],"lokacija":null}

Upit: Da li dostavljate za Vranje?
Izlaz:
{"namere":["dostava"],"biljka":null,"uslovi":[],"lokacija":"Vranje"}

Upit: Kada radite?
Izlaz:
{"namere":["radno_vreme"],"biljka":null,"uslovi":[],"lokacija":null}

Upit: Koji vam je broj telefona?
Izlaz:
{"namere":["kontakt"],"biljka":null,"uslovi":[],"lokacija":null}
"""

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
            "type": ["string", "null"]
        },
        "uslovi": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "lokacija": {
            "type": ["string", "null"]
        }
    },
    "required": ["namere", "biljka", "uslovi", "lokacija"]
}

MAPIRANJE_USLOVA = {
    "suncu": "sunce",
    "sunčano": "sunce",
    "sunčana": "sunce",
    "sunčan": "sunce",
    "osunčano": "sunce",
    "osuncano": "sunce",
    "jako sunce": "sunce",
    "puno sunca": "sunce",
    "direktno sunce": "sunce",

    "toplota": "sunce",
    "nemam hladovinu": "sunce",
    "nema hlad": "sunce",
    "nema hladovina": "sunce",

    "hlad": "senka",
    "hladu": "senka",
    "senku": "senka",
    "senci": "senka",
    "hladovina": "senka",
    "bez sunca": "senka",
    "nema mnogo sunca": "senka",
    "nema direktno sunce": "senka",
    "severna strana": "senka",

     "nema sunce": "senka",
    "nemam sunce": "senka",
    "nije sunce": "senka",
    "nije suncano": "senka",
    "bez sunca": "senka",
    "nema bas sunca": "senka",
    "ima malo sunca": "senka",
    "slabo sunce": "senka",
    "nije za sunce": "senka",
    "ne podnosi sunce": "senka",
    "nece na sunce": "senka",

    "polusenci": "polusenka",
    "polusenku": "polusenka",

    "malo zalivanja": "malo vode",
    "malo vode": "malo vode",
    "ne traži puno vode": "malo vode",
    "ne traži mnogo vode": "malo vode",
    "bez puno vode": "malo vode",
    "bez mnogo vode": "malo vode",
    "suša": "malo vode",
    "susa": "malo vode",
    "podnosi sušu": "malo vode",
    "podnosi susu": "malo vode",
    "retko zalivanje": "malo vode",

    "terasi": "terasa",
    "balkonu": "balkon",
    "žardinjere": "saksija",
    "zardinjere": "saksija",
    "viseće saksije": "saksija",
    "visece saksije": "saksija",
    "velika saksija": "saksija",

    "živa ograda": "živa ograda",
    "ziva ograda": "živa ograda",
    "ograda": "živa ograda",
    "živica": "živa ograda",
    "zivica": "živa ograda",
    "živu ogradu": "živa ograda",
    "zivu ogradu": "živa ograda",

    "zimzelene": "zimzelena",
    "zeleno tokom cele godine": "zimzelena",
    "zelena zimi": "zimzelena",

    "dvorištu": "dvorište",
    "dvoriste": "dvorište",
    "ispred kuće": "dvorište",
    "ispred kuce": "dvorište",

    "dekoracija": "ukrasna",
    "ukrasno": "ukrasna",
    "ulaz": "ukrasna",

    "mirisne": "mirisna",
    "lepo mirišu": "mirisna",
    "lepo mirisu": "mirisna",
    "aromatična": "zacinska",
    "aromaticna": "zacinska",
    "začinska": "zacinska",

    "lako održavanje": "laka nega",
    "lako odrzavanje": "laka nega",
    "početnik": "laka nega",
    "pocetnik": "laka nega",
    "početnici": "laka nega",
    "pocetnici": "laka nega",
    "ne zahteva puno pažnje": "laka nega",
    "ne zahteva puno paznje": "laka nega",

    "brzo raste": "brz rast",
    "rastu brzo": "brz rast",

    "cveta celo leto": "dugo cvetanje",
    "cvetaju celo leto": "dugo cvetanje",
    "cvetaju najduže": "dugo cvetanje",
    "cvetaju najduze": "dugo cvetanje",
    "dugo cveta": "dugo cvetanje",

    "mnogo cvetova": "cvetanje",
    "pčele": "medonosna",
    "pcele": "medonosna",
    "privlači pčele": "medonosna",
    "privlaci pcele": "medonosna",

    "mala basta": "mala bašta",
    "mala bašta": "mala bašta",
    "maju": "maj",
    "tokom leta": "leto",
    "letnje vrućine": "sunce",
    "letnje vrucine": "sunce",
    "vetar": "otporna",
    "otporne": "otporna"
}

#ne koristi se jos
MAPA_LOKACIJA = {
    "vranje": "Vranje",
    "vr": "Vranje",
    "vranju": "Vranje",
    "bujanovac": "Bujanovac",
    "bu": "Bujanovac",
    "surdulica": "Surdulica",
    "surdulicu": "Surdulica",
    "presevo": "Preševo",
    "preseva": "Preševo",
    "preševo": "Preševo",
    "preševa": "Preševo",
    "vladicin han": "Vladičin Han",
    "han": "Vladičin Han",
    "vl han": "Vladičin Han",
    "vl. han": "Vladičin Han",
    "vladičin han": "Vladičin Han"
}


def normalizuj_biljku(biljka):
    if biljka is None:
        return None

    biljka = biljka.lower().strip()

    

    mapa = {
    # LAVANDA
    "lavanda": "lavanda",
    "lavande": "lavanda",
    "lavandu": "lavanda",
    "lavandi": "lavanda",
    "lavandom": "lavanda",
    "lavandica": "lavanda",
    "lavandicu": "lavanda",

    # MUSKATLA
    "muskatla": "muskatla",
    "muskatle": "muskatla",
    "muskatlu": "muskatla",
    "muskatli": "muskatla",
    "muškatla": "muskatla",
    "muškatle": "muskatla",
    "muškatlu": "muskatla",
    "muškatli": "muskatla",
    "muštakla": "muskatla",
    "kaliopa": "muskatla",
    "slesce": "muskatla",
    "slešče": "muskatla",

    # PETUNIJA
    "petunija": "petunija",
    "petunije": "petunija",
    "petuniju": "petunija",
    "petuniji": "petunija",
    "petunijice": "petunija",

    # BEGONIJA
    "begonija": "begonija",
    "begonije": "begonija",
    "begoniju": "begonija",
    "begoniji": "begonija",

    # TUJA SMARAGD
    "tuja": "tuja smaragd",
    "tuje": "tuja smaragd",
    "tuju": "tuja smaragd",
    "tuji": "tuja smaragd",
    "tuja smaragd": "tuja smaragd",
    "tuje smaragd": "tuja smaragd",
    "tuju smaragd": "tuja smaragd",
    "smaragd": "tuja smaragd",

    # SURFINIJA
    "surfinija": "surfinija",
    "surfinije": "surfinija",
    "surfiniju": "surfinija",
    "surfiniji": "surfinija",

    # KADIFICA
    "kadifica": "kadifica",
    "kadifice": "kadifica",
    "kadificu": "kadifica",
    "kadifici": "kadifica",

    # VERBENA
    "verbena": "verbena",
    "verbene": "verbena",
    "verbenu": "verbena",
    "verbeni": "verbena",

    # VINKA
    "vinka": "vinka",
    "vinke": "vinka",
    "vinku": "vinka",
    "vinki": "vinka",

    # LOBELIJA
    "lobelija": "lobelija",
    "lobelije": "lobelija",
    "lobeliju": "lobelija",
    "lobeliji": "lobelija",

    # GAZANIJA
    "gazanija": "gazanija",
    "gazanije": "gazanija",
    "gazaniju": "gazanija",
    "gazaniji": "gazanija",

    # SALVIJA
    "salvija": "salvija",
    "salvije": "salvija",
    "salviju": "salvija",
    "salviji": "salvija",

    # DALIJA
    "dalija": "dalija",
    "dalije": "dalija",
    "daliju": "dalija",
    "daliji": "dalija",

    # HRIZANTEMA
    "hrizantema": "hrizantema",
    "hrizanteme": "hrizantema",
    "hrizantemu": "hrizantema",
    "hrizantemi": "hrizantema",

    # MACUHICA
    "maćuhica": "maćuhica",
    "maćuhice": "maćuhica",
    "maćuhicu": "maćuhica",
    "maćuhici": "maćuhica",
    "macuhica": "maćuhica",
    "macuhice": "maćuhica",
    "macuhicu": "maćuhica",

    # RUZMARIN
    "ruzmarin": "ruzmarin",
    "ruzmarina": "ruzmarin",
    "ruzmarinu": "ruzmarin",
    "ruzmarinom": "ruzmarin",

    # NANA
    "nana": "nana",
    "nane": "nana",
    "nanu": "nana",
    "nani": "nana",
    "menta": "nana",

    # ZALFIJA
    "žalfija": "žalfija",
    "žalfije": "žalfija",
    "žalfiju": "žalfija",
    "žalfiji": "žalfija",
    "zalfija": "žalfija",
    "zalfije": "žalfija",
    "zalfiju": "žalfija",

    # TIMIJAN
    "timijan": "timijan",
    "timijana": "timijan",
    "timijanu": "timijan",
    "majčina dušica": "timijan",
    "majcina dusica": "timijan",

    # ORIGANO
    "origano": "origano",
    "origana": "origano",
    "origanu": "origano",

    # TUJA BRABANT
    "tuja brabant": "tuja brabant",
    "tuje brabant": "tuja brabant",
    "tuju brabant": "tuja brabant",
    "brabant": "tuja brabant",

    # KLEKA
    "kleka": "kleka",
    "kleke": "kleka",
    "kleku": "kleka",
    "kleki": "kleka",

    # TISA
    "tisa": "tisa",
    "tise": "tisa",
    "tisu": "tisa",
    "tisi": "tisa",

    # SIMSIR
    "šimšir": "šimšir",
    "šimšira": "šimšir",
    "šimširu": "šimšir",
    "šimšire": "šimšir",
    "simsir": "šimšir",
    "simšir": "šimšir",
    "simsira": "šimšir",
    "šemšir": "šimšir",
    "šemsir": "šimšir",

    # LEYLANDII
    "leylandii": "leylandii",
    "lejlandi": "leylandii",
    "lejlandii": "leylandii",
    "lejlandija": "leylandii",

    # FOTINIJA
    "fotinija": "fotinija",
    "fotinije": "fotinija",
    "fotiniju": "fotinija",
    "fotiniji": "fotinija",

    # LOVOR VISNJA
    "lovor višnja": "lovor višnja",
    "lovor visnja": "lovor višnja",
    "lovor višnje": "lovor višnja",
    "lovor visnje": "lovor višnja",
    "lovor višnju": "lovor višnja",
    "lovor visnju": "lovor višnja",
    "lovor": "lovor višnja",

    # HIBISKUS
    "hibiskus": "hibiskus",
    "hibiskusa": "hibiskus",
    "hibiskusu": "hibiskus",

    # RUZA
    "ruža": "ruža",
    "ruže": "ruža",
    "ružu": "ruža",
    "ruži": "ruža",
    "ruza": "ruža",
    "ruze": "ruža",
    "ruzu": "ruža",
    "ruzi": "ruža",
    "ružva": "ruža",

    # HORTENZIJA
    "hortenzija": "hortenzija",
    "hortenzije": "hortenzija",
    "hortenziju": "hortenzija",
    "hortenziji": "hortenzija",

    # JAPANSKA DUNJA
    "japanska dunja": "japanska dunja",
    "japanske dunje": "japanska dunja",
    "japansku dunju": "japanska dunja",
    "dunja": "japanska dunja",

    # JAVOR KUGLASTI
    "javor kuglasti": "javor kuglasti",
    "kuglasti javor": "javor kuglasti",
    "javor": "javor kuglasti",

    # BREZA
    "breza": "breza",
    "breze": "breza",
    "brezu": "breza",
    "brezi": "breza",

    # KATALPA
    "katalpa": "katalpa",
    "katalpe": "katalpa",
    "katalpu": "katalpa",
    "katalpi": "katalpa",

    # KUGLASTI BAGREM
    "kuglasti bagrem": "kuglasti bagrem",
    "bagrem kuglasti": "kuglasti bagrem",
    "bagrem": "kuglasti bagrem",

    # CRVENI JAVOR
    "crveni javor": "crveni javor",
    "crvenog javora": "crveni javor",
    "crvenom javoru": "crveni javor",

    # UKRASNA TRESNJA
    "ukrasna trešnja": "ukrasna trešnja",
    "ukrasna tresnja": "ukrasna trešnja",
    "ukrasne trešnje": "ukrasna trešnja",
    "ukrasne tresnje": "ukrasna trešnja",
    "ukrasnu trešnju": "ukrasna trešnja",
    "ukrasnu tresnju": "ukrasna trešnja",

    # OPŠTE REČI KOJE NISU KONKRETNE BILJKE
    "zelena": None,
    "mirisna": None,
    "zimzelena": None,
    "saksija": None,
    "saksije": None,
    "cvece": None,
    "cveće": None,
    "biljka": None,
    "biljke": None,
    "drvo": None,
    "žbun": None,
    "zbun": None,
    "zacinska": None,
    "začinska": None
}

    return mapa.get(biljka, biljka)


def dodaj_nameru(rezultat, namera):
    if "namere" not in rezultat or not isinstance(rezultat["namere"], list):
        rezultat["namere"] = []

    if namera not in rezultat["namere"]:
        rezultat["namere"].append(namera)

    if "opste" in rezultat["namere"] and len(rezultat["namere"]) > 1:
        rezultat["namere"].remove("opste")

    return rezultat

def normalizuj_rezultat(rezultat):
    if rezultat is None:
        return None

    novi_uslovi = []

    for uslov in rezultat.get("uslovi", []):
        uslov_mali = str(uslov).lower().strip()
        normalizovan = MAPIRANJE_USLOVA.get(uslov_mali, uslov_mali)

        if normalizovan in DOZVOLJENI_USLOVI and normalizovan not in novi_uslovi:
            novi_uslovi.append(normalizovan)

    rezultat["uslovi"] = novi_uslovi
    rezultat["biljka"] = normalizuj_biljku(rezultat.get("biljka"))

    if rezultat.get("lokacija"):
        rezultat["lokacija"] = rezultat["lokacija"].strip().title()

    return rezultat



# def korekcija_namere(upit, rezultat):
#     tekst = upit.lower()

#     if any(rec in tekst for rec in [
#         "pošto", "koliko košta", "cena", "koliko para",
#         "koliko treba da platim", "koliko novca",
#         "košta li", "za koliko", "koliko naplaćujete"
#     ]):
#         rezultat["namera"] = "cena"

#     elif any(rec in tekst for rec in [
#         "dostavljate", "dostavite", "vozite",
#         "šaljete", "saljete", "isporuka", "dostava"
#     ]):
#         rezultat["namera"] = "dostava"

#     elif any(rec in tekst for rec in [
#         "gde se nalazite", "gde je rasadnik", "adresa",
#         "kako da dođem", "kako da dodjem", "u kom mestu"
#     ]):
#         rezultat["namera"] = "lokacija"

#     elif any(rec in tekst for rec in [
#         "imate li", "da li imate", "ima li", "dostupna",
#         "dostupne", "dostupan", "dostupno",
#         "na stanju", "prodajete li",
#         "mogu da kupim", "može li da se kupi", "moze li da se kupi"
#     ]):
#         rezultat["namera"] = "dostupnost"

#     elif rezultat.get("biljka") is not None and any(rec in tekst for rec in [
#         "koliko raste", "koliko naraste",
#         "koliko brzo raste", "kolika je visina",
#         "koliko često", "koliko cesto",
#         "koliko se zaliva", "kada cvetaju",
#         "može u saksiju", "moze u saksiju",
#         "voli sunce", "podnosi senku",
#         "može da prezimi", "moze da prezimi",
#         "traži mnogo održavanja", "trazi mnogo odrzavanja",
#         "može da se oblikuje", "moze da se oblikuje",
#         "dobra za pčele", "dobra za pcele",
#         "cveta celo leto",
#         "koliko vode traži", "koliko vode trazi"
#     ]):
#         rezultat["namera"] = "informacije"

#     elif any(rec in tekst for rec in [
#         "preporučujete", "preporucujete", "treba mi",
#         "koja biljka", "koje biljke", "šta da posadim",
#         "sta da posadim", "šta je najbolje", "sta je najbolje",
#         "želim", "zelim"
#     ]):
#         rezultat["namera"] = "preporuka"

#     return rezultat

def korekcija_namere(upit, rezultat):
    tekst = upit.lower()

    rezultat["namere"] = []

    if any(rec in tekst for rec in [
        "pošto", "koliko košta", "cena", "koliko para",
        "koliko treba da platim", "koliko novca",
        "košta li", "za koliko", "koliko naplaćujete"
    ]):
        dodaj_nameru(rezultat, "cena")

    if any(rec in tekst for rec in [
        "imate li", "da li imate", "ima li", "dostupna",
        "dostupne", "dostupan", "dostupno",
        "na stanju", "prodajete li",
        "mogu da kupim", "može li da se kupi", "moze li da se kupi"
    ]):
        dodaj_nameru(rezultat, "dostupnost")

    if any(rec in tekst for rec in [
        "dostavljate", "dostavite", "vozite",
        "šaljete", "saljete", "isporuka", "dostava",
        "vršite dostavu",
        "vrsite dostavu",
        "imate dostavu",
        "jel imate dostavu",
        "jel vršite dostavu",
        "jel vrsite dostavu",
        "da li dostavavljate",
        "dostava",
        "dostavu za"
    ]):
        dodaj_nameru(rezultat, "dostava")

    if any(rec in tekst for rec in [
        "gde se nalazite", "gde je rasadnik", "gde ste",
        "adresa", "kako da dođem", "kako da dodjem", "u kom mestu"
    ]):
        dodaj_nameru(rezultat, "lokacija")

    if any(rec in tekst for rec in [
        "radno vreme", "kad radite", "kada radite",
        "do koliko radite", "od koliko radite",
        "kad ste kući", "kad ste kuci"
    ]):
        dodaj_nameru(rezultat, "radno_vreme")

    if any(rec in tekst for rec in [
        "broj telefona", "telefon", "kontakt",
        "kako da vas pozovem", "kako mogu da vas pozovem",
        "koji vam je broj", "imate li broj"
    ]):
        dodaj_nameru(rezultat, "kontakt")

    if any(rec in tekst for rec in [
        "preporučujete", "preporucujete", "treba mi",
        "koja biljka", "koje biljke", "šta da posadim",
        "sta da posadim", "šta je najbolje", "sta je najbolje",
        "želim", "zelim"
    ]):
        dodaj_nameru(rezultat, "preporuka")

    if rezultat.get("biljka") is not None and any(rec in tekst for rec in [
        "koliko raste", "koliko naraste",
        "koliko brzo raste", "kolika je visina",
        "koliko često", "koliko cesto",
        "koliko se zaliva", "kada cvetaju",
        "može u saksiju", "moze u saksiju",
        "voli sunce", "podnosi senku",
        "može da prezimi", "moze da prezimi",
        "traži mnogo održavanja", "trazi mnogo odrzavanja",
        "može da se oblikuje", "moze da se oblikuje",
        "dobra za pčele", "dobra za pcele",
        "cveta celo leto",
        "koliko vode traži", "koliko vode trazi"
    ]):
        dodaj_nameru(rezultat, "informacije")

    if not rezultat["namere"]:
        rezultat["namere"] = ["opste"]

    # Kompatibilnost sa starim kodom
    rezultat["namera"] = rezultat["namere"][0]

    return rezultat

def ocisti_lokaciju(upit, rezultat):
    tekst = upit.lower()

    poznata_mesta = [
        "Vranje",
        "Bujanovac",
        "Preševo",
        "Presevo",
        "Surdulica",
        "Vladičin Han",
        "Vladicin Han",
        "Niš",
        "Nis",
        "Leskovac"
    ]

    if "dostava" in rezultat.get("namere", []):
        pronadjena_lokacija = None

        for mesto in poznata_mesta:
            if mesto.lower() in tekst:
                pronadjena_lokacija = mesto
                break

        rezultat["lokacija"] = pronadjena_lokacija

    return rezultat


def dopuni_uslove_iz_upita(upit, rezultat):
    tekst = upit.lower()

    for fraza, uslov in MAPIRANJE_USLOVA.items():
        if fraza in tekst and uslov in DOZVOLJENI_USLOVI:
            if uslov not in rezultat["uslovi"]:
                rezultat["uslovi"].append(uslov)

    return rezultat

def ocisti_uslove_po_upitu(upit, rezultat):
    tekst = upit.lower()
    uslovi = rezultat.get("uslovi", [])

    # Ako je pitanje o konkretnoj biljci, ne treba da izvlačimo uslove za evaluaciju.
    if rezultat.get("namera") == "informacije":
        rezultat["uslovi"] = []
        return rezultat

    # Ako je dostava/lokacija/cena/dostupnost/opste, uslovi uglavnom nisu potrebni.
    if rezultat.get("namera") in ["cena", "dostupnost", "lokacija", "dostava", "opste"]:
        rezultat["uslovi"] = []
        return rezultat

    # Uklanjanje čestih viškova koje model dodaje bez razloga.
    if "leto" in uslovi and "leto" not in tekst and "leta" not in tekst:
        uslovi.remove("leto")

    if "terasa" in uslovi and "terasa" not in tekst and "terasi" not in tekst:
        uslovi.remove("terasa")

    if "sunce" in uslovi and any(fraza in tekst for fraza in [
        "nema mnogo sunca",
        "nemam mnogo sunca",
        "nemam direktno sunce",
        "bez sunca",
        "u hladu",
        "hlad"
    ]):
        uslovi.remove("sunce")
        if "senka" not in uslovi:
            uslovi.append("senka")

    rezultat["uslovi"] = uslovi
    return rezultat


def parsiraj_upit(upit):
    response = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": upit}
        ],
        format=JSON_SCHEMA,
        options={
            "temperature": 0
        }
    )

    tekst = response["message"]["content"]

    try:
        rezultat = json.loads(tekst)

        rezultat = normalizuj_rezultat(rezultat)
        rezultat = korekcija_namere(upit, rezultat)
        rezultat = dopuni_uslove_iz_upita(upit, rezultat)
        rezultat = ocisti_uslove_po_upitu(upit, rezultat)
        rezultat = ocisti_lokaciju(upit, rezultat)

        return rezultat

    except json.JSONDecodeError:
        print("Model nije vratio validan JSON:")
        print(tekst)
        return None


if __name__ == "__main__":
    upit = "Treba mi biljka za balkon na suncu i da ne traži puno vode"
    rezultat = parsiraj_upit(upit)

    print(json.dumps(rezultat, ensure_ascii=False, indent=2))