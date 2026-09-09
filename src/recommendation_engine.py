import pandas as pd
from hibrid_five import parsiraj_upit


BILJKE_CSV = "biljke3.csv"


def ucitaj_biljke():
    df = pd.read_csv(BILJKE_CSV)
    df["naziv"] = df["naziv"].str.lower().str.strip()
    return df


def nadji_biljku(df, naziv_biljke):
    if naziv_biljke is None:
        return None

    naziv_biljke = naziv_biljke.lower().strip()

    rezultat = df[df["naziv"] == naziv_biljke]

    if rezultat.empty:
        return None

    return rezultat.iloc[0]


def odgovor_za_cenu(df, biljka):
    red = nadji_biljku(df, biljka)

    if red is None:
        return f"Nemam podatak o ceni za biljku: {biljka}."

    return f"{red['naziv'].capitalize()} košta {red['cena']} dinara."


def odgovor_za_dostupnost(df, biljka):
    red = nadji_biljku(df, biljka)

    if red is None:
        return f"Nemam podatak o dostupnosti za biljku: {biljka}."

    return (
        f"{red['naziv'].capitalize()} je dostupna od "
        f"{red['dostupnost_od']} do {red['dostupnost_do']}."
    )


def odgovor_za_informacije(df, biljka):
    red = nadji_biljku(df, biljka)

    if red is None:
        return f"Nemam detaljne informacije za biljku: {biljka}."

    return (
        f"{red['naziv'].capitalize()}:\n"
        f"- cena: {red['cena']} din\n"
        f"- visina: {red['visina']}\n"
        f"- sunce: {red['sunce']}\n"
        f"- voda: {red['voda']}\n"
        f"- tip: {red['tip']}\n"
        f"- nega: {red['nega']}\n"
        f"- opis: {red['opis']}"
    )


