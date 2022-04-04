import pygame
import random
import time
import socket
import pickle
import labyrinth


def server_program():
    maze = labyrinth.getMaze()
    goal = labyrinth.getGoal()
    maze_walls = labyrinth.getWalls()

    screen = pygame.display.set_mode((1395, 1100))
    screen.fill((0, 0, 0))
    color = (0, 128, 255)
    pygame.draw.rect(screen, (0, 255, 0), goal) # finish
    maze.draw(goal)
    pygame.draw.rect(screen, (138,43,226), pygame.Rect(16,16,10,10))

    message = [maze,goal]
    message = pickle.dumps(message)
    # get the hostname
    host = socket.gethostname()
    port = 2000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(1)
    #while True:
        #conn, address = server_socket.accept()  # accept new connection
        #conn.send(message)
        
    #conn.close()

if __name__ == '__main__':
    server_program()
