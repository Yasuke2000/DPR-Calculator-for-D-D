from flask import Flask, render_template, request, redirect, url_for
from dpr import Attack, compute_dpr, chance_to_hit_at_least_once
from puzzles import prime_factors
import json
import os
from datetime import datetime

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


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    notes = load_notes()
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if content:
            notes.append({'time': datetime.utcnow().isoformat(), 'content': content})
            save_notes(notes)
        return redirect(url_for('notes'))
    return render_template('notes.html', notes=notes)


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
