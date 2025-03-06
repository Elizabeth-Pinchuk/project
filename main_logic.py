import sys

import pygame as pg
from classes import *
from all_in_all import *
SCREEN_SIZE = (512, 512)
pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
map = Map((100, 50, 250), 0, SCREEN_SIZE, (16, 16))
map_manager = Map_manager(SCREEN_SIZE, screen, map)

def exit_game():
    pg.quit()
    sys.exit()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit_game()
    map_manager.fill()
    # map_manager.debug()
    map_manager.show_map()
    pg.display.flip()