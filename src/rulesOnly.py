import json
import re
import pandas as pd


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


def normalizuj_tekst(tekst):
    tekst = tekst.lower().strip()

    zamene = {
        "š": "s",
        "đ": "dj",
        "č": "c",
        "ć": "c",
        "ž": "z"
    }

    for staro, novo in zamene.items():
        tekst = tekst.replace(staro, novo)

    tekst = re.sub(r"[^\w\s]", " ", tekst)
    tekst = re.sub(r"\s+", " ", tekst)

    return tekst.strip()


MAPA_BILJAKA = {
    "lavanda": "lavanda",
    "lavande": "lavanda",
    "lavandu": "lavanda",
    "lavandi": "lavanda",
    "lavandom": "lavanda",
    "lavandica": "lavanda",

    "muskatla": "muskatla",
    "muskatle": "muskatla",
    "muskatlu": "muskatla",
    "muskatli": "muskatla",
    "mustakla": "muskatla",

    "petunija": "petunija",
    "petunije": "petunija",
    "petuniju": "petunija",

    "begonija": "begonija",
    "begonije": "begonija",
    "begoniju": "begonija",

    "tuja": "tuja smaragd",
    "tuje": "tuja smaragd",
    "tuju": "tuja smaragd",
    "smaragd": "tuja smaragd",
    "tuja smaragd": "tuja smaragd",
    "smaragd tuja": "tuja smaragd",

    "tuja brabant": "tuja brabant",
    "brabant": "tuja brabant",
    "brabant tuja": "tuja brabant",

    "surfinija": "surfinija",
    "surfinije": "surfinija",
    "surfiniju": "surfinija",

    "kadifica": "kadifica",
    "kadifice": "kadifica",
    "kadificu": "kadifica",

    "verbena": "verbena",
    "verbene": "verbena",
    "verbenu": "verbena",

    "vinka": "vinka",
    "vinke": "vinka",
    "vinku": "vinka",

    "lobelija": "lobelija",
    "lobelije": "lobelija",
    "lobeliju": "lobelija",

    "gazanija": "gazanija",
    "gazanije": "gazanija",
    "gazaniju": "gazanija",

    "salvija": "salvija",
    "salvije": "salvija",
    "salviju": "salvija",

    "dalija": "dalija",
    "dalije": "dalija",
    "daliju": "dalija",

    "hrizantema": "hrizantema",
    "hrizanteme": "hrizantema",
    "hrizantemu": "hrizantema",

    "macuhica": "maćuhica",
    "macuhice": "maćuhica",
    "macuhicu": "maćuhica",

    "ruzmarin": "ruzmarin",
    "ruzmarina": "ruzmarin",
    "ruzmarinu": "ruzmarin",

    "nana": "nana",
    "nane": "nana",
    "nanu": "nana",
    "menta": "nana",

    "zalfija": "žalfija",
    "zalfije": "žalfija",
    "zalfiju": "žalfija",

    "timijan": "timijan",
    "timijana": "timijan",
    "timijanu": "timijan",
    "majcina dusica": "timijan",

    "origano": "origano",
    "origana": "origano",
    "origanu": "origano",

    "kleka": "kleka",
    "kleke": "kleka",
    "kleku": "kleka",

    "tisa": "tisa",
    "tise": "tisa",
    "tisu": "tisa",

    "simsir": "šimšir",
    "simsira": "šimšir",
    "simsiru": "šimšir",
    "semsir": "šimšir",

    "leylandii": "leylandii",
    "lejlandi": "leylandii",
    "lejlandii": "leylandii",

    "fotinija": "fotinija",
    "fotinije": "fotinija",
    "fotiniju": "fotinija",

    "lovor visnja": "lovor višnja",
    "lovor visnje": "lovor višnja",
    "lovor visnju": "lovor višnja",
    "lovor": "lovor višnja",

    "hibiskus": "hibiskus",
    "hibiskusa": "hibiskus",
    "hibiskusu": "hibiskus",

    "ruza": "ruža",
    "ruze": "ruža",
    "ruzu": "ruža",
    "ruzi": "ruža",

    "hortenzija": "hortenzija",
    "hortenzije": "hortenzija",
    "hortenziju": "hortenzija",

    "japanska dunja": "japanska dunja",
    "japanske dunje": "japanska dunja",
    "japansku dunju": "japanska dunja",
    "dunja": "japanska dunja",

    "javor kuglasti": "javor kuglasti",
    "kuglasti javor": "javor kuglasti",

    "breza": "breza",
    "breze": "breza",
    "brezu": "breza",

    "katalpa": "katalpa",
    "katalpe": "katalpa",
    "katalpu": "katalpa",

    "kuglasti bagrem": "kuglasti bagrem",
    "bagrem kuglasti": "kuglasti bagrem",
    "bagrem": "kuglasti bagrem",

    "crveni javor": "crveni javor",
    "crvenog javora": "crveni javor",

    "ukrasna tresnja": "ukrasna trešnja",
    "ukrasne tresnje": "ukrasna trešnja",
    "ukrasnu tresnju": "ukrasna trešnja"
}


