from snitches.messages import SPAS_INTRO_MESSAGE
from snitches.snitch import Snitch
from snitches.base_mission import EndOfMissionsMessage, ActionMission, InfoMessage

Vlad = Snitch("Vladi", None)
Vili = Snitch("Vili", Vlad)
Pesho = Snitch("Pesho", Vili)
Spas = Snitch("Spas", Pesho)

Spas.add_missions([
    InfoMessage(Spas, SPAS_INTRO_MESSAGE),
    ActionMission(Spas, "Grapes", 10),
    ActionMission(Spas, "Apples", 20),
    ActionMission(Spas, "Cherries", 15),
    ActionMission(Spas, "Blueberries", 20),
    EndOfMissionsMessage(Spas)
])

Pesho.add_missions([
    InfoMessage(Pesho, SPAS_INTRO_MESSAGE),
    # todo add missions
    EndOfMissionsMessage(Pesho)
])

Vili.add_missions([
    InfoMessage(Vili, SPAS_INTRO_MESSAGE),
    # todo add missions
    EndOfMissionsMessage(Vili)
])

Vlad.add_missions([
    InfoMessage(Vlad, SPAS_INTRO_MESSAGE),
    # todo add missions
    EndOfMissionsMessage(Vlad)
])

SNITCHES_ARRAY = [Spas, Vili, Vlad, Pesho]

SNITCHES = {snitch.name: snitch for snitch in SNITCHES_ARRAY}
