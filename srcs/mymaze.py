# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    mymaze.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: absalhi <absalhi@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/05 20:54:15 by absalhi           #+#    #+#              #
#    Updated: 2022/12/06 04:21:46 by absalhi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

if __name__ == "__main__":
    from utilities import printf, RED
    
    printf("Please run the game using the main.py file.\n", RED)
    exit(1)

import pygame as pg
from screeninfo import get_monitors

from srcs.utilities import *


class MyMaze:
    
    def __init__(self):

        pg.init()
        pg.display.set_caption("MyMaze v1.0")

        monitors = get_monitors()
        for i in range(0, len(monitors)):

            if monitors[i].is_primary:
                
                self.monitor = monitors[i]
                self.RESOLUTION = self.WIDTH, self.HEIGHT = (
                    monitors[i].width - 700), (monitors[i].height - 500)
                
        self.FPS = 120
        self.is_running = True
        self.is_fullscreen = False
        
        self.player = "srcs/resources/player/down_0.png"
        self.wall = [f"srcs/resources/wall/{i}.png" for i in range(0, 4)]
        self.treasure = "srcs/resources/treasure.png"
        self.ground = [f"srcs/resources/ground/{i}.png" for i in range(0, 2)]

        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        if self.is_fullscreen == False: self.screen = pg.display.set_mode(self.RESOLUTION, pg.RESIZABLE)
        else: self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.clock = pg.time.Clock()

        self.create_fonts([32, 20, 16, 8])

        try: f = open("map.ber", "r")
        except FileNotFoundError:
            printf("File not found.\n", RED)
            exit(1)
            
        _rows = f.readlines()
        self.n_rows, self.n_columns = len(_rows), len(_rows[0]) - 1
        self.rows = [[0 for i in range(0, self.n_columns)] for i in range(0, self.n_rows)]
        for ir in range(0, self.n_rows):

            for ic in range(0, self.n_columns):
                
                if _rows[ir][ic] == "0": self.rows[ir][ic] = 0
                if _rows[ir][ic] == "1": self.rows[ir][ic] = 1
                if _rows[ir][ic] in "Pp": self.rows[ir][ic] = 2
                if _rows[ir][ic] in "Ee": self.rows[ir][ic] = 3
        
        self.player_pos = { "c": 1, "r": 1 }
        self.player_deg = 2
        self.frame = 0

        self.run()


    def create_fonts(self, font_sizes):
        
        self.fonts = []
        
        for size in font_sizes:
            
            try: self.fonts.append(pg.font.Font("srcs/resources/IBMPlexMono-Regular.ttf", size))
            except: self.fonts.append(pg.font.SysFont("Arial", size))


    def draw_cell(self, path, w, h, ic, ir, t=None):
        
        _w, _h = w, h
        if t == 3: _w, _h = _w - (_w * 25 / 100), _h - (_h * 25 / 100)
        if t == 2: _w, _h = _w - (_w * 25 / 100), _h + (_h * 15 / 100)
        cell = pg.image.load(path)
        cell = pg.transform.scale(cell, (_w, _h))
        cell.convert()
        
        __w, __h = ic * w, ir * h
        if t == 3: __w, __h = __w + (w * 12 / 100), __h + (h * 12 / 100)
        if t == 2: __w, __h = __w + (w * 12 / 100), __h - (h * 35 / 100)
        self.screen.blit(cell, (__w, __h))


    def get_map(self):

        width_px, height_px = int(self.WIDTH / self.n_columns), int(self.HEIGHT / self.n_rows)

        ir = 0
        for r in self.rows:
            
            ic = 0
            for c in r:
                
                if c == 1:

                    self.draw_cell(self.wall[0], width_px, height_px, ic, ir) if ir + 1 < self.n_rows and self.rows[ir + 1][ic] == 1 else self.draw_cell(self.wall[2], width_px, height_px, ic, ir)
                    
                elif c in [0, 2, 3]:
                    
                    self.draw_cell(self.ground[1], width_px, height_px, ic, ir)

                if c == 2:

                    self.draw_cell(self.player, width_px, height_px, ic, ir, c)
                    self.player_pos["c"] = ic
                    self.player_pos["r"] = ir
                    
                if c == 3:

                    self.draw_cell(self.treasure, width_px, height_px, ic, ir, c)
                    
                ic += 1
            ir += 1


    def render(self, font, text, color, pos):

        text_to_show = font.render(text, 0, pg.Color(color))
        self.screen.blit(text_to_show, pos)


    def draw(self):
        
        self.screen.fill("#000000")
        self.get_map()
        self.animate_sprites()
        self.render(self.fonts[0], text=f"{int(self.clock.get_fps())} FPS",
            color="red", pos=(25, 10))

    
    def move_player(self, U, R, D, L):
        
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


    def animate_sprites(self):
        
        if self.player_deg == 0: self.player = f"srcs/resources/player/up_{self.frame}.png"
        if self.player_deg == 1: self.player = f"srcs/resources/player/right_{self.frame}.png"
        if self.player_deg == 2: self.player = f"srcs/resources/player/down_{self.frame}.png"
        if self.player_deg == 3: self.player = f"srcs/resources/player/left_{self.frame}.png"
        
        self.frame += 1
        if self.frame > 16: self.frame = 0

    
    def run(self):
        
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
                    
                    if e.key in [pg.K_s, pg.K_DOWN]: self.move_player(0, 0, 1, 0)
                    
                    elif e.key in [pg.K_w, pg.K_UP]: self.move_player(1, 0, 0, 0)
                        
                    elif e.key in [pg.K_a, pg.K_LEFT]: self.move_player(0, 0, 0, 1)
                        
                    elif e.key in [pg.K_d, pg.K_RIGHT]: self.move_player(0, 1, 0, 0)
                        

            self.clock.tick(self.FPS)

            pg.display.flip()