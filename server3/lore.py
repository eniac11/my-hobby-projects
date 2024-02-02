"""Copyright (C) 2024 Hadley Epstein

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from .character import *


# Orders
technolas = create_order("Technolas", "Technology magic")
auraleis = create_order("Auralëis", "The manipulation of Aura")

# Magic
# Aura = magic(auraleis, "Aura", "Types of aura eamr and iamr, audralr")

visacality = create_magic('visacality', "Represents the nature of how an object looks.")
blue_aura = Reference(visacality, "known_as", visacality.known_as("Blue Aura"))

physicality = create_magic('physicality', "Represents the nature of physical nature of an object")
green_aura = Reference(physicality, "known_as", physicality.known_as("Green Aura"))

magic_Aura = create_magic('magic', [
    create_p(children=[
        'Represents magic, there are varying levels of sight with each level compounding on top of the previous:',
        create_element('ul', children=[
            create_list_item(children=[
                create_header("Level 1", level=3),
                "The mage is only aware that there is magic"
            ]),
            create_list_item(children=[
                create_header("Level 2", level=3),
                "The mage is able to discern power level of the magic"
            ]),
            create_list_item(children=[
                create_header("Level 3", level=3),
                "The mage is able to figure out what the magic can do"
            ]),
            create_list_item(children=[
                create_header("Level 4", level=3),
                "The mage can manipulate the Aura as long as it external, this allows them to change the nature ",
                "of the magic."
            ])
        ])
    ])
])
yellow_aura = Reference(magic_Aura, "known_as", magic_Aura.known_as("Yellow Aura"))

aura = MagicSystem("aura", [
    create_p(children=[
        "Aura can be manipulated by mages of ", auraleis
    ]),
    create_p(children=[
        "There are two types of Aura:",
        create_element("ul", children=[
            create_list_item(children=[
                create_header("eämr", level=3),
                "External Aura, Aura that permeates the World", create_breakline(),
                "Manipulation of eämr changes physical properties of physical things in the world. Like Physicality ",
                "changes the properties of ", physicality, " whereas ", visacality, " only affects the sight."
            ]),
            create_list_item(children=[
                create_header("iämr", level=3),
                "Internal Aura, Aura that that is internal to everything.", create_breakline(),
                "Manipulation of iämr involves the redistribution of iämr Aura within the mage this means that if they ",
                "wanted to be incredibly strong they would have to decrease something like intelligence and depending ",
                "on the factor of strength required, the same amount of intelligence would need to be decrease."
            ])
        ])
    ])
], magic=[
    magic_Aura,
    physicality,
    visacality
])

Aura = title(aura)

# Factions

astadi_retal = create_faction("Astadi Retal", "An ancient society that want to turn back progress to the days of "
                                              "knights and chivalry", short_name="astadi")
astadi = Reference(astadi_retal, "short_name", astadi_retal.short_name)
Astadi = title(astadi)
technologists = create_faction("Technologists", "A faction within technolas that combats against the astadi")

# Monoliths
islude = create_monolith("Islūdë", "The boundary between old and new")
sentinel = create_monolith("Sentinel", "is an unmanned station that provides an independent AI ineteface for Space " 
                           "Travel, Scanning and management")

# Characters
Radr = create_character("Radr", "A AIE Human, who evolved from Dsar")
Dsar = Reference(Radr, 'known_as', Radr.known_as("Dsar"))
Omedh = create_character("Ömedh", "A technologist who held out against the Radr")
Atabje_Weoh = create_character("Atabje Weoh", "Atabje is the first person other than Dsar to evolve in AIE, "
                                              "Weoh comes from weohnata(will in Ancient Language) signifying the "
                                              "future. brings hope of the future")
Atabje = Reference(Atabje_Weoh, 'known_as', Atabje_Weoh.known_as('Atabje'))

# Events
event_The_Radr = create_event("The Radr", "When Radr released the Radr the cloud of evolution and awakening")

# Objects
The_Radr = create_object("The Radr", "The cloud of evolution and awakening")
Ion_Cannon = create_object("Ion-Cannon", "Laser Cannons")

# Items
gren_disc = create_item("Gren Disc", "A Spinning, extremely sharp explosive Disc")
grenade_disc = Reference(gren_disc, "known_as", "Grenade Disc")
