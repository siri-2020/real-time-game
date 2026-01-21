import socket
import time
import threading
from game_field import GameField
from player import Player
from net_server_engine import ServerGameEngine

HOST = '0.0.0.0'
PORT = 21001
FPS = 60

game_field = GameField(0, 0, 800, 600)
game_engine = ServerGameEngine(game_field, fps=FPS)

def client_handler(conn, player_id):
    """Handles communication with a single client."""
    print(f"Player {player_id} handler started.")
    
    new_player = Player(100, 100, 3, 3)
    new_player.id = player_id
    game_engine.add_player(new_player)

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            
            try:
                actions = eval(data.decode())
                game_engine.set_player_actions(player_id, actions)
            except:
                pass 

            state = game_engine.get_game_state_data()
            
            state["self"] = player_id
            
            conn.sendall(str(state).encode())
            
        except Exception as e:
            print(f"Connection error with {player_id}: {e}")
            break

    print(f"Player {player_id} disconnected.")
    game_engine.remove_player(player_id)
    conn.close()

def game_loop_thread():
    """Runs the physics simulation independently of network calls."""
    while True:
        game_engine.update_state()
        time.sleep(1/FPS)

if __name__ == "__main__":
    physics_thread = threading.Thread(target=game_loop_thread)
    physics_thread.daemon = True
    physics_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        
        client_id_counter = 0
        
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            client_id_counter += 1
            
            t = threading.Thread(target=client_handler, args=(conn, client_id_counter))
            t.start()