def filtriraj_po_uslovima(df, uslovi):
    rezultat = df.copy()

    for uslov in uslovi:
        uslov = uslov.lower().strip()

        if uslov == "sunce":
            rezultat = rezultat[rezultat["sunce"].str.contains("sunce", case=False, na=False)]

        elif uslov == "senka":
            rezultat = rezultat[rezultat["sunce"].str.contains("senka", case=False, na=False)]

        elif uslov == "polusenka":
            rezultat = rezultat[rezultat["sunce"].str.contains("polusenka", case=False, na=False)]

        elif uslov == "malo vode":
            rezultat = rezultat[rezultat["voda"].str.contains("malo", case=False, na=False)]

        elif uslov == "srednje vode":
            rezultat = rezultat[rezultat["voda"].str.contains("srednje", case=False, na=False)]

        elif uslov == "puno vode":
            rezultat = rezultat[rezultat["voda"].str.contains("puno", case=False, na=False)]

        elif uslov == "zimzelena":
            rezultat = rezultat[rezultat["tip"].str.contains("zimzelena", case=False, na=False)]

        elif uslov == "zacinska":
            rezultat = rezultat[rezultat["tip"].str.contains("zacinska", case=False, na=False)]

        elif uslov == "živa ograda":
            rezultat = rezultat[
                rezultat["opis"].str.contains("ograda|živa ograda|živicu|zaštita", case=False, na=False)
            ]

        elif uslov == "saksija":
            rezultat = rezultat[
                rezultat["opis"].str.contains("saksija|saksije|viseće|žardinjere|terase|balkone", case=False, na=False) |
                rezultat["tip"].str.contains("cvece|zacinska", case=False, na=False)
            ]

        elif uslov == "balkon":
            rezultat = rezultat[
                rezultat["opis"].str.contains("balkon|balkone|terase|saksije", case=False, na=False) |
                rezultat["tip"].str.contains("cvece", case=False, na=False)
            ]

        elif uslov == "terasa":
            rezultat = rezultat[
                rezultat["opis"].str.contains("terasa|terase|balkone|saksije", case=False, na=False) |
                rezultat["tip"].str.contains("cvece|zacinska", case=False, na=False)
            ]

        elif uslov == "dvorište":
            rezultat = rezultat[
                rezultat["tip"].str.contains("zimzelena|žbun|drvo|cvece|zacinska", case=False, na=False)
            ]

        elif uslov == "ukrasna":
            rezultat = rezultat[
                rezultat["opis"].str.contains("dekorativ|ukras|cvet|boja|krošnja", case=False, na=False)
            ]

        elif uslov == "mirisna":
            rezultat = rezultat[
                rezultat["opis"].str.contains("miris|aromati", case=False, na=False) |
                rezultat["tip"].str.contains("zacinska", case=False, na=False)
            ]

        elif uslov == "laka nega":
            rezultat = rezultat[
                rezultat["nega"].str.contains("minimalna|retko|vrlo malo|povremeno", case=False, na=False) |
                rezultat["opis"].str.contains("otporna|podnosi", case=False, na=False)
            ]

        elif uslov == "brz rast":
            rezultat = rezultat[
                rezultat["opis"].str.contains("brz rast|brzo", case=False, na=False) |
                rezultat["nega"].str.contains("brz rast", case=False, na=False)
            ]

        elif uslov == "dugo cvetanje":
            rezultat = rezultat[
                rezultat["opis"].str.contains("celo leto|dug period|tokom leta|bogato cveta", case=False, na=False)
            ]

        elif uslov == "cvetanje":
            rezultat = rezultat[
                rezultat["tip"].str.contains("cvece|žbun", case=False, na=False) |
                rezultat["opis"].str.contains("cvet|cvetanje", case=False, na=False)
            ]

        elif uslov == "medonosna":
            rezultat = rezultat[
                rezultat["opis"].str.contains("medonosna|pčele|pcele", case=False, na=False) |
                rezultat["tip"].str.contains("zacinska", case=False, na=False)
            ]

        elif uslov == "kamenjar":
            rezultat = rezultat[
                rezultat["voda"].str.contains("malo", case=False, na=False) &
                rezultat["sunce"].str.contains("sunce", case=False, na=False)
            ]

        elif uslov == "mala bašta":
            rezultat = rezultat[
                rezultat["visina"].str.contains("15-30|20-30|20-40|30-50|30-60|40-80|0.5-2|1-2", case=False, na=False)
            ]

        elif uslov == "maj":
            rezultat = rezultat[
                rezultat["dostupnost_od"].str.contains("mart|april|maj", case=False, na=False) &
                rezultat["dostupnost_do"].str.contains("maj|septembar|oktobar|novembar", case=False, na=False)
            ]

        elif uslov == "leto":
            rezultat = rezultat[
                rezultat["dostupnost_od"].str.contains("mart|april|maj", case=False, na=False) &
                rezultat["dostupnost_do"].str.contains("septembar|oktobar", case=False, na=False)
            ]

        elif uslov == "otporna":
            rezultat = rezultat[
                rezultat["opis"].str.contains("otporna|podnosi|dugovečna", case=False, na=False) |
                rezultat["nega"].str.contains("minimalna|retko|vrlo malo", case=False, na=False)
            ]

    return rezultat

