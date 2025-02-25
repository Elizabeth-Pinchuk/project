import pygame as pg


class Map_manager:
    size = (16, 16)
    def __init__(self, screen_size, canvas):
        self.screen_size = screen_size
        self.canvas = canvas
    def draw_grid(self):
        for i in range(self.size[0] + 1):
            start_pos = (self.screen_size[0] / self.size[0] * i, 0)
            end_pos = (self.screen_size[0] / self.size[0] * i, self.screen_size[1])
            pg.draw.line(self.canvas, (100, 100, 255), start_pos, end_pos, width=2)
        for i in range(self.size[1] + 1):
            start_pos = (0, self.screen_size[1] / self.size[1] * i)
            end_pos = ( self.screen_size[0], self.screen_size[1] / self.size[1] * i)
            pg.draw.line(self.canvas, (100, 100, 255), start_pos, end_pos, width=2)