MAPIRANJE_USLOVA = {
    "suncu": "sunce",
    "sunce": "sunce",
    "suncano": "sunce",
    "jako sunce": "sunce",
    "puno sunca": "sunce",
    "direktno sunce": "sunce",
    "osuncano": "sunce",
    "juzna strana": "sunce",

    "hlad": "senka",
    "hladu": "senka",
    "senka": "senka",
    "senku": "senka",
    "hladovina": "senka",
    "bez sunca": "senka",
    "nema sunca": "senka",
    "nema mnogo sunca": "senka",
    "nemam mnogo sunca": "senka",
    "nema direktno sunce": "senka",
    "severna strana": "senka",

    "polusenka": "polusenka",
    "polusenci": "polusenka",
    "malo sunca": "polusenka",

    "malo vode": "malo vode",
    "malo zalivanja": "malo vode",
    "retko zalivanje": "malo vode",
    "ne trazi puno vode": "malo vode",
    "ne trazi mnogo vode": "malo vode",
    "bez puno vode": "malo vode",
    "bez mnogo vode": "malo vode",
    "podnosi susu": "malo vode",
    "susa": "malo vode",

    "srednje vode": "srednje vode",
    "normalno zalivanje": "srednje vode",
    "redovno zalivanje": "srednje vode",

    "puno vode": "puno vode",
    "mnogo vode": "puno vode",
    "voli vodu": "puno vode",
    "obilno zalivanje": "puno vode",

    "terasa": "terasa",
    "terasi": "terasa",

    "balkon": "balkon",
    "balkonu": "balkon",

    "saksija": "saksija",
    "saksije": "saksija",
    "saksiju": "saksija",
    "zardinjera": "saksija",
    "zardinjere": "saksija",

    "ziva ograda": "živa ograda",
    "zivu ogradu": "živa ograda",
    "ograda": "živa ograda",
    "zivica": "živa ograda",
    "zakloni pogled": "živa ograda",

    "zimzelena": "zimzelena",
    "zimzelene": "zimzelena",
    "zelena zimi": "zimzelena",
    "zelena tokom cele godine": "zimzelena",

    "dvoriste": "dvorište",
    "dvoristu": "dvorište",
    "basta": "dvorište",
    "ispred kuce": "dvorište",

    "ukrasna": "ukrasna",
    "ukrasno": "ukrasna",
    "dekorativna": "ukrasna",
    "dekoracija": "ukrasna",

    "mirisna": "mirisna",
    "mirise": "mirisna",
    "lepo mirise": "mirisna",

    "laka nega": "laka nega",
    "lako odrzavanje": "laka nega",
    "za pocetnike": "laka nega",
    "ne zahteva puno paznje": "laka nega",

    "brz rast": "brz rast",
    "brzo raste": "brz rast",
    "brzorastuca": "brz rast",

    "dugo cvetanje": "dugo cvetanje",
    "cveta celo leto": "dugo cvetanje",
    "dugo cveta": "dugo cvetanje",

    "cvetanje": "cvetanje",
    "cvetna": "cvetanje",
    "mnogo cvetova": "cvetanje",

    "medonosna": "medonosna",
    "pcele": "medonosna",
    "privlaci pcele": "medonosna",

    "kamenjar": "kamenjar",

    "mala basta": "mala bašta",
    "malo dvoriste": "mala bašta",
    "mali prostor": "mala bašta",

    "maj": "maj",
    "maju": "maj",

    "leto": "leto",
    "leta": "leto",
    "tokom leta": "leto",
    "za leto": "leto",

    "otporna": "otporna",
    "otporne": "otporna",
    "izdrzljiva": "otporna",
    "vetar": "otporna",

    "zacinska": "zacinska",
    "za kuvanje": "zacinska",
    "lekovita": "zacinska",
    "aromaticna": "zacinska"
}


MAPA_LOKACIJA = {
    "vranje": "Vranje",
    "vranju": "Vranje",
    "bujanovac": "Bujanovac",
    "bujanovcu": "Bujanovac",
    "surdulica": "Surdulica",
    "surdulicu": "Surdulica",
    "presevo": "Preševo",
    "preseva": "Preševo",
    "nis": "Niš",
    "nisu": "Niš",
    "leskovac": "Leskovac",
    "leskovcu": "Leskovac",
    "vladicin han": "Vladičin Han",
    "han": "Vladičin Han"
}


