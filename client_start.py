import pygame
import time
import socket
import pickle
import threading
import queue

print("Enter Server IP: ", end ="")
host = input()
print("Joining server at:" , host)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("mazeSong.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()

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
pause_time = 0 # time spent in pause menu
latency = 0
startTime = 0

port = 2001  # socket server port number
client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server 
data_queue = queue.Queue()

def client_program(client_socket):
    """
    Principal function that receives the initial data from the server (maze, goal, color)
    """
    data = b''

    # waits to receive entire message based on bytestring
    while b"746869736973746865656e64" not in data:
        packet = client_socket.recv(4096)
        data += packet

    data_arr= pickle.loads(data)

    return data_arr # close the connection

def data_receiver(client_socket, queue):
    """
    Threaded function to handle client coordinate updates from server
    :param client_socket: the socket the particular client is using
    :param queue: queue containing the updates in order as received
    """
    count = 0
    
    #loop for duration of game
    while(not done):
        data = b''
        try:
            # wait to receive full message
            while b"746869736973746865656e64" not in data:
                packet = client_socket.recv(4096)
                data += packet
            #print("updated chords:", count)
            count += 1
            stuff = pickle.loads(data)
            queue.put(stuff)
        except:
            pass
        latency = time.time() - startTime #in seconds
        latency = latency * 100 #in milliseconds
        latency = str(latency)[:5]
        print(latency, "ms of latency")


data = client_program(client_socket)
maze = data[0]
goal = data[1]
difficulty = data[2]
Loss = False
data_receiver = threading.Thread(target=data_receiver, args=(client_socket, data_queue))
data_receiver.start()
coords = {}
while not done:

    if Loss:
        screen.fill((0, 0, 0))
        victory_text = font2.render("DEFEAT!",True,(255,255,255))
        screen.blit(victory_text,(700 - (victory_text.get_width() // 2), 550 - (victory_text.get_height() // 2)))
        pygame.display.flip()

    oldX = x
    oldY= y
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
            cords = "quit"
            cords = pickle.dumps(cords)
            cords += b"746869736973746865656e647373737373737373"
            client_socket.send(cords)
            pygame.display.quit()
            pygame.quit()

        if event.type == pygame.KEYDOWN and not done:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                if pause:
                    pause = False
                    pause_time += time.time() - pause_time_start
                else:
                    pause = True
                    pause_time_start = time.time()

            if event.key == pygame.K_RETURN:
                done = True

    if pause and not done:
        screen.fill((0, 0, 0))
        pause_text = font2.render("PAUSE",True,(255,255,255))
        screen.blit(pause_text, (700 - (pause_text.get_width() // 2), 550 - (pause_text.get_height() // 2)))

    # the actual game
    if not victory and not pause and not Loss and not done:
        move_up = True
        move_down = True
        move_left = True
        move_right = True
        pressed = pygame.key.get_pressed()

        if  pressed[pygame.K_UP] or pressed[pygame.K_w]:
            # checks if their is a overlap with the wall
            for m in maze.maze_walls:
                player = pygame.Rect(x, y - speed, 10, 10)
                if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                    move_up = False
                    if(difficulty==True):
                        x = 16
                        y = 16
                    break
            if move_up:
                y -= speed

        if  pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            player = pygame.Rect(x, y + speed, 10, 10)
            for m in maze.maze_walls:
                if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                    move_down = False
                    if(difficulty==True):
                        x = 16
                        y = 16
                    break
            if move_down:
                y += speed

        if  pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            player = pygame.Rect(x - speed, y, 10, 10)
            for m in maze.maze_walls:
                if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                    move_left = False
                    if(difficulty==True):
                        x = 16
                        y = 16
                    break
            if move_left:
                x -= speed

        if  pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            player = pygame.Rect(x + speed, y, 10, 10)
            for m in maze.maze_walls:
                if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                    move_right = False
                    if(difficulty==True):
                        x = 16
                        y = 16
                    break
            if move_right:
                x += speed

            # checks if player has reached the goal
        if goal.colliderect((x, y, 10, 10)):
            victory = True
            # draws the screen
        
        if not oldX == x or not oldY == y:
            cords = [x,y]
            cords = pickle.dumps(cords)
            cords += b"746869736973746865656e647373737373737373"
            client_socket.send(cords)

        startTime = time.time()     #####latency count

        try:
            coords = data_queue.get_nowait()
        except queue.Empty:
            pass
        for player in coords.values():
            if(player == "win"):
                Loss = True
            else:
                pygame.draw.rect(screen, (player[2][0],player[2][1],player[2][2]), pygame.Rect(player[0],player[1],10,10))
        pygame.display.flip() 
        maze.draw(goal)

    if victory and not done:
        screen.fill((0, 0, 0))
        victory_text = font2.render("VICTORY!",True,(255,255,255))
        screen.blit(victory_text,(700 - (victory_text.get_width() // 2), 550 - (victory_text.get_height() // 2)))
        cords = "win"
        cords = pickle.dumps(cords)
        cords += b"746869736973746865656e647373737373737373"
        client_socket.send(cords)
        pygame.display.flip()
