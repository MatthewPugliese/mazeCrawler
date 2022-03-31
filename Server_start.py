import pygame
import random
import time
import socket
import pickle



class cell:
    def __init__(self,up,down,left,right):
        self.visited = False
        self.walls = [up,down,left,right]

class labyrinth:
    # generates the maze
    def __init__(self,id):
        self.id = id
        self.walls = []
        self.maze_walls = []
        self.cells = []

        x = 0
        t = 0

        # creates all cell within the maze
        for f in range(32):
            for s in range(42):
                self.cells.append(cell((x + 8, t, 25, 8), (x + 8, t + 33, 25, 8), (x, t + 8, 8, 25), (x + 33, t + 8, 8, 25)))
                x += 33
            x = 0
            t += 33

        # generates maze using prim's algorithm
        for v in self.cells[0].walls:
            self.maze_walls.append(v)
            self.walls.append(v)

        self.cells[0].visited = True

        while len(self.walls) > 0:
            wall = random.choice(self.walls)
            # checks which cells are divided by the wall
            divided_cells = []
            for u in self.cells:
                if wall in u.walls:
                    divided_cells.append(u)

            if len(divided_cells) > 1 and (not ((divided_cells[0].visited and divided_cells[1].visited) or ((not divided_cells[0].visited) and (not divided_cells[1].visited)))):
                # checks which cells have been visited
                for k in divided_cells:
                    k.walls.remove(wall)

                    if k.visited == False:
                        k.visited = True

                    for q in k.walls:
                        if not q in self.walls:
                            self.walls.append(q)

                        if not q in self.maze_walls:
                            self.maze_walls.append(q)

                    if wall in self.maze_walls:
                        self.maze_walls.remove(wall)

            self.walls.remove(wall)

        for j in range(0,1100,33):
            for i in range(0,1395,33):
                self.maze_walls.append((i, j, 8, 8))

screen = pygame.display.set_mode((1395, 1100))
done = False
color = (0, 128, 255) # color of the walls
id = 0
maze = labyrinth(id)
randomX = random.randint(0,1200)
randomY = random.randint(528, 990)
toAddx = randomX%33
toAddy = randomY%33
randomX = randomX - toAddx 
randomY = randomY - toAddy
goal = pygame.Rect(randomX+8,randomY+8,25,25)
message = [maze,goal]
message = pickle.dumps(message)


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 2000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(1)
    while True:
        conn, address = server_socket.accept()  # accept new connection
        conn.send(message)
        
    conn.close()

if __name__ == '__main__':
    server_program()
