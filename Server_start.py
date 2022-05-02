from os import chroot
import pygame
import socket
import pickle
import labyrinth
import concurrent.futures
import time
import random


def data_receiver(client_socket, dict, client_addr):
    player_color = [random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)]
    while(True):
        data = b''
        while b"746869736973746865656e647373737373737373" not in data:
            packet = client_socket.recv(4096)
            data += packet
        cord_array = pickle.loads(data)
        if(cord_array == "quit"):
            #delete player 
            del dict[client_addr]
            print("client disconnected")
        else:
            cord_array.append(player_color)
            dict[client_addr] = cord_array


def server_program():
    pygame.init()
    pygame.display.set_caption('Server')
    maze = labyrinth.getMaze()
    goal = labyrinth.getGoal()
    maze_walls = labyrinth.getWalls()
    screen = pygame.display.set_mode((1395, 1100))
    screen.fill((0, 0, 0))
    color = (0, 128, 255)
    maze.draw(goal)
    pygame.display.flip()
    player_Chords = {}



    message = [maze,goal]
    message = pickle.dumps(message)
    message += b"746869736973746865656e64"
    host = "149.43.218.169"
    port = 2001  # initiate port no above 1024
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(5)


    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            client_sock, client_addr = server_socket.accept()
            print("Client Connected")
            executor.submit(handle_client, client_sock, maze, goal, screen, message, player_Chords)
            executor.submit(data_receiver, client_sock, player_Chords, client_addr)
    

def handle_client(sock, maze, goal, screen, message, dict):
    sock.send(message) #the maze and goal are sent to the client
    while True:
            draw_players(maze, goal, screen, dict, sock)
            time.sleep(.03)
        

def draw_players(maze, goal, screen, dict, sock):
    # for player in dict.values():
    #     pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(player[0],player[1],10,10))
    # pygame.display.flip() 
    # maze.draw(goal)
    cord_msg = pickle.dumps(dict)
    cord_msg += b"746869736973746865656e64"
    sock.send(cord_msg) 

if __name__ == '__main__':
    server_program()
