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
            # Receive direction from client
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

