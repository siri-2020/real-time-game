from game_field import GameField
from player import Player
from npc import NPC
from graphics_engine import GraphicsEngine
from input_controller import InputController
from game_engine import GameEngine

def main():
    game_field = GameField(0, 0, 1280, 720)
    player = Player(640, 360)
    npc1 = NPC(200, 200, 100, 150)
    npc2 = NPC(1000, 500, -120, 80)
    graph_engine = GraphicsEngine(1280, 720)
    input_controller = InputController()
    game_engine = GameEngine(graph_engine, input_controller, game_field, player, npc1, npc2, fps=60)
    game_engine.run_game()

if __name__ == "__main__":
    main()