def izracunaj_bodove(red, uslovi):
    bodovi = 0
    razlozi = []

    tekst_biljke = " ".join([
        str(red["sunce"]),
        str(red["voda"]),
        str(red["tip"]),
        str(red["nega"]),
        str(red["opis"])
    ]).lower()

    for uslov in uslovi:
        if uslov == "sunce" and "sunce" in str(red["sunce"]).lower():
            bodovi += 1
            razlozi.append("voli sunce")

        elif uslov == "senka" and "senka" in str(red["sunce"]).lower():
            bodovi += 1
            razlozi.append("podnosi senku")

        elif uslov == "malo vode" and "malo" in str(red["voda"]).lower():
            bodovi += 1
            razlozi.append("traži malo vode")

        elif uslov == "srednje vode" and "srednje" in str(red["voda"]).lower():
            bodovi += 1
            razlozi.append("traži srednje vode")

        elif uslov == "puno vode" and "puno" in str(red["voda"]).lower():
            bodovi += 1
            razlozi.append("traži puno vode")

        elif uslov == "zimzelena" and "zimzelena" in tekst_biljke:
            bodovi += 1
            razlozi.append("zimzelena je")

        elif uslov == "živa ograda" and ("ograda" in tekst_biljke or "zaštita" in tekst_biljke):
            bodovi += 1
            razlozi.append("pogodna je za živu ogradu")

        elif uslov == "saksija" and ("saksij" in tekst_biljke or "balkon" in tekst_biljke or "terase" in tekst_biljke):
            bodovi += 1
            razlozi.append("može u saksiju")

        elif uslov == "balkon" and ("balkon" in tekst_biljke or "terase" in tekst_biljke or "cvece" in tekst_biljke):
            bodovi += 1
            razlozi.append("dobra je za balkon")

        elif uslov == "terasa" and ("terasa" in tekst_biljke or "terase" in tekst_biljke or "cvece" in tekst_biljke):
            bodovi += 1
            razlozi.append("dobra je za terasu")

        elif uslov == "mirisna" and ("miris" in tekst_biljke or "aromati" in tekst_biljke or "zacinska" in tekst_biljke):
            bodovi += 1
            razlozi.append("mirisna/aromatična je")

        elif uslov == "laka nega" and ("minimalna" in tekst_biljke or "retko" in tekst_biljke or "otporna" in tekst_biljke):
            bodovi += 1
            razlozi.append("laka je za održavanje")

        elif uslov == "dugo cvetanje" and ("celo leto" in tekst_biljke or "dug period" in tekst_biljke or "bogato cveta" in tekst_biljke):
            bodovi += 1
            razlozi.append("dugo cveta")

    return bodovi, razlozi


def odgovor_za_preporuku(df, uslovi):
    if not uslovi:
        rezultat = df.head(5)
        tekst = "Niste naveli posebne uslove, pa izdvajam nekoliko popularnih biljaka:\n"
        for _, red in rezultat.iterrows():
            tekst += f"- {red['naziv'].capitalize()} ({red['cena']} din) — {red['opis']}\n"
        return tekst.strip()

    kandidati = []

    for _, red in df.iterrows():
        bodovi, razlozi = izracunaj_bodove(red, uslovi)

        if bodovi > 0:
            kandidati.append((bodovi, red, razlozi))

    if not kandidati:
        return "Nisam našao biljku koja odgovara navedenim uslovima. Probajte sa manje uslova."

    kandidati.sort(key=lambda x: x[0], reverse=True)
    kandidati = kandidati[:5]

    tekst = "Najbolje preporuke na osnovu uslova:\n"

    for i, (bodovi, red, razlozi) in enumerate(kandidati, start=1):
        tekst += (
            f"{i}. {red['naziv'].capitalize()} "
            f"({red['cena']} din) — poklapanje {bodovi}/{len(uslovi)}\n"
            f"   Razlog: {', '.join(razlozi)}.\n"
            f"   Opis: {red['opis']}\n"
        )

    return tekst.strip()
# def odgovor_za_preporuku(df, uslovi):
#     rezultat = filtriraj_po_uslovima(df, uslovi)

#     if rezultat.empty:
#         return "Nisam našao biljku koja tačno odgovara svim uslovima. Probajte sa manje uslova."

#     rezultat = rezultat.head(5)

#     tekst = "Preporučujem sledeće biljke:\n"

#     for _, red in rezultat.iterrows():
#         tekst += (
#             f"- {red['naziv'].capitalize()} "
#             f"({red['cena']} din) — {red['opis']}\n"
#         )

