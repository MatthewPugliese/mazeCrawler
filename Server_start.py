from os import chroot
import pygame
import socket
import pickle
import labyrinth
import concurrent.futures
import threading
import time
import random

def server_program():
    """
    Principal function that initiates the server and accepts client connections
    """
    maze = labyrinth.getMaze()
    goal = labyrinth.getGoal()
    player_colors = [[255,188,66],[216,17,89],[226,160,255],[183,255,216],[255,220,204],[251,99,118],[100,245,141],[255,202,58],[138,201,38],[247,99,0],[237,37,78],[3,252,86],[233,223,0]]
    player_coords = {}
    
    lock = threading.Lock()
    difficulty = False
    # same maze and goal for every client
    # maze, goal, difficulty all coded in message    
    message = [maze,goal,difficulty]
    message = pickle.dumps(message)
    message += b"746869736973746865656e64"

    # dynamic hostname retreival
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    print("Host IP is:", host)
    
    port = 2000  # initiate port above 1024
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(5)

    # thread method executer to run indefinitly, accept client connections, and handle clients
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            client_sock, client_addr = server_socket.accept()
            print("Client Connected")
            executor.submit(handle_client, client_sock, message, player_coords)
            executor.submit(data_receiver, client_sock, player_coords, client_addr, player_colors, lock)

def data_receiver(client_socket, player_coords, client_addr, player_colors, lock):
    """
    Threaded function to handle client coordinate updates

    :param client_socket: the socket a particular client is using
    :param player_coords: dictionary containing the current coordinates for every client (key client_addr, value array of coordinates)
    :param client_addr: the IP address of a connection
    :param player_colors: array containing unique colors in RGB format
    """   
    # assign players a unique random color from dictionary
    player_color = random.choice(player_colors)
    player_colors.remove(player_color) 
    
    # constantly receive updates from player
    while(True):
        data = b''
        # waits to receive entire message based on bytestring
        while b"746869736973746865656e647373737373737373" not in data:
            packet = client_socket.recv(4096)
            data += packet
        lock.acquire()
        cord_array = pickle.loads(data)
        lock.release()

        # player left the game
        if(cord_array == "quit"):
            #delete player
            lock.acquire()
            del player_coords[client_addr]
            lock.release()
            print("client disconnected")
        
        # player won - send to all players
        elif(cord_array == "win"):
            lock.acquire()
            player_coords[client_addr] = "win"
            lock.release()
        
        # update player coord array
        else:
            lock.acquire()
            cord_array.append(player_color)
            player_coords[client_addr] = cord_array
            lock.release()

def handle_client(sock, message, player_coords):
    """
    Threaded function to initialize and update clients 

    :param sock: the socket a particular client is using
    :param message: the maze and goal as a pickled object
    :param player_coords: the dictionary containing all player coordinates
    """  
    sock.send(message) #the maze and goal are sent to the client
    
    # constantly send updates to client
    while True:
        cord_msg = pickle.dumps(player_coords)
        cord_msg += b"746869736973746865656e64"
        sock.send(cord_msg) 
        time.sleep(.03)

if __name__ == '__main__':
    server_program()