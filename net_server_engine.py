import random
from player import Player
from npc import NPC

class ServerGameEngine:
    def __init__(self, game_field, *, fps=60):
        self.game_field = game_field
        self.players = []
        self.npcs = []
        self.scores = {} 
        self.fps = fps
        self.running = False
        
        for _ in range(5):
            self.spawn_npc()

    def spawn_npc(self):
        x = random.randint(self.game_field.x_min, self.game_field.x_max)
        y = random.randint(self.game_field.y_min, self.game_field.y_max)
        vx = random.choice([-2, -1, 1, 2])
        vy = random.choice([-2, -1, 1, 2])
        self.npcs.append(NPC(x, y, vx, vy))

    def add_player(self, player):
        self.players.append(player)
        self.scores[player.id] = 0

    def remove_player(self, player_id):
        self.players = [p for p in self.players if p.id != player_id]
        if player_id in self.scores:
            del self.scores[player_id]

    def set_player_actions(self, player_id, actions):
        for p in self.players:
            if p.id == player_id:
                p.current_actions = actions
                break

    def get_game_state_data(self):
        players_data = {}
        for p in self.players:
            players_data[p.id] = (p.x, p.y, self.scores.get(p.id, 0))
        
        npcs_data = [(npc.x, npc.y) for npc in self.npcs]
        
        return {
            "players": players_data,
            "npcs": npcs_data
        }

    def check_consumption(self):
        for p in self.players:
            for npc in self.npcs[:]:
                distance = ((p.x - npc.x)**2 + (p.y - npc.y)**2)**0.5
                if distance < 40:
                    self.npcs.remove(npc)
                    self.scores[p.id] += 1
                    self.spawn_npc() 

    def update_state(self):
        for npc in self.npcs:
            npc.move(self.game_field, 1) 

        for p in self.players:
            actions = getattr(p, "current_actions", {})
            p.move(
                "a" in actions, 
                "d" in actions, 
                "w" in actions, 
                "s" in actions, 
                self.game_field, 
                1
            )
        
        self.check_consumption()

    def run(self):
        pass
