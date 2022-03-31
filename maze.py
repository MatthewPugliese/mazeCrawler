import pygame
import random
import time


pygame.init()
# all fonts used
font1 = pygame.font.SysFont("comicsansms", 49, True)
font2 = pygame.font.SysFont("comicsansms", 150, True)
font3 = pygame.font.SysFont("comicsansms", 28, True)


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

    # draws the maze
    def draw(self, goal):
        screen.fill((0, 0, 0))
        for k in self.maze_walls:
            pygame.draw.rect(screen, color, pygame.Rect(k[0],k[1],k[2],k[3]))

        #pygame.draw.rect(screen, color, pygame.Rect(695, 0, 300, 105)) # clock background
        pygame.draw.rect(screen, (0, 255, 0), goal) # finish

id = 0
running = True
while running:
    screen = pygame.display.set_mode((1395, 1100))
    done = False
    color = (0, 128, 255) # color of the walls
    x = 16
    y = 16
    #x1 = 16
    #y1 = 16
    id += 1
    maze = labyrinth(id)

    randomX = random.randint(0,1200)
    randomY = random.randint(528, 990)
    toAddx = randomX%33
    toAddy = randomY%33
    randomX = randomX - toAddx 
    randomY = randomY - toAddy
    goal = pygame.Rect(randomX+8,randomY+8,25,25)

    victory = False
    speed = 3 # movement speed
    pause = False
    pause_time = 0 # time spent in pause menue

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
            # move_up1 = True
            # move_down1 = True
            # move_left1 = True
            # move_right1 = True
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

        # victory screen
        
            # if pressed[pygame.K_w]:
            #         # checks if their is a overlap with the wall
            #         for m in maze.maze_walls:
            #             player1 = pygame.Rect(x1, y1 - speed, 10, 10)
            #             if player1.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
            #                 move_up1 = False
            #                 break
            #         if move_up1:
            #             y1 -= speed

            # if pressed[pygame.K_s]:
            #     player1 = pygame.Rect(x1, y1 + speed, 10, 10)
            #     for m in maze.maze_walls:
            #         if player1.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
            #             move_down1 = False
            #             break
            #     if move_down1:
            #         y1 += speed

            # if pressed[pygame.K_a]:
            #     player1 = pygame.Rect(x1 - speed, y1, 10, 10)
            #     for m in maze.maze_walls:
            #         if player1.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
            #             move_left1 = False
            #             break
            #     if move_left1:
            #         x1 -= speed

            # if pressed[pygame.K_d]:
            #     player1 = pygame.Rect(x1 + speed, y1, 10, 10)
            #     for m in maze.maze_walls:
            #         if player1.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
            #             move_right1 = False
            #             break
            #     if move_right1:
            #         x1 += speed

            # # checks if player has reached the goal
            # if goal.colliderect((x, y, 10, 10)):
            #     victory = True

            # if goal.colliderect((x1, y1, 10, 10)):
            #     victory = True

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
