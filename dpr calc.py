import tkinter as tk
from tkinter import ttk


class DPRCalculator:

    def __init__(self, attack_bonus=0, target_ac=0, damage_dice=6, damage_bonus=0):
        self.attack_bonus = attack_bonus
        self.target_ac = target_ac
        self.damage_dice = damage_dice
        self.damage_bonus = damage_bonus

    def basic_hit_probability(self):
        return max(0.05, min(0.95, (21 + self.attack_bonus - self.target_ac) / 20))

    def advantage_hit_probability(self):
        p = self.basic_hit_probability()
        return p + (1 - p) * p

    def disadvantage_hit_probability(self):
        p = self.basic_hit_probability()
        return p * p

    def elven_accuracy_hit_probability(self):
        p = self.basic_hit_probability()
        return p + (1 - p) * p + (1 - p) * (1 - p) * p

    @staticmethod
    def halfling_luck(p):
        return p + (1 - p) * 0.05 * p

    def average_damage(self):
        return sum([(i + 1) for i in range(self.damage_dice)]) / self.damage_dice + self.damage_bonus

    def critical_hit_damage(self):
        return 2 * self.average_damage()

    def compute_dpr(self, advantage=False, disadvantage=False, elven_accuracy=False, halfling=False, rage=False,
                    divine_smite=False, eldritch_blast=False, cha_modifier=0, num_attacks=1, critical_chance=0.05,
                    action_surge=False, flurry_of_blows=False, sneak_attack_dice=0, hunters_mark=False,
                    sharpshooter=False, great_weapon_master=False, reckless_attack=False, hex_spell=False,
                    smite_variant=0, polearm_master=False,
                    crossbow_expert=False, dual_wielder=False, savage_attacker=False, bless=False,
                    haste=False, versatile_weapon=False):
        if advantage:
            hit_prob = self.advantage_hit_probability()
        elif disadvantage:
            hit_prob = self.disadvantage_hit_probability()
        elif elven_accuracy:
            hit_prob = self.elven_accuracy_hit_probability()
        else:
            hit_prob = self.basic_hit_probability()

        if halfling:
            hit_prob = self.halfling_luck(hit_prob)

        dpr = hit_prob * self.average_damage()

        if rage:
            dpr += 2  # Bonus for Barbarian's Rage

        if divine_smite:
            dpr += 2.5 * 2  # 2d8 radiant damage for Divine Smite using a 1st-level spell slot

        if eldritch_blast:
            dpr += cha_modifier  # Add CHA modifier to damage

        # Multiple Attacks
        dpr *= num_attacks

        # Critical Hits
        dpr += critical_chance * self.critical_hit_damage()

        # Fighter's Action Surge (double the number of attacks)
        if action_surge:
            dpr *= 2

        # Monk's Flurry of Blows (two additional unarmed strikes)
        if flurry_of_blows:
            dpr += 2 * (hit_prob * (1 + self.damage_bonus))

        # Rogue's Sneak Attack
        sneak_attack_avg_damage = 0
        if sneak_attack_dice > 0:
            sneak_attack_avg_damage = sum([(i + 1) for i in range(sneak_attack_dice)]) / sneak_attack_dice
        dpr += hit_prob * sneak_attack_avg_damage

        # Ranger's Hunter's Mark
        if hunters_mark:
            dpr += hit_prob * 3.5  # 1d6 average damage

        # Sharpshooter
        if sharpshooter:
            dpr += 10  # +10 damage on hit

        # Great Weapon Master
        if great_weapon_master:
            dpr += 10  # +10 damage on hit

        # Barbarian's Reckless Attack
        if reckless_attack:
            hit_prob = self.advantage_hit_probability()

        # Warlock's Hex
        if hex_spell:
            dpr += hit_prob * 3.5  # 1d6 average damage

        # Paladin's Smite Variants
        dpr += smite_variant  # Assuming smite_variant is the average damage of the smite variant used

        # Druid's Wild Shape and Bard's Blade Flourish can be complex and might need more specific implementations

        # Feats
        if polearm_master:
            dpr += hit_prob * self.average_damage()  # Additional attack with the opposite end

        if crossbow_expert:
            dpr += hit_prob * self.average_damage()  # Additional attack with a hand crossbow

        if dual_wielder:
            dpr += hit_prob * self.average_damage()  # Additional damage when fighting with two weapons

        if savage_attacker:
            # This is a bit tricky. For simplicity, we can assume it adds 10% more damage on average
            dpr *= 1.10

        # Other Mechanics
        if bless:
            hit_prob += 0.125  # Average of 1d4 added to hit

        if haste:
            dpr *= 2  # Double the number of attacks

        if versatile_weapon:
            dpr += 1  # Assuming an average increase of 1 damage for using two hands

        return dpr


