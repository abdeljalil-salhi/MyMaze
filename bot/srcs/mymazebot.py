# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    mymazebot.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: absalhi <absalhi@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/07 15:01:47 by absalhi           #+#    #+#              #
#    Updated: 2022/12/07 17:44:10 by absalhi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

if __name__ == "__main__":

    from utilities import printf, RED
    
    printf("Please run the game using the main.py file.\n", RED)
    exit(1)

from random import choices
from math import sqrt

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
                if _rows[ir][ic] in "Ee": self.rows[ir][ic] = 3

        self.validate_map()
        
        self.turn = 1
        self.n_moves = (self.n_rows * self.n_columns) * 2
        self.players = [Player(self.player_pos, self.rows, self.n_rows, self.n_columns) for i in range(0, 1000)]
        
        id = 0
        for player in self.players:
           player.id = id
           player.moves = self.create_random_moves(self.n_moves)
           id += 1
        
        self.solve()
        
    
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

        p = 0
        e = 0

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

    
    def solve(self):
        
        """
        This function solves the maze provided.
        """

        for player in self.players:

            executed = player.exec_moves()
            
            if player.exit_found == True:
                
                print(f"{player.id} found the exit.")
                self.show_maps(executed)
                break
                