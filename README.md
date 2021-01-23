# diceRoller
Kivy UI for a dice rolling app

diceRoll.py contains a few functions for generating random numbers from specified ranges, and functions to interpret lists of the form ['1d8','2d6','3d4'] as instructions to roll one eigth-sided die, two six-sided dice, and three four-sided dice.

diceUIKivy.py uses those functions to allow users to roll a pool comprised of any number of 'standard' dice, along with a field for a custom die.
It also contains a tab allowing a user to check the distribution of values from any pool of dice.
You will need to install kivy and kivy_garden.graph
