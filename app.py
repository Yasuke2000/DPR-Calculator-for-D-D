from flask import Flask, render_template, request
from dpr import Attack, compute_dpr, chance_to_hit_at_least_once

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
