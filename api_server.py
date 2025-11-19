from flask import Flask, request, jsonify
from chordLogic import get_triade, apply_modulation
from synthConfig import KEY_BASE_MIDI, ENVELOPE, FORMA_ONDA, REVERB, DELAY