#     return tekst.strip()


def odgovor_za_lokaciju():
    return "Rasadnik se nalazi u Tibuždu, u blizini Vranja."


def odgovor_za_dostavu(lokacija):
    if lokacija is None:
        return "Radimo dostavu za okolna mesta. Napišite za koje mesto vas zanima dostava."

    return f"Za mesto {lokacija} možemo proveriti ili organizovati dostavu u dogovoru sa kupcem."

def odgovor_za_radno_vreme():
    return "Radno vreme rasadnika je svakog dana od 08:00 do 18:00. Za dolazak je najbolje da se prethodno najavite."


def odgovor_za_kontakt():
    return "Možete nas kontaktirati telefonom ili porukom na Instagram/Facebook stranici rasadnika."


# def generisi_odgovor(rezultat_parsera, df):
#     namera = rezultat_parsera.get("namera")
#     biljka = rezultat_parsera.get("biljka")
#     uslovi = rezultat_parsera.get("uslovi", [])
#     lokacija = rezultat_parsera.get("lokacija")

#     if namera == "cena":
#         return odgovor_za_cenu(df, biljka)

#     elif namera == "dostupnost":
#         return odgovor_za_dostupnost(df, biljka)

#     elif namera == "informacije":
#         return odgovor_za_informacije(df, biljka)

#     elif namera == "preporuka":
#         return odgovor_za_preporuku(df, uslovi)

#     elif namera == "lokacija":
#         return odgovor_za_lokaciju()

#     elif namera == "dostava":
#         return odgovor_za_dostavu(lokacija)

#     elif namera == "opste":
#         return "Mogu da odgovorim na pitanja o cenama, dostupnosti, nezi biljaka, preporukama i dostavi."

#     else:
#         return "Nisam siguran šta tačno pitate. Možete preformulisati pitanje."

def generisi_odgovor(rezultat_parsera, df):
    namere = rezultat_parsera.get("namere")

    if not namere:
        namere = [rezultat_parsera.get("namera", "opste")]

    biljka = rezultat_parsera.get("biljka")
    uslovi = rezultat_parsera.get("uslovi", [])
    lokacija = rezultat_parsera.get("lokacija")

    odgovori = []

    for namera in namere:
        if namera == "cena":
            odgovori.append(odgovor_za_cenu(df, biljka))

        elif namera == "dostupnost":
            odgovori.append(odgovor_za_dostupnost(df, biljka))

        elif namera == "informacije":
            odgovori.append(odgovor_za_informacije(df, biljka))

        elif namera == "preporuka":
            odgovori.append(odgovor_za_preporuku(df, uslovi))

        elif namera == "lokacija":
            odgovori.append(odgovor_za_lokaciju())

        elif namera == "dostava":
            odgovori.append(odgovor_za_dostavu(lokacija))

        elif namera == "radno_vreme":
            odgovori.append(odgovor_za_radno_vreme())

        elif namera == "kontakt":
            odgovori.append(odgovor_za_kontakt())

        elif namera == "opste":
            odgovori.append(
                "Mogu da odgovorim na pitanja o cenama, dostupnosti, nezi biljaka, preporukama, lokaciji, radnom vremenu, kontaktu i dostavi."
            )

    return "\n\n".join(odgovori)


if __name__ == "__main__":
    df = ucitaj_biljke()

    print("NLP asistent za rasadnik je pokrenut.")
    print("Za izlaz unesite: kraj")
    print("-" * 50)

    while True:
        upit = input("\nUnesite pitanje: ")

        if upit.lower().strip() in ["kraj", "exit", "quit"]:
            print("Kraj rada.")
            break

        rezultat = parsiraj_upit(upit)

        print("\nJSON parser:")
        print(rezultat)

        odgovor = generisi_odgovor(rezultat, df)

        print("\nOdgovor sistema:")
        print(odgovor)