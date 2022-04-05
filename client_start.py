
import pygame
import random
import time
import socket
import pickle
from Server_start import labyrinth

pygame.init()

font1 = pygame.font.SysFont("comicsansms", 49, True)
font2 = pygame.font.SysFont("comicsansms", 150, True)
font3 = pygame.font.SysFont("comicsansms", 28, True)
screen = pygame.display.set_mode((1395, 1100))
done = False
color = (0, 128, 255) # color of the walls
x = 16
y = 16
victory = False
speed = 3 # movement speed
pause = False
pause_time = 0 # time spent in pause menue

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 2000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server 
    data = b''

    while True:
        packet = client_socket.recv(4096)
        if packet is None:
            print("NONE")
            break
        data += packet

    data_arr= pickle.loads(data)
    print(data_arr)
    client_socket.close() 
    return data_arr # close the connection

data = client_program()
print("data")
print(data)
maze = data[0]
goal = data[1]
while not done:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                if pause:
                    pause = False
                    pause_time += time.time() - pause_time_start
                else:
                    pause = True
                    pause_time_start = time.time()

            if event.key == pygame.K_RETURN:
                done = True

    if pause:
        screen.fill((0, 0, 0))
        pause_text = font2.render("PAUSE",True,(255,255,255))
        screen.blit(pause_text, (700 - (pause_text.get_width() // 2), 550 - (pause_text.get_height() // 2)))

        # the actual game
    if not victory and not pause:
        move_up = True
        move_down = True
        move_left = True
        move_right = True
        pressed = pygame.key.get_pressed()

            # movment
        if  pressed[pygame.K_UP] or pressed[pygame.K_w]:
                # checks if their is a overlap with the wall
            for m in maze.maze_walls:
                player = pygame.Rect(x, y - speed, 10, 10)
                if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                    move_up = False
                    break
            if move_up:
                y -= speed

        if  pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            player = pygame.Rect(x, y + speed, 10, 10)
            for m in maze.maze_walls:
                if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                    move_down = False
                    break
            if move_down:
                y += speed

        if  pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            player = pygame.Rect(x - speed, y, 10, 10)
            for m in maze.maze_walls:
                if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                    move_left = False
                    break
            if move_left:
                x -= speed

        if  pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            player = pygame.Rect(x + speed, y, 10, 10)
            for m in maze.maze_walls:
                if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                    move_right = False
                    break
            if move_right:
                x += speed

            # checks if player has reached the goal
        if goal.colliderect((x, y, 10, 10)):
                victory = True

            # draws the screen
        maze.draw(goal)
            #text = draw_time(start, pause_time)
        pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(x,y,10,10))
            #screen.blit(text[0], (700, 15))
            

            # draws the screen
        maze.draw(goal)
            #text = draw_time(start, pause_time)
        pygame.draw.rect(screen, (138,43,226), pygame.Rect(x,y,10,10))
            #pygame.draw.rect(screen, (255,182,193), pygame.Rect(x1,y1,10,10))
            #screen.blit(text[0], (700, 15))

        # victory screen
    if victory:
        screen.fill((0, 0, 0))
        victory_text = font2.render("VICTORY!",True,(255,255,255))
        reset = font3.render("(Press Enter to Start New Game)",True,(255,255,255))
        screen.blit(victory_text,(700 - (victory_text.get_width() // 2), 550 - (victory_text.get_height() // 2)))

        #clock.tick(60)
    pygame.display.flip()
