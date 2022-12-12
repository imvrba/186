import pygame as pg

# define commonly used colors for easy reference (R,G,B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SKYBLUE = (135, 206, 235)


# game settings
WIDTH = 1024   #a large enough number that occupies the screen and also divisible by 32 so we have full tiles
HEIGHT = 768  #same logic as the width, but for height
FPS = 144
TITLE = "CprE 186 Game"
BACKGROUND = pg.image.load("background.jpg")

TILESIZE = 32  #size of the tile that we chose
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE