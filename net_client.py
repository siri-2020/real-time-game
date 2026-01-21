import socket
from graphics_engine import GraphicsEngine
from input_controller import InputController

HOST = '127.0.0.1'
PORT = 21001

class NetGraphicsEngine(GraphicsEngine):
    def render_text(self, text, x, y, color="white"):
        import pygame
        font = pygame.font.SysFont(None, 24)
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server")

        graph_engine = NetGraphicsEngine(800, 600) 
        input_controller = InputController()

        while True:
            pkeys = input_controller.get_pressed_keys()
            
            actions = {}
            if "w" in pkeys: actions["up"] = 1
            if "s" in pkeys: actions["down"] = 1
            if "a" in pkeys: actions["left"] = 1
            if "d" in pkeys: actions["right"] = 1
            if "q" in pkeys: break

            s.send(str(actions).encode())

            data = s.recv(4096) 
            if not data:
                print("Server disconnected")
                break
                
            state = eval(data.decode())

            graph_engine.start_frame()

            my_id = state.get("self")
            
          for npc_pos in state.get("npcs", []):
                graph_engine.render_circle(npc_pos[0], npc_pos[1], 10, "blue")

            players = state.get("players", {})
            for pid, pdata in players.items():
                x, y, score = pdata
                
                color = "green" if pid == my_id else "red"
                graph_engine.render_circle(x, y, 20, color)
                
                try:
                    graph_engine.render_text(f"Score: {score}", x - 20, y - 40)
                except AttributeError:
                    print(f"Player {pid} Score: {score}")

            graph_engine.show_frame()

if __name__ == "__main__":
    run_client()