FRAZE_NAMERE = {
    "cena": [
        "posto",
        "koliko kosta",
        "cena",
        "koliko para",
        "koliko treba da platim",
        "koliko novca",
        "kosta li",
        "za koliko",
        "koliko naplacujete"
    ],

    "dostupnost": [
        "imate li",
        "da li imate",
        "ima li",
        "dostupna",
        "dostupne",
        "dostupan",
        "dostupno",
        "na stanju",
        "prodajete li",
        "mogu da kupim",
        "moze li da se kupi"
    ],

    "dostava": [
        "dostavljate",
        "dostavite",
        "vozite",
        "saljete",
        "isporuka",
        "dostava",
        "dostavu",
        "vrsite dostavu",
        "imate dostavu"
    ],

    "lokacija": [
        "gde se nalazite",
        "gde je rasadnik",
        "gde ste",
        "adresa",
        "kako da dodjem",
        "u kom mestu"
    ],

    "radno_vreme": [
        "radno vreme",
        "kad radite",
        "kada radite",
        "do koliko radite",
        "od koliko radite",
        "kad ste kuci"
    ],

    "kontakt": [
        "broj telefona",
        "telefon",
        "kontakt",
        "kako da vas pozovem",
        "koji vam je broj",
        "imate li broj"
    ],

    "preporuka": [
        "preporucujete",
        "treba mi",
        "koja biljka",
        "koje biljke",
        "sta da posadim",
        "sta je najbolje",
        "zelim",
        "hoću",
        "hocu",
        "trazim"
    ],

    "informacije": [
        "koliko raste",
        "koliko naraste",
        "koliko brzo raste",
        "kolika je visina",
        "koliko cesto",
        "koliko se zaliva",
        "kada cveta",
        "kada cvetaju",
        "moze u saksiju",
        "voli sunce",
        "podnosi senku",
        "moze da prezimi",
        "trazi mnogo odrzavanja",
        "moze da se oblikuje",
        "dobra za pcele",
        "koliko vode trazi"
    ]
}


def dodaj_nameru(namere, namera):
    if namera not in namere:
        namere.append(namera)


def pronadji_biljku(tekst):
    tekst_norm = normalizuj_tekst(tekst)

    kandidati = sorted(MAPA_BILJAKA.keys(), key=len, reverse=True)

    for fraza in kandidati:
        fraza_norm = normalizuj_tekst(fraza)

        pattern = r"\b" + re.escape(fraza_norm) + r"\b"

        if re.search(pattern, tekst_norm):
            biljka = MAPA_BILJAKA[fraza]

            if biljka is None:
                return None

            if biljka in DOZVOLJENE_BILJKE:
                return biljka

            return None

    return None


def pronadji_uslove(tekst):
    tekst_norm = normalizuj_tekst(tekst)
    uslovi = []

    kandidati = sorted(MAPIRANJE_USLOVA.keys(), key=len, reverse=True)

    for fraza in kandidati:
        fraza_norm = normalizuj_tekst(fraza)

        if fraza_norm in tekst_norm:
            uslov = MAPIRANJE_USLOVA[fraza]

            if uslov in DOZVOLJENI_USLOVI and uslov not in uslovi:
                uslovi.append(uslov)

    if "sunce" in uslovi and "senka" in uslovi:
        negativne_fraze = [
            "bez sunca",
            "nema sunca",
            "nemam mnogo sunca",
            "nema mnogo sunca",
            "nema direktno sunce",
            "hlad"
        ]

        if any(fraza in tekst_norm for fraza in negativne_fraze):
            uslovi.remove("sunce")

    return uslovi


def pronadji_lokaciju(tekst):
    tekst_norm = normalizuj_tekst(tekst)

    kandidati = sorted(MAPA_LOKACIJA.keys(), key=len, reverse=True)

    for fraza in kandidati:
        fraza_norm = normalizuj_tekst(fraza)

        pattern = r"\b" + re.escape(fraza_norm) + r"\b"

        if re.search(pattern, tekst_norm):
            return MAPA_LOKACIJA[fraza]

    return None


def pronadji_namere(tekst, biljka):
    tekst_norm = normalizuj_tekst(tekst)
    namere = []

    for namera, fraze in FRAZE_NAMERE.items():
        for fraza in fraze:
            fraza_norm = normalizuj_tekst(fraza)

            if fraza_norm in tekst_norm:
                dodaj_nameru(namere, namera)
                break

    if biljka is not None:
        info_fraze = FRAZE_NAMERE["informacije"]

        for fraza in info_fraze:
            if normalizuj_tekst(fraza) in tekst_norm:
                dodaj_nameru(namere, "informacije")
                break

    if not namere:
        namere = ["opste"]

    if "opste" in namere and len(namere) > 1:
        namere.remove("opste")

    return namere


def ocisti_uslove_po_nameri(uslovi, namere):
    if "preporuka" in namere:
        return uslovi

    if "informacije" in namere:
        return []

    if any(n in namere for n in ["cena", "dostupnost", "lokacija", "dostava", "radno_vreme", "kontakt", "opste"]):
        return []

    return uslovi


def parsiraj_upit(upit):
    biljka = pronadji_biljku(upit)
    uslovi = pronadji_uslove(upit)
    lokacija = pronadji_lokaciju(upit)
    namere = pronadji_namere(upit, biljka)

    uslovi = ocisti_uslove_po_nameri(uslovi, namere)

    rezultat = {
        "namere": namere,
        "biljka": biljka,
        "uslovi": uslovi,
        "lokacija": lokacija
    }

    rezultat["namera"] = rezultat["namere"][0]

    return rezultat


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