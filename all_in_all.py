import pygame as pg


class Map_manager:
    size = (16, 16)

    def __init__(self, screen_size, canvas, map):
        self.screen_size = screen_size
        self.canvas = canvas
        self.cell_size = self.screen_size[0] / self.size[0]
        self.map_object = map

    def debug(self):
        self.draw_grid()

    def draw_grid(self):
        for i in range(self.size[0] + 1):
            start_pos = self.get_cords(i, 0)
            end_pos = self.get_cords(i, self.size[1])
            pg.draw.line(self.canvas, (100, 100, 255), start_pos, end_pos, width=1)
        for i in range(self.size[1] + 1):
            start_pos = self.get_cords(0, i)
            end_pos = self.get_cords(self.size[0], i)
            pg.draw.line(self.canvas, (100, 100, 255), start_pos, end_pos, width=1)

    def show_map(self):
        k = 10
        colors = {'floor': (100, 50, 250),
                  'rock': (0, 0, 0),
                  'spaceship part': (50, 250, 50),
                  'alien': (250, 50, 50),
                  'base': (255, 255, 255), }
        for y in range(len(self.map_object.blocks)):
            for x in range(len(self.map_object.blocks[y])):
                pg.draw.circle(self.canvas,
                               colors[self.map_object.mini_map[y][x]],
                               (x * k, y * k),
                               5)

    def fill(self):
        self.canvas.fill(self.map_object.color)

    def get_cords(self, x, y):
        return self.cell_size * x, self.cell_size * y

    def get_cell(self, x, y):
        return x / self.cell_size, y / self.cell_size

    def set_objects_pos(self):
        for y in range(len(self.map_object.blocks)):
            for x in range(len(self.map_object.blocks[y])):
                self.map_object.blocks[y][x].pos[0] *= self.cell_size
                self.map_object.blocks[y][x].pos[1] *= self.cell_size