class App:

    def __init__(self, master):
        self.calculator = DPRCalculator()

        # Labels and Entries for inputs
        ttk.Label(master, text="Attack Bonus:").grid(row=0, column=0, sticky=tk.W)
        self.attack_bonus = ttk.Entry(master)
        self.attack_bonus.grid(row=0, column=1)

        ttk.Label(master, text="Target AC:").grid(row=1, column=0, sticky=tk.W)
        self.target_ac = ttk.Entry(master)
        self.target_ac.grid(row=1, column=1)

        ttk.Label(master, text="Damage Dice (e.g., 6 for d6):").grid(row=2, column=0, sticky=tk.W)
        self.damage_dice = ttk.Entry(master)
        self.damage_dice.grid(row=2, column=1)

        ttk.Label(master, text="Damage Bonus:").grid(row=3, column=0, sticky=tk.W)
        self.damage_bonus = ttk.Entry(master)
        self.damage_bonus.grid(row=3, column=1)

        ttk.Label(master, text="CHA Modifier (for Eldritch Blast):").grid(row=4, column=0, sticky=tk.W)
        self.cha_modifier = ttk.Entry(master)
        self.cha_modifier.grid(row=4, column=1)

        # Check buttons for features
        self.advantage = tk.BooleanVar()
        ttk.Checkbutton(master, text="Advantage", variable=self.advantage).grid(row=5, column=0, sticky=tk.W)

        self.disadvantage = tk.BooleanVar()
        ttk.Checkbutton(master, text="Disadvantage", variable=self.disadvantage).grid(row=5, column=1, sticky=tk.W)

        self.elven_accuracy = tk.BooleanVar()
        ttk.Checkbutton(master, text="Elven Accuracy", variable=self.elven_accuracy).grid(row=6, column=0, sticky=tk.W)

        self.halfling = tk.BooleanVar()
        ttk.Checkbutton(master, text="Halfling", variable=self.halfling).grid(row=6, column=1, sticky=tk.W)

        self.rage = tk.BooleanVar()
        ttk.Checkbutton(master, text="Rage", variable=self.rage).grid(row=7, column=0, sticky=tk.W)

        self.divine_smite = tk.BooleanVar()
        ttk.Checkbutton(master, text="Divine Smite", variable=self.divine_smite).grid(row=7, column=1, sticky=tk.W)

        self.eldritch_blast = tk.BooleanVar()
        ttk.Checkbutton(master, text="Eldritch Blast with Agonizing Blast", variable=self.eldritch_blast).grid(
            row=8, column=0, sticky=tk.W)

        ttk.Label(master, text="Number of Attacks:").grid(row=11, column=0, sticky=tk.W)
        self.num_attacks = ttk.Entry(master)
        self.num_attacks.grid(row=11, column=1)

        self.action_surge = tk.BooleanVar()
        ttk.Checkbutton(master, text="Action Surge", variable=self.action_surge).grid(row=12, column=0, sticky=tk.W)

        self.flurry_of_blows = tk.BooleanVar()
        ttk.Checkbutton(master, text="Flurry of Blows", variable=self.flurry_of_blows).grid(row=12, column=1,
                                                                                            sticky=tk.W)

        ttk.Label(master, text="Sneak Attack Dice (e.g., 2 for 2d6):").grid(row=13, column=0, sticky=tk.W)
        self.sneak_attack_dice = ttk.Entry(master)
        self.sneak_attack_dice.grid(row=13, column=1)

        self.hunters_mark = tk.BooleanVar()
        ttk.Checkbutton(master, text="Hunter's Mark", variable=self.hunters_mark).grid(row=14, column=0, sticky=tk.W)

        self.sharpshooter = tk.BooleanVar()
        ttk.Checkbutton(master, text="Sharpshooter", variable=self.sharpshooter).grid(row=14, column=1, sticky=tk.W)

        self.great_weapon_master = tk.BooleanVar()
        ttk.Checkbutton(master, text="Great Weapon Master", variable=self.great_weapon_master).grid(row=15, column=0,
                                                                                                    sticky=tk.W)
        self.reckless_attack = tk.BooleanVar()
        ttk.Checkbutton(master, text="Reckless Attack", variable=self.reckless_attack).grid(row=16, column=0,
                                                                                            sticky=tk.W)

        self.hex_spell = tk.BooleanVar()
        ttk.Checkbutton(master, text="Hex", variable=self.hex_spell).grid(row=16, column=1, sticky=tk.W)

        ttk.Label(master, text="Smite Variant Damage:").grid(row=17, column=0, sticky=tk.W)
        self.smite_variant = ttk.Entry(master)
        self.smite_variant.grid(row=17, column=1)

        self.polearm_master = tk.BooleanVar()
        ttk.Checkbutton(master, text="Polearm Master", variable=self.polearm_master).grid(row=18, column=0, sticky=tk.W)

        self.crossbow_expert = tk.BooleanVar()
        ttk.Checkbutton(master, text="Crossbow Expert", variable=self.crossbow_expert).grid(row=18, column=1,
                                                                                            sticky=tk.W)

        self.dual_wielder = tk.BooleanVar()
        ttk.Checkbutton(master, text="Dual Wielder", variable=self.dual_wielder).grid(row=19, column=0, sticky=tk.W)

        self.savage_attacker = tk.BooleanVar()
        ttk.Checkbutton(master, text="Savage Attacker", variable=self.savage_attacker).grid(row=19, column=1,
                                                                                            sticky=tk.W)

        self.bless = tk.BooleanVar()
        ttk.Checkbutton(master, text="Bless", variable=self.bless).grid(row=20, column=0, sticky=tk.W)

        self.haste = tk.BooleanVar()
        ttk.Checkbutton(master, text="Haste", variable=self.haste).grid(row=20, column=1, sticky=tk.W)

        self.versatile_weapon = tk.BooleanVar()
        ttk.Checkbutton(master, text="Versatile Weapon", variable=self.versatile_weapon).grid(row=21, column=0,
                                                                                              sticky=tk.W)
        ttk.Button(master, text="Calculate DPR", command=self.calculate_dpr).grid(row=22, column=0, columnspan=2)
        self.result_label = ttk.Label(master, text="")
        self.result_label.grid(row=23, column=0, columnspan=2)

    @staticmethod
    def safe_int_conversion(value, default=0):
        try:
            return int(value)
        except ValueError:
            return default

    def calculate_dpr(self):
        self.calculator.attack_bonus = self.safe_int_conversion(self.attack_bonus.get())
        self.calculator.target_ac = self.safe_int_conversion(self.target_ac.get())
        self.calculator.damage_dice = self.safe_int_conversion(self.damage_dice.get())
        self.calculator.damage_bonus = self.safe_int_conversion(self.damage_bonus.get())

        num_attacks = self.safe_int_conversion(self.num_attacks.get())
        critical_chance = 0.05  # 5% chance for a natural 20
        action_surge = self.action_surge.get()
        flurry_of_blows = self.flurry_of_blows.get()
        sneak_attack_dice = self.safe_int_conversion(self.sneak_attack_dice.get())
        hunters_mark = self.hunters_mark.get()
        sharpshooter = self.sharpshooter.get()
        great_weapon_master = self.great_weapon_master.get()

        dpr = self.calculator.compute_dpr(self.advantage.get(), self.disadvantage.get(), self.elven_accuracy.get(),
                                          self.halfling.get(), self.rage.get(), self.divine_smite.get(),
                                          self.eldritch_blast.get(), self.safe_int_conversion(self.cha_modifier.get()),
                                          num_attacks,
                                          critical_chance, action_surge, flurry_of_blows, sneak_attack_dice,
                                          hunters_mark, sharpshooter, great_weapon_master)
        self.result_label.config(text=f"Calculated DPR: {dpr:.2f}")


if __name__ == "__main__":
    main_root = tk.Tk()
    main_root.title("DPR Calculator")
    app = App(main_root)
    main_root.mainloop()
