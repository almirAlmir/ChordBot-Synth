import time

import numpy as np
from chordLogic import get_triade, apply_modulation
from synthConfig import (
    KEY_BASE_MIDI, 
    TEMPO_ACORDE_SEGUNDOS, 
    BPM, 
    ENVELOPE,
    FORMA_ONDA,
    NUM_VOZES,
    DETUNE_CENTS,
)
import sounddevice as sd
import keyboard

SAMPLE_RATE = 44100 # Frequência de amostragem padrão (44.1kHz)

def midi_to_freq(midi_note):
    # Fórmula para converter nota MIDI (e.g., 60) para frequência (e.g., 261.63 Hz)
    return 440.0 * 2**((midi_note - 69) / 12)

def generate_chord_audio(midi_notes):
    
    # 1. Cria a base de tempo para o acorde
    duration = TEMPO_ACORDE_SEGUNDOS
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    
    chord_signal = np.zeros_like(t)

    # 2. Gera o sinal para cada nota no acorde
    for note in midi_notes:
        base_freq = midi_to_freq(note)
        
        # Simula as múltiplas vozes (uníssono/detuning)
        for i in range(NUM_VOZES):
            # Aplica o detune
            detuned_freq = base_freq * (2**((i - (NUM_VOZES - 1)/2) * DETUNE_CENTS / 1200))
            
            # Gera a forma de onda (aqui você implementaria o 'sawtooth')
            # Por simplicidade, usamos Senoidal (sine) no conceito:
            oscillator = np.sin(2 * np.pi * detuned_freq * t)
            
            chord_signal += oscillator

    # 3. Aplica o Envelope ADSR (simplificado: apenas Attack e Release no final)
    # A implementação real do ADSR é complexa e precisa modular o sinal com uma curva.
    
    # Normaliza o sinal para evitar distorção (clipping)
    chord_signal /= NUM_VOZES * len(midi_notes)
    
    return chord_signal

# --- Definição da Progressão ---
# Progressão clássica no (Nashville Number System): I - VI - IV - V
PROGRESSAO_GRAUS = [1, 6, 4, 5] 
TONALIDADE_MIDI = KEY_BASE_MIDI 
TONALIDADE_NOME = "C" 
indice_acorde = 0 # Adicionado aqui para ser global
running = True # Variável para controlar o loop principal
#Por enquanto uma simulaçao que imprime o que aconteceria na execução -
#para depois implementar a síntese de áudio real.

SAMPLE_RATE = 44100 

# --- VARIÁVEIS GLOBAIS DE ESTADO ---
# Precisam ser definidas no escopo global para serem acessadas/modificadas por on_key_event
PROGRESSAO_GRAUS = [1, 6, 4, 5] 
TONALIDADE_MIDI = 60 
TONALIDADE_NOME = "C" 
indice_acorde = 0 
running = True 
# ... (PROGRESSION_MAP e funções de síntese como midi_to_freq e generate_chord_audio)


# ===============================================
# --- FUNÇÕES DE CONTROLE DE TECLADO (Key Mapping) ---
# ===============================================

# Mapeamento de Teclas: Associa uma tecla a uma Progressão de Graus (Nashville)
PROGRESSION_MAP = {
    '1': [1, 6, 4, 5], 
    '2': [2, 5, 1], 
    '3': [1, 4],
    'q': [1], 
}


def set_new_progression(graus):
    """Define a nova progressão global e reinicia o loop."""
    global PROGRESSAO_GRAUS, indice_acorde
    
    PROGRESSAO_GRAUS = graus
    indice_acorde = 0 
    
    print(f"\n[KEYPRESS] Progressão carregada: {PROGRESSAO_GRAUS}")


def on_key_event(event):
    """Função chamada quando uma tecla é pressionada."""
    # Acessa as variáveis globais que a função principal usa
    global running
    
    if event.event_type == keyboard.KEY_DOWN:
        key = event.name.lower() 
        
        if key in PROGRESSION_MAP:
            graus = PROGRESSION_MAP[key]
            set_new_progression(graus)
        
        elif key == 'esc': 
            print("Encerrando ChordBot...")
            running = False 
            keyboard.unhook_all()
            
        # Adicione mais comandos, como 'K C' ou 'K G' aqui, se desejar.

def run_chord_loop_simulation():
    """
    Simula o loop principal do ChordBot, gerando acordes e logando os parametros
    de síntese (em vez de gerar áudio real por enquanto).
    """
    global indice_acorde, running 
    print("------------------------------------------")
    print(f"🎸 ChordBot - MODO KEY MAPPING")
    print(f"Tonalidade Base: {TONALIDADE_NOME} | BPM: {BPM}")
    print(f"Comandos: Tecla '1', '2', '3' para mudar progressão | 'ESC' para sair.")
    print("------------------------------------------")

    # Hook do teclado (captura todos os eventos de tecla)
    keyboard.hook(on_key_event)

    while running:
        if not PROGRESSAO_GRAUS:
            print("Nenhuma progressão definida. Pressione uma tecla (ex: '1').")
            time.sleep(1)
            continue

        # --- Lógica Harmônica ---
        grau = PROGRESSAO_GRAUS[indice_acorde]
        
        acorde_base = get_triade(grau, TONALIDADE_MIDI) 
        
        # --- Aplicação de Modulação (mantida) ---
        if grau == 4: 
            acorde_final = apply_modulation(acorde_base, "maj7")
            modulacao_usada = "maj7"
        elif grau == 5:
            acorde_final = apply_modulation(acorde_base, "sus4")
            modulacao_usada = "sus4"
        else:
            acorde_final = acorde_base
            modulacao_usada = "Nenhuma"
            
        # --- Output e Geração de Áudio ---
        # Exibe a progressão que está sendo tocada
        print(f"({TONALIDADE_NOME}) | Tocando Grau: {grau} ({modulacao_usada}) -> Notas: {acorde_final}")
        
        audio_data = generate_chord_audio(acorde_final)
        sd.play(audio_data, SAMPLE_RATE)
        sd.wait() # Espera o acorde tocar antes de ir para o próximo
        # --- Próximo Acorde / Próxima Iteração ---
        indice_acorde += 1
        
        # Se chegou ao fim da progressão, reinicia
        if indice_acorde >= len(PROGRESSAO_GRAUS):
            indice_acorde = 0 
            # Imprime para o usuário saber que a progressão está recomeçando
            print("--- Progressão concluída. Reiniciando... ---") 

    print("\n------------------------------------------")
    print("ChordBot Encerrado.")
    print("------------------------------------------")

if __name__ == "__main__":
    # a função só é chamada quando o arquivo é executado diretamente
    run_chord_loop_simulation()
    
    print("\n------------------------------------------")
    print("SIMULAÇÃO CONCLUÍDA. FIM DA PROGRESSÃO.")
    print("------------------------------------------")