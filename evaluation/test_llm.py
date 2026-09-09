
import pandas as pd
#from rulesOnly import parsiraj_upit
#from llmOnly import parsiraj_upit

#from hibrid_zero import parsiraj_upit
#from hibrid_ten import parsiraj_upit
# from hibrid_one import parsiraj_upit
# from hibrid_five import parsiraj_upit
from hibrid_three import parsiraj_upit



def uporedi_vrednosti(ocekivano, dobijeno):
    if pd.isna(ocekivano):
        ocekivano = ""

    if dobijeno is None:
        dobijeno = ""

    return str(ocekivano).strip().lower() == str(dobijeno).strip().lower()


def napravi_set_uslova(vrednost):
    if pd.isna(vrednost):
        return set()

    tekst = str(vrednost).lower().strip()

    if tekst == "" or tekst == "nan":
        return set()

    return set([x.strip() for x in tekst.split(",") if x.strip() != ""])


def izvuci_namere(rezultat):
    namere = rezultat.get("namere", [])

    if not namere:
        stara_namera = rezultat.get("namera", "")
        if stara_namera:
            namere = [stara_namera]

    return [str(n).strip().lower() for n in namere]


df = pd.read_csv("pitanja.csv")

ukupno = 0
pogodjena_namera = 0
pogodjena_biljka = 0
pogodjeni_uslovi = 0
pogodjena_lokacija = 0
pogodjen_ceo_json = 0

greske = []

for index, red in df.iterrows():
#for index, red in df.head(30).iterrows():
    upit = red["upit"]
    rezultat = parsiraj_upit(upit)

    if rezultat is None:
        rezultat = {
            "namere": [],
            "namera": "",
            "biljka": "",
            "uslovi": [],
            "lokacija": ""
        }

    ukupno += 1

    ocekivana_namera = red["ocekivana_namera"]
    llm_namere_lista = izvuci_namere(rezultat)
    llm_namera = ",".join(llm_namere_lista)

    ocekivana_biljka = red["ocekivana_biljka"]
    llm_biljka = rezultat.get("biljka", "")

    ocekivani_uslovi_set = napravi_set_uslova(red["ocekivani_uslovi"])
    llm_uslovi_set = set([
        str(x).strip().lower()
        for x in rezultat.get("uslovi", [])
        if str(x).strip() != ""
    ])

    tacna_namera = str(ocekivana_namera).strip().lower() in llm_namere_lista
    tacna_biljka = uporedi_vrednosti(ocekivana_biljka, llm_biljka)
    tacni_uslovi = ocekivani_uslovi_set == llm_uslovi_set

    if "lokacija" in df.columns:
        tacna_lokacija = uporedi_vrednosti(
            red["lokacija"],
            rezultat.get("lokacija", "")
        )
    else:
        tacna_lokacija = True

    if tacna_namera:
        pogodjena_namera += 1

    if tacna_biljka:
        pogodjena_biljka += 1

    if tacni_uslovi:
        pogodjeni_uslovi += 1

    if tacna_lokacija:
        pogodjena_lokacija += 1

    if tacna_namera and tacna_biljka and tacni_uslovi and tacna_lokacija:
        pogodjen_ceo_json += 1

    if not (tacna_namera and tacna_biljka and tacni_uslovi and tacna_lokacija):
        greske.append({
            "upit": upit,
            "ocekivana_namera": ocekivana_namera,
            "llm_namera": llm_namera,
            "ocekivana_biljka": ocekivana_biljka,
            "llm_biljka": llm_biljka,
            "ocekivani_uslovi": ",".join(sorted(ocekivani_uslovi_set)),
            "llm_uslovi": ",".join(sorted(llm_uslovi_set)),
            "ocekivana_lokacija": red["lokacija"] if "lokacija" in df.columns else "",
            "llm_lokacija": rezultat.get("lokacija", "")
        })


print("\nREZULTATI ZA SVE UPITE")
print("-" * 40)
print(f"Ukupno upita: {ukupno}")

print(
    f"Tačnost namere: {pogodjena_namera}/{ukupno} = "
    f"{pogodjena_namera / ukupno * 100:.2f}%"
)

print(
    f"Tačnost biljke: {pogodjena_biljka}/{ukupno} = "
    f"{pogodjena_biljka / ukupno * 100:.2f}%"
)

print(
    f"Tačnost uslova: {pogodjeni_uslovi}/{ukupno} = "
    f"{pogodjeni_uslovi / ukupno * 100:.2f}%"
)

if "lokacija" in df.columns:
    print(
        f"Tačnost lokacije: {pogodjena_lokacija}/{ukupno} = "
        f"{pogodjena_lokacija / ukupno * 100:.2f}%"
    )

print(
    f"Ukupna tačnost JSON-a: {pogodjen_ceo_json}/{ukupno} = "
    f"{pogodjen_ceo_json / ukupno * 100:.2f}%"
)

greske_df = pd.DataFrame(greske)
# greske_df.to_csv("greskeRulesOnly.csv", index=False, encoding="utf-8-sig")

# print("\nGreške su sačuvane u fajl: greskeRulesOnly.csv")

# greske_df.to_csv("greskeLLMOnly.csv", index=False, encoding="utf-8-sig")

# print("\nGreške su sačuvane u fajl: greskeLLMOnly.csv")

# greske_df.to_csv("greskeHibridZero.csv", index=False, encoding="utf-8-sig")

# print("\nGreške su sačuvane u fajl: greskeHidbridZero.csv")

# greske_df.to_csv("greskeHibridTen.csv", index=False, encoding="utf-8-sig")

# print("\nGreške su sačuvane u fajl: greskeHibridTen.csv")

# greske_df.to_csv("greskeHibridOne.csv", index=False, encoding="utf-8-sig")

# print("\nGreške su sačuvane u fajl: greskeHibridOne.csv")


# greske_df.to_csv("greskeHibridFive.csv", index=False, encoding="utf-8-sig")

# print("\nGreške su sačuvane u fajl: greskeHibridFive.csv")

greske_df.to_csv("greskeHibridThree.csv", index=False, encoding="utf-8-sig")

print("\nGreške su sačuvane u fajl: greskeHibridThree.csv")

