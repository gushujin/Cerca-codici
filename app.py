def genera_codice_siemens():
    print("--- CONFIGURATORE RAPIDO SIEMENS SENTRON ---")
    print("Seleziona la categoria:")
    print("1. Interruttori Magnetotermici (5SY)")
    print("2. Interruttori Differenziali Puri (5SV)")
    print("3. Protezione Antincendio AFDD (5SV6)")
    
    scelta = input("\nInserisci il numero della scelta: ")

    if scelta == "1":
        # Logica Magnetotermici 5SY
        potere = input("Potere di interruzione: [4] 10kA | [7] 15kA: ")
        poli = input("Poli: [1] 1P | [2] 2P | [5] 1P+N | [6] 3P+N: ")
        ampere = input("Corrente nominale (es. 06, 10, 16, 20, 25): ")
        curva = input("Curva di intervento: [B] | [C] | [D]: ").upper()
        
        codice = f"5SY{potere}{poli}{ampere}-{curva}"
        desc = f"Magnetotermico 5SY, {potere}0kA, {poli} Poli, {ampere}A, Curva {curva}"

    elif scelta == "2":
        # Logica Differenziali 5SV
        esecuzione = input("Esecuzione: [3] Top | [4] Standard | [5] Residenziale: ")
        sens = input("Sensibilità (IΔn): [1] 10mA | [3] 30mA | [6] 300mA: ")
        poli = input("Poli: [1] 1P+N | [4] 3P+N: ")
        ampere = input("Corrente (In): [1] 16A | [2] 25A | [4] 40A | [6] 63A: ")
        tipo = input("Tipo: [0] AC | [6] A | [3] F | [4] B: ")
        
        codice = f"5SV{esecuzione}{sens}{poli}{ampere}-{tipo}"
        desc = f"Differenziale Puro 5SV, Sens. {sens}0mA, Poli {poli}, {ampere}0A, Tipo {tipo}"

    elif scelta == "3":
        # Logica AFDD 5SV6
        ampere = input("Corrente nominale (es. 06, 10, 13, 16, 20, 25, 32, 40): ")
        curva = input("Curva magnetotermica: [B] | [C]: ").upper()
        
        codice = f"5SV6016-{curva}{ampere}"
        desc = f"AFDD (Protezione Antincendio) compatto, 1P+N, 6kA, {ampere}A, Curva {curva}"

    else:
        print("Scelta non valida.")
        return

    print("\n" + "="*30)
    print(f"CODICE IDENTIFICATO: {codice}")
    print(f"DESCRIZIONE: {desc}")
    print("="*30)

if __name__ == "__main__":
    genera_codice_siemens()
