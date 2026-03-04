
from GameSim.BotTraining.TrainerFullAct import TrainerFullAct
from GameSim.BotTraining.TrainingVisualizer import TrainingVisualizer
from GameSim.Render.Renderer import Renderer


def main():
    save = True
    train = True
    load_model = False
    delay = 0.25
    render_type = Renderer.RenderType.PYGAME
    episodes = 10_000

    load_path = "artifacts/models/first_fight/ppo_agent.pt"
    combat_sim_path = "CombatSim/"

    visualizer = TrainingVisualizer(port=5000)
    visualizer.start()

    rend = Renderer(render_type=render_type)
    BigAwesomeBot = TrainerFullAct(episodes, rend, train=train, save=save, delay=delay, combat_sim_path=combat_sim_path,
                                   visualizer=visualizer)

    if load_model:
        BigAwesomeBot.controller.agent.load_models(load_path)

    BigAwesomeBot.run()


if __name__ == "__main__":
    main()
