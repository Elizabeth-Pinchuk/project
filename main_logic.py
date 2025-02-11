import sys

import pygame as pg
from classes import*
SCREEN_SIZE = (500, 300)
pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
def exit_game():
        pg.quit()
        sys.exit()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit_game()
