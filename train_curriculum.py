from transformers.pipelines.image_text_to_text import add_images_to_messages

from CombatSim.Entities.Dungeon.SpikeSlimeMedium import SpikeSlimeMedium
from CombatSim.util import get_default_deck
from GameSim.BotTraining.Trainer import Trainer
from GameSim.BotTraining.Regimen import Regimen
from GameSim.Render.Renderer import Renderer


def main():
    save = True
    train = True
    delay = 0
    render_type = Renderer.RenderType.NONE

    rend = Renderer(render_type=render_type)
    BigAwesomeBot = Trainer(rend, train=train, save=save, delay=delay)
    basic_combats = Regimen(
            max_episodes=60_000,
            possible_enemies=       ["Cultist"],
            num_enemies=            [1,2],
            default_deck=           get_default_deck(),
            num_additional_cards=   0,
            additional_cards=       None,
            allow_repeat_enemies=   True,
            player_max_health=      70,
            player_start_health=    70,
            max_gauntlet_length=    20
    )

    reduce_variance_combats = Regimen(
            max_episodes=40_000,
            possible_enemies=     ["Cultist", "JawWorm", "GreenLouse", "RedLouse", "SpikeSlimeMedium", "AcidSlimeMedium"],
            num_enemies=          [1,2,2,2,2,3],
            default_deck=         ["FollowUp", "TalktotheHand", "Protect", "CarveReality", "DeceiveReality",
                                                                "Eruption", "Vigilance","BattleHymn"],
            num_additional_cards= 4,
            additional_cards=     {"Strike":0.5, "Defend": 0.5},
            allow_repeat_enemies= False,
            player_max_health =   70,
            player_start_health = 70,
            max_gauntlet_length=  20
    )

    # "Lagavulin", "GremlinNob",
    elite_combats = Regimen(
            max_episodes=           40_000,
            possible_enemies=       [ "GremlinNob", "Lagavulin", ["Sentry", "Sentry", "Sentry"]],
            num_enemies=            1,
            default_deck=           ["Strike", "Strike", "Strike", "Strike", "Defend", "Defend", "Defend", "Eruption", "Vigilance"],
            num_additional_cards=   3,
            additional_cards=       {"CutThroughFate": 0.1, "BowlingBash": 0.1, "FollowUp" : 0.1, "TalktotheHand": 0.1, "CarveReality": 0.1, "Brilliance": 0.1,
                                        "FlurryofBlows": 0.1, "Tantrum": 0.1, "ReachHeaven": 0.1, "Rushdown": 0.1},
            allow_repeat_enemies=   True,
            player_max_health=      70,
            player_start_health=    70,
            max_gauntlet_length=    3
    )

    BigAwesomeBot.add_regimen(basic_combats)
    BigAwesomeBot.add_regimen(reduce_variance_combats)
    BigAwesomeBot.add_regimen(elite_combats)
    BigAwesomeBot.run()


if __name__ == "__main__":
    main()