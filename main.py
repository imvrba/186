#Group 1's city builder main program.
#Last updated 03/09/21
#Members Names: Isaac Vrba, Cameron Jones, Dan.
#Camera movement and grid loading/Movement from https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2004

import pygame as pg #changes pygame to pg so we don't have to type 'pygames' out each time
import sys
from os import path
from settings import *
from sprites import *
import random
from Inventory import *
from Map import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #creates the size of the screen
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.bearList = []
        self.bears = pg.sprite.Group()
        self.isCrafting = False
        self.inventoryRunning = False
        self.GameOver = False
        self.optionChosen = 0
        self.ChosenMenu = 0
        self.bearCount = 1
        self.scoreText = scoreText(pg)
        self.WaveText = WaveCount(self)
        pg.key.set_repeat(500, 100)
        self.load_data()
        #self.usedInventory = inventory(pg)
        self.texts = []
        # Load and play background music
        # Sound source: http://ccmixter.org/files/Apoxode/59262
        # License: https://creativecommons.org/licenses/by/3.0/
        #pg.mixer.music.load("Apoxode_-_Electric 1.mp3")
        #pg.mixer.music.play(loops=-1)


    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map2.txt'))
        self.map_data = []
        with open(path.join(game_folder, 'map2.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
    def gameOver(self):
        print("GAME OVER!!!")
        self.screen.fill((0,0,0))
        self.font = pg.font.Font('freesansbold.ttf', 75)
        self.GameOverText = self.font.render("GAME OVER", 1, (255, 255, 255))
        self.GameOverTextRect = self.GameOverText.get_rect()
        self.screen.blit(self.GameOverText, self.GameOverTextRect)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()



    def itemSpawner(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        #item_list is a list of possible items to add to the map
        item_list = ['R', 'S', 'F', 'G', 'W']
        #item_qty is a list containing the quantities of each item
        item_qty = [0, 0, 0, 0, 0]
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '.':
                    randNum = random.randint(0,200)
                    if randNum == 1:
                        if item_qty[1] < 10:
                            Stone(self, col, row)
                            item_qty[1] = item_qty[1] + 1
                    elif randNum == 2:
                        if item_qty[2] < 5:
                            Food(self, col, row)
                            item_qty[2] = item_qty[2] + 1
                    elif randNum == 3:
                        if item_qty[3] < 5:
                            Gold(self, col, row)
                            item_qty[3] = item_qty[3] + 1
                    elif randNum == 4:
                        if item_qty[4] < 15:
                            Wood(self, col, row)
                            item_qty[4] = item_qty[4] + 1
                    #elif randNum == 0:
                        #if item_qty[0] < 3:
                            #self.rabbit = rabbit(self, col, row)
                            #item_qty[0] = item_qty[0] + 1
                elif tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                    self.playerText = playerText(pg, self.player)
                    self.camera = Camera(self.map.width, self.map.height)
                elif tile == "R":
                    self.Rabbit = rabbit(self,col,row)


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.rabbits = pg.sprite.Group()
        self.stone = pg.sprite.Group()
        self.food = pg.sprite.Group()
        self.wood = pg.sprite.Group()
        self.gold = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1': #loads a traditional, non-passable wall
                    Wall(self, col, row)
                if tile == 'P': #loads the player in the tile with a 'P'
                    self.player = Player(self,col, row)
                    self.playerText = playerText(pg, self.player)
                if tile == '2': #loads spaces with 2 with a passable wall
                    PassableWall(self, col, row)
                if tile == 'S': #loads stone
                    Stone(self, col, row)
                if tile == 'F': #loads food
                    Food(self, col, row)
                if tile == 'G': #loads in gold
                    Gold(self, col, row)
                if tile == "W": #loads in wood
                    Wood(self, col, row)
    def spawn(self):
        now = pg.time.get_ticks()
        count = range(self.bearCount)
        initx = 61           #init bear spawn location
        inity = 20
        if (now % 900 == 0):
            self.WaveText.wave += 1
            self.WaveText.waveText = self.WaveText.font.render("Wave number " + str(self.WaveText.wave), 1,
                                                               (255, 255, 255))
            for New_bear in count:
                self.Bear = bear(self, initx,inity)
                self.bearList.append(self.Bear)
                initx += 1         #new bear spawn location based off current bears
                inity -= 1
            self.bearCount += 1

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    #defining what happens when the program is closed/quits
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        for text in self.texts:
            text.textSurfaceRect.x = 250
            text.textSurfaceRect.y = 15
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def inventory(self):
        self.inventoryRunning = True
        self.isCrafting = False
        black = (0, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        while self.inventoryRunning:
            X = 1024
            Y = 768
            display_surface = pg.display.set_mode((X, Y))
            pg.display.set_caption('Inventory')
            font = pg.font.Font('freesansbold.ttf', 32)
            text = font.render("Stone: " + str(self.player.stone), True, green, blue)
            text2 = font.render("Food: " + str(self.player.food), True, green, blue)
            text3 = font.render("Gold: " + str(self.player.gold), True, green, blue)
            textRect = text.get_rect()
            text2Rect = text2.get_rect()
            text3Rect = text3.get_rect()
            textRect.center = (X // 2, Y // 2)
            text2Rect.center = (X // 2, Y // 2 - 30)
            text3Rect.center = (X // 2, Y // 2 - 60)
            display_surface.fill(black)
            display_surface.blit(text, textRect)
            display_surface.blit(text2, text2Rect)
            display_surface.blit(text3, text3Rect)
            font = pg.font.Font
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_TAB:
                        self.inventoryRunning = False
                    if event.key == pg.K_RIGHT and self.inventoryRunning == True:
                        display_surface.fill(black)
                        self.isCrafting = True
                        self.crafting()
                        print("true")
                    if event.key == pg.K_ESCAPE:
                        self.quit()


            pg.display.update()
    def crafting(self):
        black = (0, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 128)

        while self.isCrafting:
            X = 1024
            Y = 768
            display_surface = pg.display.set_mode((X, Y))
            pg.display.set_caption('Inventory')
            font = pg.font.Font('freesansbold.ttf', 32)
            craftText = font.render("Create Pickaxe: ", True, green, blue)
            craftText1 = font.render("Make Arrow: ", True, green, blue)
            arrow = font.render("--->", True, green, blue)
            craftTextRect = craftText.get_rect()
            craftText1Rect = craftText1.get_rect()
            arrowRect = arrow.get_rect()
            craftTextRect.center = (X // 2, Y // 2)
            craftText1Rect.center = (X // 2, Y // 2 + 35)
            #arrowRect.center = (X // 2 - 200,Y // 2-35)
            if (self.optionChosen == 0):
                print("location")
                arrowRect.center = (X // 2 - 200, Y // 2)
            else:
                arrowRect.center = (X // 2-200, Y // 2 + (35 * self.optionChosen))
            display_surface.fill(black)
            display_surface.blit(craftText, craftTextRect)
            display_surface.blit(craftText1, craftText1Rect)
            display_surface.blit(arrow,arrowRect)

            font = pg.font.Font
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.type == pg.QUIT:
                        self.quit()
                    if event.key == pg.K_TAB:
                        self.inventoryRunning = False
                        self.isCrafting = False
                    if event.key == pg.K_DOWN and self.isCrafting == True:
                        if(self.optionChosen < 1):#if additional crafting options are added increase
                            self.optionChosen += 1
                    if event.key == pg.K_UP and self.isCrafting == True:
                        if(self.optionChosen > 0):
                            self.optionChosen -= 1
                    if event.key == pg.K_LEFT and self.isCrafting == True:
                        self.isCrafting = False
                    if (event.key == pg.K_0):
                        if self.optionChosen == 1:
                            crafting.makeArrow(self,self.player)
                            print(self.player.arrows)
                    if event.key == pg.K_ESCAPE:
                        self.quit()
            pg.display.update()


    def draw(self):
        if (self.GameOver == False):
            self.screen.blit(BACKGROUND,(0,0))
            self.draw_grid()
            #self.all_sprites.draw(self.screen)
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            #if self.usedInventory.isLoaded == True:
                #self.screen.blit(self.usedInventory.image,self.usedInventory.rect)
            pg.draw.rect(self.screen, (0, 0, 0), pg.Rect(250, 0, 500, 60))
            for text in self.texts:
                self.screen.blit(text.textSurface,text.textSurfaceRect)
            self.screen.blit(self.scoreText.scoretext,self.scoreText.textRect)
            self.screen.blit(self.playerText.healthText, self.playerText.healthTextRect)
            self.screen.blit(self.WaveText.waveText, self.WaveText.waveTextRect)
            pg.display.flip()
        else:
            self.gameOver()

    def events(self):
        if(self.GameOver == False):
            # catch all events here
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if event.key == pg.K_LEFT and self.player.isShooting == False:
                        self.player.move(dx=-1)
                    if event.key == pg.K_RIGHT and self.player.isShooting == False:
                        self.player.move(dx=1)
                    if event.key == pg.K_UP and self.player.isShooting == False:
                        self.player.move(dy=-1)
                    if event.key == pg.K_DOWN and self.player.isShooting == False:
                        self.player.move(dy=1)
                    if event.key == pg.K_SPACE:
                        self.player.placeWall()
                    if event.key == pg.K_f and self.player.isShooting == False:
                        self.player.isShooting = True
                    elif event.key == pg.K_f and self.player.isShooting == True:
                        self.player.isShooting = False
                    if event.key == pg.K_UP and self.player.isShooting == True:
                        self.player.shoot(0, -1)
                        self.player.isShooting = False
                    if event.key == pg.K_DOWN and self.player.isShooting == True:
                        self.player.shoot(0, 1)
                        self.player.isShooting = False
                    if event.key == pg.K_RIGHT and self.player.isShooting == True:
                        self.player.shoot(1, 0)
                        self.player.isShooting = False
                    if event.key == pg.K_LEFT and self.player.isShooting == True:
                        self.player.shoot(-1, 0)
                        self.player.isShooting = False
                    if event.key == pg.K_0:
                        self.player.collect()



                    #if event.key == pg.K_i and self.usedInventory.isLoaded == False:
                        #self.usedInventory.isLoaded = True
                    #elif event.key == pg.K_i and self.usedInventory.isLoaded == True:
                        #self.usedInventory.isLoaded = False
                    if event.key == pg.K_TAB:
                        self.inventory()


            Movex = random.randint(-1,1)
            Movey = random.randint(-1,1)
            self.spawn()

            self.Rabbit.move(dx=Movex, px=self.player.x, py=self.player.y)
            self.Rabbit.move(dy=Movey, px=self.player.x, py=self.player.y)
            moveHorizOrVert = random.randint(0, 1)
            for bear in self.bears:
                if(bear.isDead == True):
                    bear.isDeadFunction()
                    self.scoreText.score = self.player.kills * 10
                    self.scoreText.scoretext = self.scoreText.font.render("Score = " + str(self.scoreText.score), 1,
                                                                          (255, 255, 255))
                if(moveHorizOrVert == 1):
                    Movex = random.randint(-1, 1)
                    bear.move(dx=Movex, px=self.player.x, py=self.player.y)
                else:
                    Movey = random.randint(-1, 1)
                    bear.move(dy=Movey, px=self.player.x, py=self.player.y)

            for bullet in self.bullets:
                bullet.move()
            for text in self.texts:
                text.unload()
                if(text.remove == True):
                    self.texts.remove(text)
            if(self.player.health <= 0):
                self.GameOver = True
            self.playerText.healthText = self.playerText.font.render("Health = " + str(self.player.health), 1, (255, 255, 255))
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.itemSpawner()
    g.run()
    g.show_go_screen()
        
