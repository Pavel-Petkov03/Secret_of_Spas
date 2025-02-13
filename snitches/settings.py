from snitches.messages import SPAS_INTRO_MESSAGE, VILI_INTRO_MESSAGE, VLADI_INTRO_MESSAGE, EVA_INTRO_MESSAGE
from snitches.snitch import Snitch
from snitches.base_mission import EndOfMissionsMessage, ActionMission, InfoMessage

Vladi = Snitch("Vladi", None)
Eva = Snitch("Eva", Vladi)
Vili = Snitch("Vili", Eva)
Spas = Snitch("Spas", Vili)

Spas.add_missions([
    InfoMessage(Spas, SPAS_INTRO_MESSAGE),
    ActionMission(Spas, "Grapes(for rakiq)", 10),
    ActionMission(Spas, "Apples(for rakiq)", 20),
    ActionMission(Spas, "Cherries(for rakiq)", 15),
    ActionMission(Spas, "Blueberries(for rakiq)", 20),
    EndOfMissionsMessage(Spas)
])

Eva.add_missions([
    InfoMessage(Eva, EVA_INTRO_MESSAGE),
    ActionMission(Eva, "Grapes(for wine)", 10),
    ActionMission(Eva, "Bananas(for wine)", 20),
    ActionMission(Eva, "Lemons(for gin)", 15),
    ActionMission(Eva, "Carrots(for gin)", 20),
    EndOfMissionsMessage(Eva)
])

Vili.add_missions([
    InfoMessage(Vili, VILI_INTRO_MESSAGE),
    ActionMission(Vili, "Pineapples(for gin)", 10),
    ActionMission(Vili, "Cucumbers(for gin)", 20),
    ActionMission(Vili, "Pears(for wine)", 15),
    ActionMission(Vili, "Potatoes(for wine)", 20),
    EndOfMissionsMessage(Vili)
])

Vladi.add_missions([
    InfoMessage(Vladi, VLADI_INTRO_MESSAGE),
    ActionMission(Vladi, "Potatoes(for vodka)", 10),
    ActionMission(Vladi, "Bananas(for vodka)", 20),
    ActionMission(Vladi, "Plums(for vodka)", 15),
    ActionMission(Vladi, "Pears(for vodka)", 20),
    EndOfMissionsMessage(Vladi)
])

SNITCHES_ARRAY = [Spas, Vili, Vladi, Eva]

SNITCHES = {snitch.name: snitch for snitch in SNITCHES_ARRAY}
