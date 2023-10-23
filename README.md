DPR Calculator Documentation
Overview
The DPR Calculator is a tool designed to calculate the average Damage Per Round (DPR) for characters in tabletop role-playing games, specifically Dungeons & Dragons. The calculator takes into account various character abilities, features, and conditions to provide an estimate of the average damage output.

Classes
DPRCalculator
This class is responsible for the core calculations related to DPR.

Methods:
basic_hit_probability(): Calculates the basic probability of hitting a target.
advantage_hit_probability(): Calculates the hit probability when the attacker has advantage.
disadvantage_hit_probability(): Calculates the hit probability when the attacker has disadvantage.
elven_accuracy_hit_probability(): Calculates the hit probability when the attacker has the Elven Accuracy feature.
halfling_luck(p): Adjusts the hit probability for the Halfling's Luck feature.
average_damage(): Calculates the average damage dealt with a single attack.
critical_hit_damage(): Calculates the damage dealt on a critical hit.
compute_dpr(...): Computes the average DPR based on various character features and conditions.
App
This class creates the graphical user interface (GUI) for the DPR Calculator using the tkinter library.

Methods:
safe_int_conversion(value, default=0): Safely converts a string to an integer. Returns the default value if the conversion fails.
calculate_dpr(): Retrieves input values from the GUI, performs the DPR calculation, and displays the result.
GUI Overview
The GUI provides input fields for:

Attack Bonus
Target AC (Armor Class)
Damage Dice
Damage Bonus
CHA (Charisma) Modifier
Number of Attacks
Sneak Attack Dice
Smite Variant Damage
Additionally, there are checkboxes for various character features and conditions, such as:

Advantage
Disadvantage
Elven Accuracy
Halfling
Rage
Divine Smite
Eldritch Blast with Agonizing Blast
Action Surge
Flurry of Blows
Hunter's Mark
Sharpshooter
Great Weapon Master
Reckless Attack
Hex
Polearm Master
Crossbow Expert
Dual Wielder
Savage Attacker
Bless
Haste
Versatile Weapon
After inputting the desired values and selecting the relevant features, the user can click the "Calculate DPR" button to get the average DPR result.

Usage
To use the DPR Calculator:

Run the provided code.
Input the relevant values into the GUI fields.
Select any applicable character features or conditions.
Click the "Calculate DPR" button.
The calculated average DPR will be displayed below the button.
