
from GameSim.BotTraining.TrainerFullAct import TrainerFullAct
from GameSim.Render.Renderer import Renderer


def main():
    save = True
    train = True
    load_model = False
    delay = 1
    render_type = Renderer.RenderType.PYGAME
    episodes = 10_000

    load_path = "artifacts/models/first_fight/ppo_agent.pt"
    combat_sim_path = "CombatSim/"

    rend = Renderer(render_type=render_type)
    BigAwesomeBot = TrainerFullAct(episodes, rend, train=train, save=save, delay=delay, combat_sim_path=combat_sim_path)

    if load_model:
        BigAwesomeBot.controller.agent.load_models(load_path)

    BigAwesomeBot.run()


if __name__ == "__main__":
    main()
