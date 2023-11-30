# mazeCrawler
Welcome to the source code for our Spring 2022 COSC 465 Computer Networking Final Project Artifact. Here we designed an online game where players race to finish a randomly generated maze as fast as they can.


# Getting Started
In order to run this on a machine of your own, there are a few things you should know. First, **this project is written entirely in python version 3.** Also, you'll have to install the code to a local directory and a few packages that the code depends on including:
1. Pygame: to install run `pip3 install pygame` in your terminal

# Running the Game
1. Start the server by running `python3 Server_start.py`
1. Start a client by running `python3 client_start.py` (this can be done on the same machine as the server or another device)
1. Connect the client to the server by typing the server IP into the client terminal window (it is important to note that the client and server **MUST** be on the same port number).

# Important Notes
1. While playing the game, the controls are the arrow keys on your computer.
1. If you decide to quit, just close the window to properly leave the game.
1. There is no replay functionality built in, to play again you'll have to restart the server and reconnect the clients.

# References
1. Maze generation algorithm implementation based off: Joseph Bakulikira. 2021. Procedural Maze Generator Algorithms. GitHub. Retrieved March 25, 2022 from https://github.com/Josephbakulikira/Procedural-Maze-Generator-Algorithms
1. Mihail Dumitrescu and Nihar Sharma. 2011. Robust Networking in Multiplayer Games. Retrieved March 25, 2022 from http://courses.cms.caltech.edu/cs145/2011/robustgames.pdf
1. Takuji Iimura, Hiroaki Hazeyama, and Youki Kadobayashi. 2004. Zoned Federation of Game Servers. Proceedings of ACM SIGCOMM 2004 Workshops on NetGames ’04 Network and System Support for Games - SIGCOMM 2004 Workshops (2004). DOI: https://doi.org/10.1145/1016540.1016549
