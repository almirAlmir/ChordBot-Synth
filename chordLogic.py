# Nesse modulo eu quero transpor a representação de 1
# grau na escala em notas MIDI que harmonizem entre si

#------------------------------------------------------------------------

# escala maior a partir da tônica (Dó, Ré, Mi, Fá, Sol, Lá, Si por exemplo)
INTERVALOS_MAIOR = [0, 2, 4, 5, 7, 9, 11]

# pra cada grau da escala maior, define a qualidade do acorde
# 1-based: [I, ii, iii, IV, V, vi, vii°]
QUALIDADE_ACORDE = [
    (4, 7), # Maior: +4 (Terça M), +7 (Quinta P)
    (3, 7), # Menor: +3 (Terça m), +7 (Quinta P)
    (3, 7), # Menor: +3, +7
    (4, 7), # Maior: +4, +7
    (4, 7), # Maior: +4, +7
    (3, 7), # Menor: +3, +7
    (3, 6)  # Diminuto: +3, +6 (Quinta Dim)
]
#------------------------------------------------------------------------

def get_triade(grau: int, nota_midi: int, oitava_base: int = 4) -> list[int]:
    """
    Retorna a lista de notas MIDI para a tríade do grau que foi escolhido.

    :param grau: O grau do acorde (1 a 7).
    :param nota_midi: A nota MIDI da Tonalidade (ex: 60 para C4).
    :param oitava_base: Oitava em que o acorde deve ser tocado (4 = C4).
    :return: Uma lista de inteiros (notas MIDI).
    """
    if not 1 <= grau <= 7:
        raise ValueError("O grau do acorde deve estar entre 1 e 7.")

    # encontra o intervalo da tônica do acorde (a partir da "Key")
    indice_escala = grau - 1 
    intervalo_tônica = INTERVALOS_MAIOR[indice_escala]
    
    # add a oitava base
    tonica_midi = nota_midi + intervalo_tônica + (oitava_base * 12) #12 semitions por cada oitava
    
    # pega a Terça e a Quinta baseadas na qualidade (Maior/Menor/Diminuto)
    terca, quinta = QUALIDADE_ACORDE[indice_escala]
    
    # retorna a tríade completa
    return [
        tonica_midi,
        tonica_midi + terca,
        tonica_midi + quinta
    ]

def apply_modulation(acorde_midi: list[int], tipo_modulacao: str) -> list[int]:
    """
    Simula uma espcie de joystick adicionando extensões ou alterando notas.
    
    :param acorde_midi: A tríade inicial.
    :param tipo_modulacao: A extensão a ser adicionada (ex: 'maj7', 'add9').
    :return: O acorde extendido
    """
    
    # a tônica define a base dos intervalos
    tonica = acorde_midi[0]

    if tipo_modulacao == "maj7":
        # sétima Maior (intervalo +11 semitons)
        return acorde_midi + [tonica + 11]
    
    elif tipo_modulacao == "sus4":
        # Suspende a terça (substituindo-a pela quarta perfeita: +5)
        # O acorde sem a 3ª é [Tônica, Quinta]
        # Toda logica utilziada aqui é com base na tônica
        acorde_sus = [tonica, acorde_midi[2]] 
        return acorde_sus + [tonica + 5]
    
    # pode ser que  a gente adicione mais tipos de modulação futuramente nesse espaço
    return acorde_midi