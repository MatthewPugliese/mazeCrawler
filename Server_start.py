import pygame
import random
import time
import socket
import pickle
import labyrinth
import concurrent.futures

def server_program():
    player_Chords = {}
    clientnum = 0
    pygame.init()
    pygame.display.set_caption('Server')
    maze = labyrinth.getMaze()
    goal = labyrinth.getGoal()
    maze_walls = labyrinth.getWalls()
    print("1")
    screen = pygame.display.set_mode((1395, 1100))
    screen.fill((0, 0, 0))
    color = (0, 128, 255)
    maze.draw(goal)
    #pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(16,16,10,10))
    pygame.display.flip()



    print("2")
    message = [maze,goal]
    message = pickle.dumps(message)
    message += b"746869736973746865656e64"
    # get the hostname
    host = socket.gethostname()
    port = 2001  # initiate port no above 1024
    print("3")
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(5)
    #conn, address = server_socket.accept()  # accept new connection
    #conn.send(message)
    print("4")
    #conn.close()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            client_sock, client_addr = server_socket.accept()
            executor.submit(handle_client, client_sock, maze, goal, screen, message, player_Chords, clientnum)

    server_socket.close()

    return    

def handle_client(sock, maze, goal, screen, message, dict, clientnum):
    sock.send(message) #the maze and goal are sent to the client
    print("before")
    clientnum = clientnum + 1
    while True:
        cords = sock.recv(4096)
        data = b''
        while b"746869736973746865656e647373737373737373" not in data:
            packet = sock.recv(4096)
            if packet == b'':
                return
            print(packet)
            data += packet
        cord_array = pickle.loads(data)
        dict[clientnum] = cord_array#
        print(dict)
        
        draw_players(maze, goal, screen, dict, sock)

def draw_players(maze, goal, screen, dict, sock):
    for player in dict.values():
        pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(player[0],player[1],10,10))
    pygame.display.flip() 
    maze.draw(goal)
    cord_msg = pickle.dumps(dict)
    cord_msg += b"746869736973746865656e64"
    sock.send(cord_msg)
    #print("made it")  

if __name__ == '__main__':
    server_program()