from flask import Flask, render_template, request, redirect, url_for
from dpr import Attack, compute_dpr, chance_to_hit_at_least_once
from puzzles import prime_factors
from tools import (
    generate_ability_scores,
    random_barovia_encounter,
    random_name,
    random_tarokka_card,
)
import json
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

NOTES_FILE = os.path.join(os.path.dirname(__file__), 'notes.json')


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    chance = None
    if request.method == 'POST':
        attack_bonus = int(request.form.get('attack_bonus', 0) or 0)
        target_ac = int(request.form.get('target_ac', 0) or 0)
        damage_die = int(request.form.get('damage_die', 6) or 6)
        damage_bonus = int(request.form.get('damage_bonus', 0) or 0)
        num_attacks = int(request.form.get('num_attacks', 1) or 1)
        advantage = request.form.get('advantage') == 'on'
        disadvantage = request.form.get('disadvantage') == 'on'
        crit_range = int(request.form.get('crit_range', 20) or 20)

        attack = Attack(
            attack_bonus=attack_bonus,
            target_ac=target_ac,
            damage_die=damage_die,
            damage_bonus=damage_bonus,
            num_attacks=num_attacks,
            advantage=advantage,
            disadvantage=disadvantage,
            crit_range=crit_range,
        )
        result = compute_dpr(attack)
        chance = chance_to_hit_at_least_once(attack)
    return render_template('index.html', result=result, chance=chance)


@app.route('/ability-scores')
def ability_scores():
    scores = generate_ability_scores()
    return render_template('ability_scores.html', scores=scores)


@app.route('/tarokka')
def tarokka():
    card = random_tarokka_card()
    return render_template('tarokka.html', card=card)


@app.route('/encounter')
def encounter():
    encounter = random_barovia_encounter()
    return render_template('encounter.html', encounter=encounter)


@app.route('/npc-name')
def npc_name():
    name = random_name()
    return render_template('npc_name.html', name=name)

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    notes = load_notes()
    if request.method == 'POST':
        session_name = request.form.get('session', '').strip()
        content = request.form.get('content', '').strip()
        if content:
            notes.append({
                'time': datetime.utcnow().isoformat(),
                'session': session_name or 'General',
                'content': content,
            })
            save_notes(notes)
        return redirect(url_for('notes'))
    grouped = defaultdict(list)
    for note in notes:
        grouped[note.get('session', 'General')].append(note)
    return render_template('notes.html', grouped_notes=grouped)


@app.route('/puzzles', methods=['GET', 'POST'])
def puzzles():
    factors = None
    if request.method == 'POST':
        try:
            number = int(request.form.get('number', '0'))
            if number > 1:
                factors = prime_factors(number)
        except ValueError:
            factors = []
    return render_template('puzzles.html', factors=factors)
if __name__ == '__main__':
    app.run(debug=True)
