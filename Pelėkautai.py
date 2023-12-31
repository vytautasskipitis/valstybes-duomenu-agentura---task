import csv


def tikrinti_asmens_kodus(matricos_gyventojai_su_agentu_xqtzsch):
    neteisingi_kodai = []
    asmens_kodai = {}

    # nuskaitom failą
    with open(matricos_gyventojai_su_agentu_xqtzsch, 'r', newline='') as csv_failas:
        skaitytuvas = csv.reader(csv_failas)

        # antraštės eilutė
        next(skaitytuvas, None)

        for eilute in skaitytuvas:
            asmens_kodas = eilute[0]  # Pirmas stulpelis pagal excel kur surašyti asmens kodai

            # Surenka neteisingus asmens kodus
            if not patikrinti_asmens_koda(asmens_kodas):
                neteisingi_kodai.append(asmens_kodas)

                if asmens_kodas in asmens_kodai:
                    asmens_kodai[asmens_kodas] += 1
                else:
                    asmens_kodai[asmens_kodas] = 1

        # Rasti dublikatus
        dublikatai = [kodas for kodas, kiekis in asmens_kodai.items() if kiekis > 1]

        if dublikatai:
            print("Rasti dublikatai:")
            for dublikatas in dublikatai:
                print(dublikatas)
        else:
            print("Dublikatų nėra.")


    if neteisingi_kodai:
        print("Rasti neteisingi asmens kodai:")
        for neteisingas_kodas in neteisingi_kodai:
            print(neteisingas_kodas)
    else:
        print("Visi asmens kodai yra teisingi.")





def patikrinti_asmens_koda(asmens_kodas):

    if len(asmens_kodas) != 11:
        return False

    if not asmens_kodas.isdigit():
        return False

    if not (
        # Patikrina metus, mėnesį, dieną
            00 <= int(asmens_kodas[1:3]) <= 99 and
            2 <= int(asmens_kodas[0:1]) <= 6 and
            1 <= int(asmens_kodas[3:5]) <= 12 and
            asmens_kodas[3:5] != "00" and
            1 <= int(asmens_kodas[5:7]) <= 31 and
            asmens_kodas[5:7] != "00"
    ):
        return False

    svoris = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    suma = sum(int(asmens_kodas[i]) * svoris[i] for i in range(10))
    liekana = suma % 11

    if liekana != 10:
        # Jei liekana nėra 10, tai kontrolinis skaičius turi būti liekana
        kontrolinis_skaicius = liekana
    else:
        # Jei liekana yra 10, skaičiuojame kitu būdu
        svoris = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
        suma = sum(int(asmens_kodas[i]) * svoris[i] for i in range(10))
        liekana = suma % 11
        kontrolinis_skaicius = liekana if liekana != 10 else 0

    # Tikriname, ar paskutinis skaitmuo sutampa su kontroliniu skaičiumi
    return int(asmens_kodas[10]) == kontrolinis_skaicius



if __name__ == "__main__":
    matricos_gyventojai_su_agentu_xqtzsch = 'matricos_gyventojai_su_agentu_xqtzsch.csv'
    tikrinti_asmens_kodus(matricos_gyventojai_su_agentu_xqtzsch)

# metai, mėnesis, diena, 11 skaitmenų, nėra simbolių, paskutinis skaičius teisingas, vienodu asmens kodų nėra.
