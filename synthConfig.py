# synth_config.py

#--- Parametros globais de audio ---
BPM = 120
TEMPO_ACORDE_SEGUNDOS = 60 / BPM * 4 # Um compasso (4 tempos) a 120 BPM = 2.0s
KEY_BASE_MIDI = 60 # C4 (MIDI 60)

# --- Timbre digital - sintese subtrativa ---

# Envelope ADSR
# Evolução do volume ao longo do tempo
ENVELOPE = {
    "attack": 0.05, # Rápido - o som atinge o volume máximo rapidamente
    "decay": 0.3,   # Médio - o som diminui um pouco após o attack
    "sustain": 0.7, # Sustenta o volume enquanto a nota é tocada
    "release": 0.8  # Longo - o som decai suavemente ao soltar a nota
}

# Forma de onda da fonte sonora
FORMA_ONDA = "sawtooth" # Pode ser usado -> "square" e "sine" como alternativas

# Multiplos osciladores para encorpar o som (uníssono/detuning)
NUM_VOZES = 3 # numero de osciladores que tocam a mesma nota
DETUNE_CENTS = 5 # leve desvio (em centésimos de semitom) entre as vozes

# --- Cadeia de Efeitos ---

# VCF - Aplicando no fim do Envelope
FILTRO = {
    "cutoff_freq": 8000, # frequência de corte (8kHz, deixando o som claro)
    "type": "lowpass"    # deixa passar apenas frequências baixas (cortando agudos)
}

# Reverb
REVERB = {
    "mix": 0.3,          # 30% de som com efeito
    "decay_time": 2.5    # Tempo de decaimento
}

# Delay (Adicionando repetição rítmica)
DELAY = {
    "mix": 0.2,          #20% de som com efeito
    "feedback": 0.4,     #Intensidade da repetição
    "time": 0.5          #Tempo de repetição
}