# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    player.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: absalhi <absalhi@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/07 15:48:50 by absalhi           #+#    #+#              #
#    Updated: 2022/12/07 17:44:27 by absalhi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

if __name__ == "__main__":

    from utilities import printf, RED
    
    printf("Please run the game using the main.py file.\n", RED)
    exit(1)

from srcs.utilities import *


class Player:

    def __init__(self, initial_pos, rows, n_rows, n_columns):
        
        self.id = None
        self.moves = []
        self.fitness = 0
        self.player_pos = initial_pos
        self.map = rows
        self.n_rows, self.n_columns = n_rows, n_columns
        self.hit_wall = False
        self.exit_found = False

    
    def show_map(self):

        for r in self.map:
            
            for c in r: printf(f"{c}")
            printf("\n")
            
        printf("\n")

    
    def exec_moves(self):

        executed = []

        for m in self.moves:

            if m == 0 and (self.player_pos["r"] - 1 >= 0 and self.map[self.player_pos["r"] - 1][self.player_pos["c"]] == 1): self.hit_wall = True
            if m == 1 and (self.player_pos["c"] + 1 < self.n_columns and self.map[self.player_pos["r"]][self.player_pos["c"] + 1] == 1): self.hit_wall = True
            if m == 2 and (self.player_pos["r"] + 1 < self.n_rows and self.map[self.player_pos["r"] + 1][self.player_pos["c"]] == 1): self.hit_wall = True
            if m == 3 and (self.player_pos["c"] - 1 >= 0 and self.map[self.player_pos["r"]][self.player_pos["c"] - 1] == 1): self.hit_wall == True

            if self.hit_wall:
                
                executed.append(self.map)
                break

            if m == 0 and (self.player_pos["r"] - 1 >= 0 and self.map[self.player_pos["r"] - 1][self.player_pos["c"]] == 3): self.exit_found = True
            if m == 1 and (self.player_pos["c"] + 1 < self.n_columns and self.map[self.player_pos["r"]][self.player_pos["c"] + 1] == 3): self.exit_found = True
            if m == 2 and (self.player_pos["r"] + 1 < self.n_rows and self.map[self.player_pos["r"] + 1][self.player_pos["c"]] == 3): self.exit_found = True
            if m == 3 and (self.player_pos["c"] - 1 >= 0 and self.map[self.player_pos["r"]][self.player_pos["c"] - 1] == 3): self.exit_found == True

            if self.exit_found:
                
                executed.append(self.map)
                break

            if m == 0 and (self.player_pos["r"] - 1 >= 0 and not self.map[self.player_pos["r"] - 1][self.player_pos["c"]] == 1):
                self.map[self.player_pos["r"]][self.player_pos["c"]], self.map[self.player_pos["r"] - 1][self.player_pos["c"]] = 0, 2
                self.player_pos["r"] -= 1
            if m == 1 and (self.player_pos["c"] + 1 < self.n_columns and not self.map[self.player_pos["r"]][self.player_pos["c"] + 1] == 1):
                self.map[self.player_pos["r"]][self.player_pos["c"]], self.map[self.player_pos["r"]][self.player_pos["c"] + 1] = 0, 2
                self.player_pos["c"] += 1
            if m == 2 and (self.player_pos["r"] + 1 < self.n_rows and not self.map[self.player_pos["r"] + 1][self.player_pos["c"]] == 1):
                self.map[self.player_pos["r"]][self.player_pos["c"]], self.map[self.player_pos["r"] + 1][self.player_pos["c"]] = 0, 2
                self.player_pos["r"] += 1
            if m == 3 and (self.player_pos["c"] - 1 >= 0 and not self.map[self.player_pos["r"]][self.player_pos["c"] - 1] == 1):
                self.map[self.player_pos["r"]][self.player_pos["c"]], self.map[self.player_pos["r"]][self.player_pos["c"] - 1] = 0, 2
                self.player_pos["c"] -= 1

            executed.append(self.map)

        return executed