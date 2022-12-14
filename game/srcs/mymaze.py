# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    mymaze.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: absalhi <absalhi@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/05 20:54:15 by absalhi           #+#    #+#              #
#    Updated: 2022/12/08 17:10:16 by absalhi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

if __name__ == "__main__":
    
    from utilities import printf, RED
    
    printf("Please run the game using the main.py file.\n", RED)
    exit(1)

import pygame as pg
from screeninfo import get_monitors
from configparser import ConfigParser

from srcs.utilities import *


class MyMaze:

    def __init__(self):

        """
        This class contains the whole game of MyMaze.
            - Initialize the game screen
            - Initialize all the variables to be used across the class
            - Set the display mode depending on the primary screen measures
            - Get the map from the file and parse it
        """
        
        RELATIVE_RESOLUTION = False

        pg.init()
        pg.display.set_caption("MyMaze")  
             
        self.FPS = 120
        self.is_running = True
        self.is_fullscreen = False
        
        self.player = "srcs/resources/player/down_0.png"
        self.shadow = "srcs/resources/shadow.png"
        self.wall = [f"srcs/resources/wall/{i}.png" for i in range(0, 4)]
        self.treasure = "srcs/resources/treasure.png"
        self.ground = [f"srcs/resources/ground/{i}.png" for i in range(0, 2)]

        self.create_fonts([32, 20, 16, 8])

        try: f = open("map.ber", "r")
        
        except FileNotFoundError: self.map_error("file not found")
        
        self.tmp = open("/tmp/mymaze.ber", "w+")
        for l in f: self.tmp.write(l)
        self.tmp.close()
        f.seek(0)
        
        self.cparser = ConfigParser()
        self.player_deg = 2
        try:
            
            _f = open("/tmp/mymaze.ini", "w+")
            _f.write("[SAVED]\n")
            _f.write(f"PLAYER_DEG={self.player_deg}\n")
            _f.close()

        except: self.map_error("invalid config file")

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

        if RELATIVE_RESOLUTION:
            
            monitors = get_monitors()
            for i in range(0, len(monitors)):

                if monitors[i].is_primary:
                    
                    self.monitor = monitors[i]
                    self.RESOLUTION = self.WIDTH, self.HEIGHT = (
                        monitors[i].width - 700), (monitors[i].height - 500)
        
        else: self.RESOLUTION = self.WIDTH, self.HEIGHT = (self.n_columns * 64), (self.n_rows * 64)
        
        if self.is_fullscreen == False: self.screen = pg.display.set_mode(self.RESOLUTION, pg.RESIZABLE)
            
        else: self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

        self.frame = 0
        self.validate_map()
        self.clock = pg.time.Clock()

        self.run()

    
    def convert_map(self):

        try: self.tmp = open("/tmp/mymaze.ber", "r")
        except: self.map_error("temporary file deleted")

        try: self.cparser.read("/tmp/mymaze.ini")
        except: self.map_error("config file deleted")

        _tmp = self.tmp.readlines()

        for ir in range(0, self.n_rows):

            for ic in range(0, self.n_columns):
                
                if _tmp[ir][ic] == "0": self.rows[ir][ic] = 0
                if _tmp[ir][ic] == "1": self.rows[ir][ic] = 1
                if _tmp[ir][ic] in "Pp":
                    self.rows[ir][ic] = 2
                    self.player_pos = { "c": ic, "r": ir }
                if _tmp[ir][ic] in "Ee": self.rows[ir][ic] = 3

        self.tmp.close()
        self.player_deg = int(self.cparser["SAVED"]["PLAYER_DEG"])

    
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
        
        printf(f"map.ber: {error}.\n", RED)
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


    def create_fonts(self, font_sizes):

        """
        This function creates the font to be used by the game;
            - either provide it in the resources folder
            - or the default one will be used (Arial)
        """
        
        self.fonts = []
        
        for size in font_sizes:
            
            try: self.fonts.append(pg.font.Font("srcs/resources/IBMPlexMono-Regular.ttf", size))
            except: self.fonts.append(pg.font.SysFont("Arial", size))


    def draw_cell(self, path, w, h, ic, ir, t=None):

        """
        This function draws every cell in the provided map to the game by updating it accordingly.
        """
        
        _w, _h = w, h
        
        if (t == 1 and not ir == 0) and ((ir + 1 < self.n_rows) and self.rows[ir + 1][ic] in [0, 2, 3]) or (ir + 1 == self.n_rows): _h += 28
        
        if t == 1 and ir == 0 and (ic == 0 or ic == self.n_columns - 1): _h -= 28
        
        if t == 2: _w, _h = _w - (_w * 25 / 100), _h + (_h * 15 / 100)
        
        if t == 3: _w, _h = _w - (_w * 25 / 100), _h - (_h * 25 / 100)
        
        if t == 4: _w, _h = _w - (w * 40 / 100), _h - (h * 40 / 100)
        
        if t == 5: _w, _h = _w + (w * 25 / 100), _h
        
        cell = pg.image.load(path)
        cell = pg.transform.scale(cell, (_w, _h))
        cell.convert()
        
        __w, __h = ic * w, ir * h
        
        if t == 1 and not ir == 0: __h -= 28
        
        if t == 2: __w, __h = __w + (w * 12 / 100), __h - (h * 35 / 100)
        
        if t == 3: __w, __h = __w + (w * 12 / 100), __h - (h * 12 / 100)
        
        if t == 4: __w, __h = __w + (w * 19 / 100), __h + (h * 38 / 100)
        
        if t == 5: __w, __h = __w - (w * 10 / 100), __h + (h * 12 / 100)
        
        self.screen.blit(cell, (__w, __h))


    def get_map(self):

        """
        This function goes through the map cell by cell, calling the draw_cell() for each element.
        """

        width_px, height_px = int(self.WIDTH / self.n_columns), int(self.HEIGHT / self.n_rows)

        ir = 0
        for r in self.rows:
            
            ic = 0
            for c in r:
                
                if c == 1:

                    self.draw_cell(self.wall[0], width_px, height_px, ic, ir, c) if ir + 1 < self.n_rows and self.rows[ir + 1][ic] == 1 else self.draw_cell(self.wall[2], width_px, height_px, ic, ir, c)
                    
                elif c in [0, 2, 3]:
                    
                    self.draw_cell(self.ground[1], width_px, height_px, ic, ir)

                if c == 2:

                    self.draw_cell(self.shadow, width_px, height_px, ic, ir, 4)
                    self.draw_cell(self.player, width_px, height_px, ic, ir, c)
                    self.player_pos["c"] = ic
                    self.player_pos["r"] = ir
                    
                if c == 3:

                    self.draw_cell(self.shadow, width_px, height_px, ic, ir, 5)
                    self.draw_cell(self.treasure, width_px, height_px, ic, ir, c)
                    
                ic += 1
            ir += 1


    def draw(self):

        """
        This function draws the game components, change animations frames and display the FPS.
        """
        
        self.screen.fill("#000000")
        self.convert_map()
        self.get_map()
        self.animate_sprites()
        self.screen.blit(self.fonts[1].render(f"{int(self.clock.get_fps())} FPS", 0, pg.Color("red")), (25, 10))

    
    def move_player(self, U, R, D, L):

        """
        This function moves the player in the map, changing its angle, position and animation frame.
        """
        
        if U == 1:

            self.player_deg = 0
            self.animate_sprites()

            if self.player_pos["r"] - 1 > 0 and not self.rows[self.player_pos["r"] - 1][self.player_pos["c"]] == 1:
                
                self.rows[self.player_pos["r"]][self.player_pos["c"]], self.rows[self.player_pos["r"] - 1][self.player_pos["c"]] = 0, 2
                self.player_pos["r"] -= 1
        
        if R == 1:
            
            self.player_deg = 1
            self.animate_sprites()

            if self.player_pos["c"] + 1 < self.n_columns and not self.rows[self.player_pos["r"]][self.player_pos["c"] + 1] == 1:

                self.rows[self.player_pos["r"]][self.player_pos["c"]], self.rows[self.player_pos["r"]][self.player_pos["c"] + 1] = 0, 2
                self.player_pos["c"] += 1
        
        if D == 1:

            self.player_deg = 2
            self.animate_sprites()

            if self.player_pos["r"] + 1 < self.n_rows and not self.rows[self.player_pos["r"] + 1][self.player_pos["c"]] == 1:
                
                self.rows[self.player_pos["r"]][self.player_pos["c"]], self.rows[self.player_pos["r"] + 1][self.player_pos["c"]] = 0, 2
                self.player_pos["r"] += 1

        if L == 1:

            self.player_deg = 3
            self.animate_sprites()

            if self.player_pos["c"] - 1 > 0 and not self.rows[self.player_pos["r"]][self.player_pos["c"] - 1] == 1:

                self.rows[self.player_pos["r"]][self.player_pos["c"]], self.rows[self.player_pos["r"]][self.player_pos["c"] - 1] = 0, 2
                self.player_pos["c"] -= 1

        self.convert_to_file()


    def animate_sprites(self):

        """
        This function changes the animation frame of the player depending on its angle.
        """
        
        if self.player_deg == 0: self.player = f"srcs/resources/player/up_{self.frame}.png"

        if self.player_deg == 1: self.player = f"srcs/resources/player/right_{self.frame}.png"

        if self.player_deg == 2: self.player = f"srcs/resources/player/down_{self.frame}.png"
        
        if self.player_deg == 3: self.player = f"srcs/resources/player/left_{self.frame}.png"
        
        self.frame += 1
        if self.frame > 16: self.frame = 0

    
    def run(self):

        """
        This function is the game loop, running repeatedly until an exiting event is set off.
        """
        
        while self.is_running:
            
            self.draw()

            for e in pg.event.get():

                if e.type == pg.QUIT:

                    self.is_running = False
                    exit(0)

                if e.type == pg.KEYUP:

                    if e.key == pg.K_ESCAPE:

                        self.is_running = False
                        exit(0)
                    
                    if e.key in [pg.K_w, pg.K_UP]: self.move_player(1, 0, 0, 0)

                    if e.key in [pg.K_d, pg.K_RIGHT]: self.move_player(0, 1, 0, 0)

                    if e.key in [pg.K_s, pg.K_DOWN]: self.move_player(0, 0, 1, 0)
                    
                    if e.key in [pg.K_a, pg.K_LEFT]: self.move_player(0, 0, 0, 1)
                        

            self.clock.tick(30 if self.FPS > 30 else self.FPS)

            pg.display.flip()