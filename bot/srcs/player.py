# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    player.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: absalhi <absalhi@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/07 15:48:50 by absalhi           #+#    #+#              #
#    Updated: 2022/12/08 16:07:45 by absalhi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

if __name__ == "__main__":

    from utilities import printf, RED
    
    printf("Please run the game using the main.py file.\n", RED)
    exit(1)

from math import sqrt

from srcs.utilities import *


class Player:

    def __init__(self, rows, n_rows, n_columns):
        
        self.id = None
        self.moves = []
        self.fitness = 0
        self.player_pos = { "c": 0, "r": 0 }
        self.exit_pos = { "c": 0, "r": 0 }
        self.map = rows
        self.n_rows, self.n_columns = n_rows, n_columns
        self.hit_wall = False
        self.exit_found = False


    def calc_distance(self, x1, y1, x2, y2):

        """
        This function calculates the euclidean distance between two points.
        """

        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    
    def exec_moves(self, initial_pos, initial_map, best_so_far, dist):

        self.player_pos = initial_pos
        self.map = initial_map
        executed = []
        executed += best_so_far
        distance = 0

        # clear()
        # printf(f"[{self.id:06}/100000] Searching...\n", GREEN)
        
        for m in self.moves:

            # print(m)
            # print(f"id {self.id}")
            # print(self.player_pos)
            # print(self.map)

            current = self.calc_distance(self.player_pos["c"], self.exit_pos["c"], self.player_pos["r"], self.exit_pos["r"])

            if m == 0 and (self.player_pos["r"] - 1 >= 0 and self.map[self.player_pos["r"] - 1][self.player_pos["c"]] == 1): self.hit_wall = True
            if m == 1 and (self.player_pos["c"] + 1 < self.n_columns and self.map[self.player_pos["r"]][self.player_pos["c"] + 1] == 1): self.hit_wall = True
            if m == 2 and (self.player_pos["r"] + 1 < self.n_rows and self.map[self.player_pos["r"] + 1][self.player_pos["c"]] == 1): self.hit_wall = True
            if m == 3 and (self.player_pos["c"] - 1 >= 0 and self.map[self.player_pos["r"]][self.player_pos["c"] - 1] == 1): self.hit_wall == True

            if self.hit_wall:

                distance = current
                executed.append(m)
                break

            if m == 0 and (self.player_pos["r"] - 1 >= 0 and self.map[self.player_pos["r"] - 1][self.player_pos["c"]] == 3): self.exit_found = True
            if m == 1 and (self.player_pos["c"] + 1 < self.n_columns and self.map[self.player_pos["r"]][self.player_pos["c"] + 1] == 3): self.exit_found = True
            if m == 2 and (self.player_pos["r"] + 1 < self.n_rows and self.map[self.player_pos["r"] + 1][self.player_pos["c"]] == 3): self.exit_found = True
            if m == 3 and (self.player_pos["c"] - 1 >= 0 and self.map[self.player_pos["r"]][self.player_pos["c"] - 1] == 3): self.exit_found == True

            if self.exit_found:
                
                distance = -1
                executed.append(m)
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

            executed.append(m)

        return { "exec": executed, "dist": distance, "pos": self.player_pos, "map": self.map }