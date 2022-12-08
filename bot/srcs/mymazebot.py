# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    mymazebot.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: absalhi <absalhi@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/07 15:01:47 by absalhi           #+#    #+#              #
#    Updated: 2022/12/08 16:20:36 by absalhi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

if __name__ == "__main__":

    from utilities import printf, RED
    
    printf("Please run the game using the main.py file.\n", RED)
    exit(1)

from random import choices
from math import sqrt
from os import system, fork
from configparser import ConfigParser
from time import sleep
from tkinter import *

from srcs.utilities import *
from srcs.player import Player


class MyMazeBot:

    def __init__(self):

        """
        This class contains the MyMaze game solver.
        """
        
        while True:
            
            clear()
            printf("Enter the map path: ", BLUE)
            self.path = input()

            if not self.path == "":
                
                try:
                    
                    f = open(self.path, "r")

                    break
                    
                except FileNotFoundError:
                    
                    printf(f"{self.path}: invalid path.\n", RED)
                    printf("Press ENTER to try again...")
                    input()

        _rows = f.readlines()
        self.n_rows, self.n_columns = len(_rows), len(_rows[0]) - 1
        self.rows = [[0 for i in range(0, self.n_columns)] for i in range(0, self.n_rows)]
        
        for ir in range(0, self.n_rows):

            for ic in range(0, self.n_columns):
                
                if _rows[ir][ic] == "0": self.rows[ir][ic] = 0

                if _rows[ir][ic] == "1": self.rows[ir][ic] = 1

                if _rows[ir][ic] in "Pp":

                    self.rows[ir][ic] = 2
                    self.player_pos = { "c": ic, "r": ir }

                if _rows[ir][ic] in "Ee":
                    
                    self.rows[ir][ic] = 3
                    self.exit_pos = { "c": ic, "r": ir }
            
        self.validate_map()
        
        self.initial_map = self.rows.copy()
        self.initial_pos = self.player_pos.copy()
        self.very_initial_pos = self.player_pos.copy()
        self.n_moves = (self.n_rows * self.n_columns) * 2
        self.players = [Player(self.rows.copy(), self.n_rows, self.n_columns) for i in range(0, 1000000)]
        
        id = 0
        for player in self.players:
            
            player.id = id
            player.moves = self.create_random_moves(self.n_moves)
            player.player_pos = self.player_pos.copy()
            player.exit_pos = self.exit_pos.copy()
            id += 1
        
        self.found = False
        self.solve()
        
    
    def convert_map(self):

        try: self.tmp = open("/tmp/mymaze.ber", "r")
        
        except: self.map_error("temporary file deleted")

        _tmp = self.tmp.readlines()

        for ir in range(0, self.n_rows):

            for ic in range(0, self.n_columns):
                
                if _tmp[ir][ic] == "0": self.rows[ir][ic] = 0

                if _tmp[ir][ic] == "1": self.rows[ir][ic] = 1

                if _tmp[ir][ic] in "Pp":
                    
                    self.rows[ir][ic] = 2
                    self.player_pos = { "c": ic, "r": ir }
                    
                if _tmp[ir][ic] in "Ee":
                    
                    self.rows[ir][ic] = 3
                    self.exit_pos = { "c": ic, "r": ir }

        self.tmp.close()

    
    def convert_to_file(self):

        self.tmp = open("/tmp/mymaze.ber", "w+")
        
        for r in self.rows:

            for c in r:

                if c == 0: self.tmp.write("0")

                elif c == 1: self.tmp.write("1")

                elif c == 2: self.tmp.write("P")
                
                elif c == 3: self.tmp.write("E")
                
                else: self.map_error("invalid temporary file")

            self.tmp.write("\n")

        self.tmp.close()
        
        try:
            
            f = open("/tmp/mymaze.ini", "w+")
            f.write("[SAVED]\n")
            f.write(f"PLAYER_DEG={self.player_deg}\n")
            f.close()

        except: self.map_error("invalid config file")
        
    
    def map_error(self, error="invalid map"):

        """
        This function displays an error message and exits the program with the status code 1.
        """
        
        printf(f"{self.path}: {error}.\n", RED)
        exit(1)
    

    def validate_map(self):

        """
        This function checks if the map is valid, exits the program with an error in case of invalid map.
        """

        p, e = 0, 0
        
        for r in self.rows:

            for c in r:

                if c == 2: p += 1
                
                if c == 3: e += 1

        if not p == 1 or not e == 1: self.map_error()

    
    def create_random_moves(self, turns):
        
        options = [0, 1, 2, 3]

        return choices(options, k=turns)


    def solution(self, playerId):

        print(f"{playerId} found the exit.")
        
        for player in self.players:
            
            if player.id == playerId: print(player.moves)


    def show_maps(self, executed):
        
        for e in executed:
            
            for r in e:
                
                for c in r: printf(f"{c}")
                
                printf("\n")
            
        printf("\n\n\n")

    
    def calc_distance(self, x1, y1, x2, y2):

        """
        This function calculates the euclidean distance between two points.
        """

        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


    def show_results(self, results):

        root = Tk(className="MyMaze Solver")
        root.configure(bg="black")
        root.resizable(width=False, height=False)

        rootTitle = Label(root, text="MYMAZE SOLVER", bg="black", fg="#ff1100")
        rootTitle.grid(row=0, column=1)
        
        rootText = Text(root, height=20, width=50, wrap=WORD)
        rootText.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        rootText.delete(0.0, END)
        
        rootStart = Button(root, text="START", cursor="cross", command=root.destroy, bg="black", fg="#ff1100", pady=5)
        rootStart.grid(row=2, column=1)

        moves = ["UP", "RIGHT", "DOWN", "LEFT"]
        
        for r in results:
            
            rootText.insert(END, f"{moves[r]}\n")

        root.mainloop()

    
    def move_player(self, U, R, D, L):

        """
        This function moves the player in the map, changing its angle, position and animation frame.
        """

        current = self.calc_distance(self.player_pos["c"], self.exit_pos["c"], self.player_pos["r"], self.exit_pos["r"])
        
        if U == 1:

            self.player_deg = 0
            
            if self.player_pos["r"] - 1 > 0 and not self.rows[self.player_pos["r"] - 1][self.player_pos["c"]] == 1:
                
                self.rows[self.player_pos["r"]][self.player_pos["c"]], self.rows[self.player_pos["r"] - 1][self.player_pos["c"]] = 0, 2
                self.player_pos["r"] -= 1
        
        if R == 1:
            
            self.player_deg = 1
            
            if self.player_pos["c"] + 1 < self.n_columns and not self.rows[self.player_pos["r"]][self.player_pos["c"] + 1] == 1:

                self.rows[self.player_pos["r"]][self.player_pos["c"]], self.rows[self.player_pos["r"]][self.player_pos["c"] + 1] = 0, 2
                self.player_pos["c"] += 1
        
        if D == 1:

            self.player_deg = 2
            
            if self.player_pos["r"] + 1 < self.n_rows and not self.rows[self.player_pos["r"] + 1][self.player_pos["c"]] == 1:
                
                self.rows[self.player_pos["r"]][self.player_pos["c"]], self.rows[self.player_pos["r"] + 1][self.player_pos["c"]] = 0, 2
                self.player_pos["r"] += 1

        if L == 1:

            self.player_deg = 3
            
            if self.player_pos["c"] - 1 > 0 and not self.rows[self.player_pos["r"]][self.player_pos["c"] - 1] == 1:

                self.rows[self.player_pos["r"]][self.player_pos["c"]], self.rows[self.player_pos["r"]][self.player_pos["c"] - 1] = 0, 2
                self.player_pos["c"] -= 1

        self.convert_to_file()

    
    def start_solving(self, executed):

        for move in executed:

            sleep(0.5)

            if move == 0: self.move_player(1, 0, 0, 0)

            if move == 1: self.move_player(0, 1, 0, 0)

            if move == 2: self.move_player(0, 0, 1, 0)
            
            if move == 3: self.move_player(0, 0, 0, 1)

    
    def clean_map(self, is_found):

        if is_found: pos = self.very_initial_pos
        
        else: pos = self.initial_pos

        for ir in range(0, self.n_rows):

            for ic in range(0, self.n_columns):
                
                if self.initial_map[ir][ic] == 2 and not (pos["c"] == ic and pos["r"] == ir):
                    
                    self.rows[ir][ic] = 0


    def solve(self):
        
        """
        This function solves the maze provided.
        """

        best_so_far = []
        distance = self.n_moves

        for player in self.players:

            res = player.exec_moves(self.initial_pos.copy(), self.initial_map.copy(), best_so_far.copy(), distance)
            
            if res["dist"] < distance:
                
                distance = res["dist"]
                best_so_far = res["exec"].copy()
                self.initial_pos = res["pos"].copy()
                self.initial_map = res["map"].copy()
                self.clean_map(False)
            
            if player.exit_found == True:
                
                self.found = True
                
                pid = fork()
                if pid == 0: system("cd /Users/absalhi/goinfre/mymaze/game && python3 main.py")
                
                else:
                    self.clean_map(True)
                    self.show_results(res["exec"])
                    self.start_solving(res["exec"])
                    
                self.cparser = ConfigParser()
                
                break
        
        if not self.found:

            self.players = [Player(self.initial_map.copy(), self.n_rows, self.n_columns) for i in range(0, 1000000)]
        
            id = 0
            for player in self.players:
                
                player.id = id
                player.moves = self.create_random_moves(self.n_moves)
                player.player_pos = self.initial_pos.copy()
                player.exit_pos = self.exit_pos.copy()
                id += 1
            
            self.solve()
        
        exit(0)
        