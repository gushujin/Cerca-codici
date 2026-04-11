def configuratore_siemens():
    print("--- GENERATORE CODICI SIEMENS SENTRON ---")
    print("1. Magnetotermici (5SY)")
    print("2. Differenziali Puri (5SV)")
    print("3. AFDD - Antincendio (5SV6)")
    
    cat = input("\nScegli la categoria (1-3): ")

    if cat == "1":
        # Logica estratta dalle tue immagini (5SY)
        potere = input("Potere interruzione: [4] 10kA | [7] 15kA: ")
        poli = input("Poli: [1] 1P | [2] 2P | [5] 1P+N | [4] 4P | [6] 3P+N: ")
        ampere = input("Amperaggio (es. 06, 10, 16, 20, 25, 32): ")
        curva = input("Curva: [6] B | [7] C | [8] D: ")
        codice = f"5SY{potere}{poli}{ampere}-{curva}"
        desc = f"Magnetotermico 5SY, {poli} Poli, {ampere}A, Curva {'B' if curva=='6' else 'C' if curva=='7' else 'D'}"

    elif cat == "2":
        # Logica estratta dal catalogo (5SV)
        esec = input("Esecuzione: [3] Top | [4] Standard | [5] Residenziale: ")
        sens = input("Sensibilità: [1] 10mA | [3] 30mA | [6] 300mA: ")
        poli = input("Poli: [1] 1P+N | [4] 3P+N: ")
        amp = input("Corrente: [2] 25A | [4] 40A | [6] 63A: ")
        tipo = input("Tipo: [0] AC | [6] A | [3] F | [4] B: ")
        codice = f"5SV{esec}{sens}{poli}{amp}-{tipo}"
        desc = f"Differenziale 5SV, Sensibilità {sens}0mA, Poli {poli}, {amp}0A"

    elif cat == "3":
        # Logica AFDD (5SV6)
        amp = input("Amperaggio (10, 13, 16, 20, 25, 32, 40): ")
        curva = input("Curva: [B] | [C]: ").upper()
        codice = f"5SV6016-{curva}{amp}"
        desc = f"Protezione AFDD compatta (1 modulo), 1P+N, 6kA, {amp}A"

    else:
        print("Scelta non valida.")
        return

    print("\n" + "="*40)
    print(f"RISULTATO TECNICO:")
    print(f"CODICE SIEMENS: {codice}")
    print(f"CONFIGURAZIONE: {desc}")
    print("="*40)

if __name__ == "__main__":
    configuratore_siemens()
