import numpy as np

from QBot.Environments.States.EnemyState import EnemyState
from QBot.Environments.States.PlayerState import PlayerState


class CombatState:
    def __init__(self, player, enemies):
        # {
        #  "available_commands":["choose","key","click","wait","state"],
        #  "ready_for_command":true,
        #  "in_game":true,
        #  "game_state":
        #   {
        #     "choice_list":["talk"],
        #     "screen_type":"EVENT",
        #     "screen_state":
        #       {
        #         "event_id":"Neow Event",
        #         "body_text":"",
        #         "options":[
        #           {
        #             "choice_index":0,
        #             "disabled":false,
        #             "text":"[Talk]",
        #             "label":"Talk"
        #           }
        #         ],
        #         "event_name":"Neow"
        #       },
        #     "seed":4094997667555252601,
        #     "deck":[
        #       {
        #         "exhausts":false,
        #         "cost":1,
        #         "name":"Strike",
        #         "id":"Strike_P",
        #         "type":"ATTACK",
        #         "ethereal":false,
        #         "uuid":"c3dc8d97-9b06-4b79-ad2e-91d41d12b0a1",
        #         "upgrades":0,
        #         "rarity":"BASIC",
        #         "has_target":true
        #       },
        #       {
        #       "exhausts":false,
        #       "cost":1,
        #       "name":"Strike",
        #       "id":"Strike_P",
        #       "type":"ATTACK",
        #       "ethereal":false,
        #       "uuid":"dfddff14-65d5-4a03-9373-e6f5ac0f0b3b",
        #       "upgrades":0,
        #       "rarity":"BASIC",
        #       "has_target":true
        #       },
        #       {"exhausts":false,"cost":1,"name":"Strike","id":"Strike_P","type":"ATTACK","ethereal":false,"uuid":"322d8e8f-1953-4d29-a85d-0cac3ef47a3e","upgrades":0,"rarity":"BASIC","has_target":true},{"exhausts":false,"cost":1,"name":"Strike","id":"Strike_P","type":"ATTACK","ethereal":false,"uuid":"bb916eda-4fae-49f8-899d-c3fe8058d57e","upgrades":0,"rarity":"BASIC","has_target":true},{"exhausts":false,"cost":1,"name":"Defend","id":"Defend_P","type":"SKILL","ethereal":false,"uuid":"1a0ae3d6-67bd-4bfe-9c01-792751e0210e","upgrades":0,"rarity":"BASIC","has_target":false},{"exhausts":false,"cost":1,"name":"Defend","id":"Defend_P","type":"SKILL","ethereal":false,"uuid":"9f58d6bd-b740-442a-bad7-7a734e37efd8","upgrades":0,"rarity":"BASIC","has_target":false},{"exhausts":false,"cost":1,"name":"Defend","id":"Defend_P","type":"SKILL","ethereal":false,"uuid":"b024268c-a96b-44c2-86c5-b9a4ba35381a","upgrades":0,"rarity":"BASIC","has_target":false},{"exhausts":false,"cost":1,"name":"Defend","id":"Defend_P","type":"SKILL","ethereal":false,"uuid":"81e1bc8e-a0aa-4348-a9dc-eec2abb624b0","upgrades":0,"rarity":"BASIC","has_target":false},{"exhausts":false,"cost":2,"name":"Eruption","id":"Eruption","type":"ATTACK","ethereal":false,"uuid":"5f61bca8-0fad-459b-9a7c-4b831f3ff3bb","upgrades":0,"rarity":"BASIC","has_target":true},{"exhausts":false,"cost":2,"name":"Vigilance","id":"Vigilance","type":"SKILL","ethereal":false,"uuid":"6467c36a-77c4-43d1-b364-ce0e94589b23","upgrades":0,"rarity":"BASIC","has_target":false}],
        #     "relics":[
        #       {
        #         "name":"Pure Water",
        #         "id":"PureWater",
        #         "counter":-1
        #       }
        #     ],
        #     "max_hp":72,
        #     "act_boss":"The Guardian",
        #     "gold":99,
        #     "action_phase":"WAITING_ON_USER",
        #     "act":1,
        #     "screen_name":"NONE",
        #     "room_phase":"EVENT",
        #     "is_screen_up":false,
        #     "potions":[
        #       {
        #         "requires_target":false,
        #         "can_use":false,
        #         "can_discard":false,
        #         "name":"Potion Slot",
        #         "id":"Potion Slot"
        #       },
        #       {"requires_target":false,"can_use":false,"can_discard":false,"name":"Potion Slot","id":"Potion Slot"},
        #       {"requires_target":false,"can_use":false,"can_discard":false,"name":"Potion Slot","id":"Potion Slot"}
        #     ],
        #     "current_hp":72,
        #     "floor":0,
        #     "ascension_level":0,
        #     "class":"WATCHER",
        #     "map":[
        #       {
        #         "symbol":"M",                     # symbol = [M, E, $, ?]
        #         "children":[{"x":2,"y":1}],       # List of children
        #         "x":1,"y":0,
        #         "parents":[]
        #       },
        #       {
        #         "symbol":"M",
        #         "children":[{"x":3,"y":1}],
        #         "x":3,"y":0,
        #         "parents":[]
        #       },
        #       {
        #         "symbol":"M",
        #         "children":[{"x":6,"y":1}],
        #         "x":6,"y":0,
        #         "parents":[]
        #       },
        #       {
        #         "symbol":"M",
        #         "children":[{"x":1,"y":2},{"x":2,"y":2}],
        #         "x":2,"y":1,
        #         "parents":[]
        #       },
        #       {
        #         "symbol":"M",
        #         "children":[{"x":2,"y":2}],
        #         "x":3,"y":1,
        #         "parents":[]
        #       },
        #       {
        #         "symbol":"?",
        #         "children":[{"x":6,"y":2}],
        #         "x":6,"y":1,
        #         "parents":[]
        #       },
        #       {"symbol":"M","children":[{"x":1,"y":3}],"x":1,"y":2,"parents":[]},{"symbol":"?","children":[{"x":2,"y":3},{"x":3,"y":3}],"x":2,"y":2,"parents":[]},{"symbol":"M","children":[{"x":5,"y":3},{"x":6,"y":3}],"x":6,"y":2,"parents":[]},{"symbol":"M","children":[{"x":1,"y":4}],"x":1,"y":3,"parents":[]},{"symbol":"M","children":[{"x":1,"y":4},{"x":3,"y":4}],"x":2,"y":3,"parents":[]},{"symbol":"$","children":[{"x":3,"y":4}],"x":3,"y":3,"parents":[]},{"symbol":"?","children":[{"x":5,"y":4}],"x":5,"y":3,"parents":[]},{"symbol":"M","children":[{"x":6,"y":4}],"x":6,"y":3,"parents":[]},{"symbol":"?","children":[{"x":2,"y":5}],"x":1,"y":4,"parents":[]},{"symbol":"M","children":[{"x":4,"y":5}],"x":3,"y":4,"parents":[]},{"symbol":"M","children":[{"x":5,"y":5}],"x":5,"y":4,"parents":[]},{"symbol":"?","children":[{"x":5,"y":5}],"x":6,"y":4,"parents":[]},{"symbol":"R","children":[{"x":1,"y":6},{"x":3,"y":6}],"x":2,"y":5,"parents":[]},{"symbol":"R","children":[{"x":3,"y":6},{"x":4,"y":6}],"x":4,"y":5,"parents":[]},{"symbol":"?","children":[{"x":6,"y":6}],"x":5,"y":5,"parents":[]},{"symbol":"?","children":[{"x":0,"y":7}],"x":1,"y":6,"parents":[]},{"symbol":"M","children":[{"x":3,"y":7}],"x":3,"y":6,"parents":[]},{"symbol":"E","children":[{"x":3,"y":7}],"x":4,"y":6,"parents":[]},{"symbol":"M","children":[{"x":5,"y":7},{"x":6,"y":7}],"x":6,"y":6,"parents":[]},{"symbol":"M","children":[{"x":1,"y":8}],"x":0,"y":7,"parents":[]},{"symbol":"R","children":[{"x":2,"y":8},{"x":3,"y":8},{"x":4,"y":8}],"x":3,"y":7,"parents":[]},{"symbol":"R","children":[{"x":4,"y":8}],"x":5,"y":7,"parents":[]},{"symbol":"M","children":[{"x":6,"y":8}],"x":6,"y":7,"parents":[]},{"symbol":"T","children":[{"x":1,"y":9}],"x":1,"y":8,"parents":[]},{"symbol":"T","children":[{"x":1,"y":9}],"x":2,"y":8,"parents":[]},{"symbol":"T","children":[{"x":3,"y":9}],"x":3,"y":8,"parents":[]},{"symbol":"T","children":[{"x":4,"y":9},{"x":5,"y":9}],"x":4,"y":8,"parents":[]},{"symbol":"T","children":[{"x":6,"y":9}],"x":6,"y":8,"parents":[]},{"symbol":"M","children":[{"x":0,"y":10}],"x":1,"y":9,"parents":[]},{"symbol":"M","children":[{"x":4,"y":10}],"x":3,"y":9,"parents":[]},{"symbol":"?","children":[{"x":4,"y":10}],"x":4,"y":9,"parents":[]},{"symbol":"E","children":[{"x":4,"y":10}],"x":5,"y":9,"parents":[]},{"symbol":"M","children":[{"x":5,"y":10}],"x":6,"y":9,"parents":[]},{"symbol":"?","children":[{"x":0,"y":11},{"x":1,"y":11}],"x":0,"y":10,"parents":[]},{"symbol":"M","children":[{"x":3,"y":11},{"x":4,"y":11},{"x":5,"y":11}],"x":4,"y":10,"parents":[]},{"symbol":"E","children":[{"x":5,"y":11}],"x":5,"y":10,"parents":[]},{"symbol":"?","children":[{"x":0,"y":12}],"x":0,"y":11,"parents":[]},{"symbol":"M","children":[{"x":1,"y":12}],"x":1,"y":11,"parents":[]},{"symbol":"?","children":[{"x":3,"y":12}],"x":3,"y":11,"parents":[]},{"symbol":"M","children":[{"x":4,"y":12}],"x":4,"y":11,"parents":[]},{"symbol":"R","children":[{"x":4,"y":12},{"x":5,"y":12}],"x":5,"y":11,"parents":[]},{"symbol":"?","children":[{"x":0,"y":13}],"x":0,"y":12,"parents":[]},{"symbol":"M","children":[{"x":0,"y":13}],"x":1,"y":12,"parents":[]},{"symbol":"M","children":[{"x":4,"y":13}],"x":3,"y":12,"parents":[]},{"symbol":"M","children":[{"x":5,"y":13}],"x":4,"y":12,"parents":[]},{"symbol":"E","children":[{"x":6,"y":13}],"x":5,"y":12,"parents":[]},{"symbol":"M","children":[{"x":1,"y":14}],"x":0,"y":13,"parents":[]},{"symbol":"$","children":[{"x":5,"y":14}],"x":4,"y":13,"parents":[]},{"symbol":"$","children":[{"x":5,"y":14}],"x":5,"y":13,"parents":[]},{"symbol":"M","children":[{"x":5,"y":14}],"x":6,"y":13,"parents":[]},{"symbol":"R","children":[{"x":3,"y":16}],"x":1,"y":14,"parents":[]},{"symbol":"R","children":[{"x":3,"y":16}],"x":5,"y":14,"parents":[]}
        #     ],
        #     "room_type":"NeowRoom"
        #   }
        # }
        self.player_state = PlayerState(player)
        self.enemy_states = [EnemyState(enemy) for enemy in enemies]

    def get_state(self):
        # [[player_state], [[enemy_state] x 5]]
        deck_state, player_state = self.player_state.get_state()
        enemy_states = np.array([enemy_state.get_state() for enemy_state in self.enemy_states]).flatten()

        enemy_states = np.pad(enemy_states, (0, (max(0, (EnemyState.get_len()*3) - enemy_states.size))), constant_values=0)
        return deck_state, np.concatenate((player_state, enemy_states))
