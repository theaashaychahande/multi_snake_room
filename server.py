import socket
import threading
import pickle
import random
import time

WIDTH, HEIGHT = 800, 600
FOOD_COUNT = 20
SNAKE_INIT_LENGTH = 5
SNAKE_SPEED = 5
TICK_RATE = 15

SERVER_IP = '0.0.0.0'
SERVER_PORT = 5555


snakes = {} 
foods = []

lock = threading.Lock()

def random_pos():
    return (random.randint(20, WIDTH-20), random.randint(20, HEIGHT-20))

def spawn_food():
    while len(foods) < FOOD_COUNT:
        foods.append(random_pos())

def handle_client(conn, addr, player_id):
    global snakes
    print(f"[NEW CONNECTION] {addr} as {player_id}")
  
    conn.sendall(pickle.dumps(player_id))
    
    color = tuple(random.randint(50, 255) for _ in range(3))
    start_pos = random_pos()
    direction = (SNAKE_SPEED, 0)
    with lock:
        snakes[player_id] = {
            'body': [start_pos] * SNAKE_INIT_LENGTH,
            'dir': direction,
            'color': color,
            'alive': True
        }
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
           
            direction = pickle.loads(data)
            with lock:
                if player_id in snakes:
                    snakes[player_id]['dir'] = direction
    except Exception as e:
        print(f"[DISCONNECT] {player_id} {e}")
    finally:
        with lock:
            if player_id in snakes:
                del snakes[player_id]
        conn.close()

def game_loop():
    global snakes, foods
    while True:
        time.sleep(1 / TICK_RATE)
        with lock:
          
            for pid, snake in snakes.items():
                if not snake['alive']:
                    continue
                dx, dy = snake['dir']
                head_x, head_y = snake['body'][0]
                new_head = (head_x + dx, head_y + dy)
              
                new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)
                snake['body'].insert(0, new_head)
              
                ate = False
                for f in foods:
                    if (abs(new_head[0] - f[0]) < 10) and (abs(new_head[1] - f[1]) < 10):
                        foods.remove(f)
                        ate = True
                        break
                if not ate:
                    snake['body'].pop()  
              
                if new_head in snake['body'][1:]:
                    snake['alive'] = False
            spawn_food()
          
            state = {'snakes': snakes, 'foods': foods}
            for conn in connections:
                try:
                    conn.sendall(pickle.dumps(state))
                except:
                    pass

connections = []

def accept_clients(server):
    player_id = 0
    while True:
        conn, addr = server.accept()
        connections.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr, player_id), daemon=True).start()
        player_id += 1

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen()
    print(f"[SERVER STARTED] {SERVER_IP}:{SERVER_PORT}")
    threading.Thread(target=game_loop, daemon=True).start()
    accept_clients(server)

if __name__ == "__main__":
    main() 

