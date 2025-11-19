from flask import Flask, request, jsonify
from chordLogic import get_triade, apply_modulation
from synthConfig import KEY_BASE_MIDI, ENVELOPE, FORMA_ONDA, REVERB, DELAY

app = Flask(__name__)

@app.route('api/chord/<int:grau>', methods=['GET'])
def get_chord_notes(grau):
    
    tipo_modulacao = request.args.get('mod') #pega o tipo da mudulaçao

    acorde_base = get_triade(grau, KEY_BASE_MIDI)
    acorde_final = acorde_base

    #A funcao de modulacao entra aqui
    if tipo_modulacao:
        acorde_final = apply_modulation(acorde_final, tipo_modulacao)

    return jsonify({
        'grau': grau,
        'modulacao': tipo_modulacao or 'None',
        'notas_midi': acorde_final,
        'status': 'success'})    