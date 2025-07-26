import socket
import pickle
import pygame
import sys
import math

WIDTH, HEIGHT = 800, 600
SNAKE_SPEED = 8
TICK_RATE = 15


SERVER_IP = '127.0.0.1' 
SERVER_PORT = 5555

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Slither.io Multiplayer (Python)")
    clock = pygame.time.Clock()

  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))

  
    player_id = pickle.loads(s.recv(1024))

    direction = (SNAKE_SPEED, 0) 
    swipe_start = None  

    while True:
     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                s.close()
                sys.exit()
      
        mouse_pos = pygame.mouse.get_pos()
        head_pos = None
     
        if 'state' in locals() and state is not None and 'snakes' in state:
            snake = state['snakes'].get(player_id)
            if snake and len(snake['body']) > 0:
                head_pos = snake['body'][0]
        if head_pos:
            dx = mouse_pos[0] - head_pos[0]
            dy = mouse_pos[1] - head_pos[1]
            dist = math.hypot(dx, dy)
            if dist > 0:
                direction = (int(SNAKE_SPEED * dx / dist), int(SNAKE_SPEED * dy / dist))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction = (0, -SNAKE_SPEED)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction = (0, SNAKE_SPEED)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction = (-SNAKE_SPEED, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction = (SNAKE_SPEED, 0)

     
        try:
            s.sendall(pickle.dumps(direction))
        except:
            print("Disconnected from server.")
            break

        try:
            data = b""
            while True:
                part = s.recv(4096)
                data += part
                try:
                    state = pickle.loads(data)
                    break
                except:
                    continue
        except:
            print("Disconnected from server.")
            break

 
        screen.fill((0, 0, 0))
    
        for f in state['foods']:
            pygame.draw.circle(screen, (255, 0, 0), f, 7)
    
        for pid, snake in state['snakes'].items():
            color = snake['color']
            body = snake['body']
           
            for i, pos in enumerate(body):
                if i == 0:
                    continue 
              
                seg_color = tuple(min(255, c + (i % 2) * 30) for c in color)
                pygame.draw.circle(screen, seg_color, pos, 10)
         
            if body:
                head_pos = body[0]
                pygame.draw.circle(screen, color, head_pos, 14)
               
                dx, dy = 0, 0
                if len(body) > 1:
                    dx = head_pos[0] - body[1][0]
                    dy = head_pos[1] - body[1][1]
                    dist = math.hypot(dx, dy)
                    if dist != 0:
                        dx, dy = dx / dist, dy / dist
               
                eye_offset = 6
                eye_radius = 3
                ex1 = int(head_pos[0] + dx * eye_offset - dy * 4)
                ey1 = int(head_pos[1] + dy * eye_offset + dx * 4)
                ex2 = int(head_pos[0] + dx * eye_offset + dy * 4)
                ey2 = int(head_pos[1] + dy * eye_offset - dx * 4)
                pygame.draw.circle(screen, (255,255,255), (ex1, ey1), eye_radius)
                pygame.draw.circle(screen, (255,255,255), (ex2, ey2), eye_radius)
                pygame.draw.circle(screen, (0,0,0), (ex1, ey1), 1)
                pygame.draw.circle(screen, (0,0,0), (ex2, ey2), 1)

        pygame.display.flip()
        clock.tick(TICK_RATE)

if __name__ == "__main__":
    main() 
