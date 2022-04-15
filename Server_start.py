import pygame
import random
import time
import socket
import pickle
import labyrinth
import concurrent.futures

def server_program():
    pygame.init()
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
    port = 2000  # initiate port no above 1024
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
            executor.submit(handle_client, client_sock, maze, goal, screen, message)
            

    server_socket.close()

    return    

def handle_client(sock, maze, goal, screen, message):
    sock.send(message) #the maze and goal are sent to the client
    while True:
        cords = sock.recv(4096)
        data = b''
        while b"746869736973746865656e647373737373737373" not in data:
            packet = sock.recv(4096)
            print(packet)
            data += packet
        cord_array = pickle.loads(data)
        print(cord_array)
        pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(cord_array[0],cord_array[1],10,10))
        pygame.display.flip()
        maze.draw(goal)


if __name__ == '__main__':
    server_program()
