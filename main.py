import time
from chordLogic import get_triade, apply_modulation
from synthConfig import (
    KEY_BASE_MIDI, 
    TEMPO_ACORDE_SEGUNDOS, 
    BPM, 
    ENVELOPE,
    FORMA_ONDA
)

# --- Definição da Progressão ---
# Progressão clássica no (Nashville Number System): I - VI - IV - V
PROGRESSAO_GRAUS = [1, 6, 4, 5] 

#Por enquanto uma simulaçao que imprime o que aconteceria na execução -
#para depois implementar a síntese de áudio real.
def run_chord_loop_simulation():
    """
    Simula o loop principal do ChordBot, gerando acordes e logando os parametros
    de síntese (em vez de gerar áudio real por enquanto).
    """
    print("------------------------------------------")
    print(f"🎸 ChordBot - SIMULAÇÃO DE LOOP DE ACORDES")
    print(f"Key/Nota Base (C4): {KEY_BASE_MIDI} | BPM: {BPM}")
    print(f"Tempo por Acorde: {TEMPO_ACORDE_SEGUNDOS:.2f} segundos")
    print("------------------------------------------")

    
    indice_acorde = 0 # variável para rastrear a ordem dos acordes

    while indice_acorde < len(PROGRESSAO_GRAUS):
        grau = PROGRESSAO_GRAUS[indice_acorde]
        
        # --- Lógica Harmônica ---
        
        acorde_base = get_triade(grau, KEY_BASE_MIDI) # A oitava base é 4 por padrao no get_triade
        
        # --- Simulação de Modulação ---
        
        if grau == 4: 
            acorde_final = apply_modulation(acorde_base, "maj7") # Exemplo: aplicar Sétima Maior (maj7) no acorde IV
            modulacao_usada = "maj7 (Sétima Maior)"
        elif grau == 5:
            
            acorde_final = apply_modulation(acorde_base, "sus4") # Exemplo: suspender a terça do V
            modulacao_usada = "sus4 (Quarta Suspensa)"
        else:
            acorde_final = acorde_base
            modulacao_usada = "Nenhuma"
            
        # --- Output da Síntese ---
        print(f"\nGrau {indice_acorde + 1}: Acorde {grau}")
        print(f"  -> Notas MIDI: {acorde_final}")
        print(f"  -> Modulação: {modulacao_usada}")
        print(f"  -> Timbre: {FORMA_ONDA} com ENVELOPE: A:{ENVELOPE['attack']}, R:{ENVELOPE['release']}")
        
        # Simulação de espera do tempo
        print("  -> Toca por...") # time.sleep(TEMPO_ACORDE_SEGUNDOS) quando for realmente implementado
        
        indice_acorde += 1

if __name__ == "__main__":
    # a função só é chamada quando o arquivo é executado diretamente
    run_chord_loop_simulation()
    
    print("\n------------------------------------------")
    print("SIMULAÇÃO CONCLUÍDA. FIM DA PROGRESSÃO.")
    print("------------------------------------------")