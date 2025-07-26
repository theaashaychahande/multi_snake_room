# multi_snake_room

A simple multiplayer snake game inspired by Slither.io, built with Python, Pygame, and sockets.

## Features
- Multiple players control snakes that grow by eating food
- Real-time multiplayer over LAN
- Simple graphics using Pygame

## How to Run

### 1. Install Requirements
Make sure you have Python 3 and pip installed. Then install Pygame:

```
pip install pygame
```

### 2. Start the Server
Run this in one terminal:

```
python server.py
```

### 3. Start Clients
Run this in other terminals or computers (change `SERVER_IP` in `client.py` if not on the same machine):

```
python client.py
```

## Controls
- Arrow keys or WASD to control your snake

## Notes
- All players must be on the same network (LAN) unless you set up port forwarding.
- For learning/demo purposes only. Not production-ready. 
