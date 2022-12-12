import pygame as pg
from settings import *
from sprites import *

class inventory(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load("inventory.png").convert()
        self.rect = self.image.get_rect()
        self.isLoaded = False
        self.rect.x = 250
        self.rect.y = 250
class text:
    def __init__(self, game,userText,isMiningText,player):
        self.game = game
        self.font = pg.font.Font('freesansbold.ttf', 50)
        self.healthText = self.font.render("Health = " + str(player.health), 1, (255, 255, 255))
        self.textSurface = self.font.render(str(userText), True, WHITE)
        self.textSurfaceRect = self.textSurface.get_rect()
        self.healthTextRect = self.healthText.get_rect()
        self.isMiningText = isMiningText
        self.remove = False
        self.textSurfaceRect.x = player.rect.x+10
        self.textSurfaceRect.y = player.rect.y-40

    def unload(self):
        now = pg.time.get_ticks()
        if(self.isMiningText == True and now % 100 == 0):
            self.remove = True
class scoreText:
    def __init__(self, game):
        self.font = pg.font.Font('freesansbold.ttf', 30)
        self.score = 0
        self.scoretext = self.font.render("Score = " + str(self.score), 1, (0, 0, 0))
        self.textRect = self.scoretext.get_rect()
class playerText:
    def __init__(self, game,player):
        self.game = game
        self.font = pg.font.Font('freesansbold.ttf', 30)
        self.healthText = self.font.render("Health = " + str(player.health), 1, (255, 255, 255))
        self.healthTextRect = self.healthText.get_rect()
        self.healthTextRect.y += 30
class WaveCount:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font('freesansbold.ttf', 30)
        self.wave = 0
        self.waveText = self.font.render("Wave number "+ str(self.wave), 1, (255, 255, 255))
        self.waveTextRect = self.waveText.get_rect()
        self.waveTextRect.y += 60
class crafting():
    def __init__(self, game):
        self.game = game
    def makePickaxe(self,player):
        if(player.wood >= 50):
            newPickaxe = pickAxe(self.game)
            player.pickAxes.append(newPickaxe)
            print("pickaxe created")
        else:
            print("no pickaxe created")
    def makeArrow(self,player):
        if (player.wood >= 1 and player.stone >= 1):
            player.arrows += 1
            player.wood -= 50
            player.stone -= 10
        else:
            print("failed to make arrow")




