import pygame as pg
import random
from settings import *
from Inventory import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        self.group1 = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load("head.png").convert_alpha()  # loads in the stone.png file
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.isShooting = False
        self.wood = 0
        self.food = 0
        self.gold = 0
        self.wheat = 0
        self.kills = 0
        self.arrow_sound = pg.mixer.Sound("arrow_launch_sound.wav")
        self.health = 1
        self.arrows = 1
        self.stone = 0
        self.pickAxes = [pickAxe(game)]
        self.sythes = [sythe(game)]
        self.axes = [axe(game)]
        self.axe = 1
        self.pickAxe = 1

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    # Coppied from collide with wall. Will eventually be a door. Probably needs to be edited.
    def collide_with_passableWalls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
    def collect(self):
        for rabbit in self.game.rabbits:
            if rabbit.x == self.x + 1 and rabbit.y == self.y or (rabbit.x == self.x - 1 and rabbit.y == self.y) or (rabbit.y == self.y + 1 and rabbit.x == self.x)or(rabbit.y == self.y - 1 and rabbit.x == self.x):
                rabbit.kill()
        for stone in self.game.stone:
            if stone.x == self.x +1 and stone.y == self.y or (stone.x == self.x -1 and stone.y == self.y) or (stone.y == self.y+1 and stone.x == self.x) or (stone.y == self.y-1 and stone.x == self.x):
                if(len(self.pickAxes) != 0):
                    stoneChange = random.randint(1,5)
                    self.stone += stoneChange
                    stone.stone -= stoneChange
                    self.pickAxes[0].swing()
                    stone.mining()
                    newText = text(self.game,(str)(stoneChange) +": Stone added",True,self)
                    for text1 in self.game.texts:
                        self.game.texts.remove(text1)
                    self.game.texts.append(newText)
                    if(self.pickAxes[0].isBroken == True):
                        self.pickAxes.pop(0)
        for wheat in self.game.food:
            if wheat.x == self.x +1 and wheat.y == self.y or (wheat.x == self.x -1 and wheat.y == self.y) or (wheat.y == self.y+1 and wheat.x == self.x) or (wheat.y == self.y-1 and wheat.x == self.x):
                if(len(self.sythes) != 0):
                    wheatChange = random.randint(1,5)
                    self.food += wheatChange
                    wheat.food -= wheatChange
                    self.sythes[0].swing()
                    wheat.collecting()
                    newText = text(self.game,(str)(wheatChange)+": Food Added",True,self)
                    for text1 in self.game.texts:
                        self.game.texts.remove(text1)
                    self.game.texts.append(newText)
                    if(self.sythes[0].isBroken == True):
                        self.pickAxes.pop(0)
        for wood in self.game.wood:
            if wood.x == self.x + 1 and wood.y == self.y or (wood.x == self.x -1 and wood.y == self.y) or (wood.y == self.y + 1 and wood.x == self.x) or (wood.y == self.y - 1 and wood.x == self.x):
                if(len(self.axes) != 0):
                    woodChange = random.randint(1,5)
                    self.wood += woodChange
                    wood.wood -= woodChange
                    self.axes[0].swing()
                    wood.collecting()
                    newText = text(self.game,(str)(woodChange)+": Wood Added",True,self)
                    for text1 in self.game.texts:
                        self.game.texts.remove(text1)
                    self.game.texts.append(newText)
                    if(self.axes[0].isBroken == True):
                        self.pickAxes.pop(0)
        for gold in self.game.gold:
           if gold.x == self.x +1 and gold.y == self.y or (gold.x == self.x -1 and gold.y == self.y) or (gold.y == self.y+1 and gold.x == self.x) or (gold.y == self.y-1 and gold.x == self.x):
                if(len(self.pickAxes) != 0):
                    gold.goldChange = random.randint(1,5)
                    self.gold += gold.goldChange
                    gold.gold -= gold.goldChange
                    self.pickAxes[0].swing()
                    gold.mining()
                    newText = text(self.game,(str)(gold.goldChange)+": Gold Added",True,self)
                    for text1 in self.game.texts:
                        self.game.texts.remove(text1)
                    self.game.texts.append(newText)
                    if(self.pickAxes[0].isBroken == True):
                        self.pickAxes.pop(0)



    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def placeWall(self):
        print("place wall")
        new_wall = Wall(self.game, self.x, self.y)
        self.groups.add(new_wall)
        self.group1.add(new_wall)

    def shoot(self, x, y):
        if (self.arrows > 0):
            Bullet = bullet(self.game, self.x, self.y, self)
            Bullet.dirx = x
            Bullet.dirY = y
            Bullet.add(self.groups)
            Bullet.add(self.game.bullets)
            self.arrow_sound.play()
            self.arrows -= 1
        else:

            self.font = pg.font.Font('freesansbold.ttf', 30)
            self.last = pg.time.get_ticks()
            self.ArrowText = self.font.render("No arrows!", 1, (255, 255, 255))
            self.arrowText1 = text(self.game, "No arrows!", True, self)
            for text1 in self.game.texts:
                self.game.texts.remove(text1)
            self.game.texts.append(self.arrowText1)
            while (self.last % 200 != 0):
                self.last = pg.time.get_ticks()
                pg.display.update()


class bullet(pg.sprite.Sprite):
    def __init__(self, game, x, y,player):
        self.groups = game.all_sprites
        self.group1 = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.last = pg.time.get_ticks()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dirx = 0
        self.dirY = 0

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
    def collide_with_rabbit(self, dx=0, dy=0):
        for rabbit in self.game.rabbits:
            if rabbit.x == self.x + dx and rabbit.y == self.y + dy:
                rabbit.isDead = True
                rabbit.image = pg.image.load("rabbit_dead.png").convert_alpha()
                self.image.get_rect()
                return True
        return False

    def collide_with_bear(self, dx=0, dy=0):
        for bear in self.game.bears:
            if bear.x == self.x + dx and bear.y == self.y + dy:
                bear.isDead = True
                bear.image.fill(WHITE)
                self.player.kills += 1
                return True
    def move(self):
        print(self.x)
        print("fesf")
        now = pg.time.get_ticks()
        if self.collide_with_rabbit():
            self.kill()
        if self.collide_with_bear():
            self.kill()
        if not self.collide_with_walls(self.dirx, self.dirY):
            if (now % 25 == 0):
                self.x += self.dirx
                self.y += self.dirY
        else:
            self.kill()


class Wall(pg.sprite.Sprite):  # traditional, non-passable wall
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load("stone_wall.png").convert_alpha()  # loads in the stone.png file
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class PassableWall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls  # groups what passable wall are included in
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))  # making it our TILESIZE
        self.image.fill(SKYBLUE)  # changes the color of the block
        self.rect = self.image.get_rect()  # creates a rectangle
        self.x = x  # x position
        self.y = y  # y position
        self.rect.x = x * TILESIZE  # set's its x position
        self.rect.y = y * TILESIZE  # set's its y position


class Stone(pg.sprite.Sprite):  # How stones in the game will be created
    def __init__(self, game, x, y):
        super(Stone, self).__init__()
        self.groups = game.all_sprites,game.stone
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("stone.png").convert_alpha()  # loads in the stone.png file
        self.image.set_colorkey((255, 255, 255))  # don't need for this one, but the background color will be white
        self.rect = self.image.get_rect()  # saying that the image is the rectagle
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.stone = 10
    def mining(self):
        if self.stone <= 0:
            self.kill()


class Food(pg.sprite.Sprite):  # Creating Food for the game
    def __init__(self, game, x, y):
        super(Food, self).__init__()  # gives access to methods and properties
        self.groups = game.all_sprites,game.food  # groups Food with all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("food.png").convert_alpha()  # loads in our food.png file
        self.image.set_colorkey((255, 255, 255))  # sets the transparent's background color to white
        self.rect = self.image.get_rect()  # says the image is in the rectangle
        self.x = x
        self.y = y
        self.food = 10
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def collecting(self):
        if self.food <= 0:
            self.kill()


class Gold(pg.sprite.Sprite):  # Creating Gold Ore for the game
    def __init__(self, game, x, y):
        super(Gold, self).__init__()  # gives access to methods and properties
        self.groups = game.all_sprites, game.gold # groups gold with all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("gold_ore.png").convert_alpha()  # loads in our gold.png file
        self.image.set_colorkey((255, 255, 255))  # sets the transparent's background color to white
        self.goldChange = 0
        self.gold = 10
        self.rect = self.image.get_rect()  # says the image is in the rectangle
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def mining(self):
        if self.gold <= 0:
            self.kill()


class Wood(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super(Wood, self).__init__()  # gives access to methods and properties
        self.groups = game.all_sprites, game.wood  # groups wood with all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("wood.png").convert_alpha()  # loads in our wood.png file
        self.image.set_colorkey((255, 255, 255))  # sets the transparent's background color to white
        self.rect = self.image.get_rect()  # says the image is in the rectangle
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.wood = 10
    def collecting(self):
        if self.wood <= 0:
            self.kill()


class rabbit(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.rabbits
        pg.sprite.Sprite.__init__(self, self.groups)
        self.last = pg.time.get_ticks()
        self.coolDown = 300
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load("rabbit.png").convert_alpha()  # loads in our gold.png file
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.isDead = False

    def move(self, dx=0, dy=0, px=0, py=0):

        now = pg.time.get_ticks()
        if(self.isDead == False):
            if not self.collide_with_walls(dx, dy):
                if (now % 200 == 0):
                    self.x += dx
                    self.y += dy
            if (now % 75 == 0):
                if (self.x - px < 0 and self.y == py):
                    print("right")
                    if not self.collide_with_walls(-1, 0):
                        self.x -= 1
                if (px - self.x < 0 and self.y == py):
                    print("left")
                    if not self.collide_with_walls(1, 0):
                        self.x += 1
                if (self.y - py < 0 and self.x == px):
                    print("up")
                    if not self.collide_with_walls(0, -1):
                        self.y -= 1
                if (py - self.y < 0 and self.x == px):
                    print("down")
                    if not self.collide_with_walls(0, 1):
                        self.y += 1

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    # Coppied from collide with wall. Will eventually be a door. Probably needs to be edited.
    def collide_with_passableWalls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def background(self):
        self.image = pg.image.load("background.jpg")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0, 0)
    #def randomSpawnedItems(pg.sprite.Sprite)

class pickAxe(pg.sprite.Sprite):
    def __init__(self, game):
        super(pickAxe, self).__init__()  # gives access to methods and properties
        self.groups = game.all_sprites  # groups wood with all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("pickaxe.png").convert_alpha()  # loads in our wood.png file
        self.image.set_colorkey((255, 255, 255))  # sets the transparent's background color to white
        self.rect = self.image.get_rect()  # says the image is in the rectangle
        self.isBroken = False
        self.durability = 100
    def swing(self):
        durabiltiyLost = random.randint(1,5)
        self.durability -= durabiltiyLost
        if(self.durability <= 0):
            print("broken")
            self.isBroken = True

class sythe(pg.sprite.Sprite):
    def __init__(self, game):
        super(sythe, self).__init__()  # gives access to methods and properties
        self.groups = game.all_sprites  # groups wood with all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("scythe.png").convert_alpha()  # loads in our wood.png file
        self.image.set_colorkey((255, 255, 255))  # sets the transparent's background color to white
        self.rect = self.image.get_rect()  # says the image is in the rectangle
        self.isBroken = False
        self.durability = 100
    def swing(self):
        durabiltiyLost = random.randint(1,5)
        self.durability -= durabiltiyLost
        if(self.durability <= 0):
            print("broken")
            self.isBroken = True

class axe(pg.sprite.Sprite):
    def __init__(self, game):
        super(axe, self).__init__()  # gives access to methods and properties
        self.groups = game.all_sprites  # groups wood with all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load("wood.png").convert_alpha()  # loads in our wood.png file
        self.image.set_colorkey((255, 255, 255))  # sets the transparent's background color to white
        self.rect = self.image.get_rect()  # says the image is in the rectangle
        self.isBroken = False
        self.durability = 100
    def swing(self):
        durabiltiyLost = random.randint(1,5)
        self.durability -= durabiltiyLost
        if(self.durability <= 0):
            print("broken")
            self.isBroken = True

class bear(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bears
        pg.sprite.Sprite.__init__(self, self.groups)
        self.last = pg.time.get_ticks()
        self.coolDown = 300
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.collision_sound = pg.mixer.Sound("collision.wav")
        self.image = pg.image.load("bear.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.isDead = False
    def isDeadFunction(self):
        self.image = self.image = pg.image.load("bear_dead.png").convert_alpha()


    def move(self, dx=0, dy=0, px=0, py=0):
        now = pg.time.get_ticks()
        self.attackMove = False
        if(self.isDead == False):
            if (now % 50 == 0):
                if (self.x - px < 0 and self.y == py):
                    print("left")
                    if not self.collide_with_walls(1, 0) and not self.collide_with_Player(1,0):
                        self.x += 1
                        self.attackMove = True
                    if self.collide_with_Player(1,0):
                        healthLost = random.randint(1,5)
                        self.game.player.health -= healthLost
                        self.game.player.health -= healthLost
                if (px - self.x < 0 and self.y == py):
                    print("right")
                    if not self.collide_with_walls(-1, 0) and not self.collide_with_Player(-1,0):
                        self.x -= 1
                        self.attackMove = True
                    if self.collide_with_Player(-1,0):
                        healthLost = random.randint(1,5)
                        self.game.player.health -= healthLost
                        self.game.player.health -= healthLost
                if (self.y - py < 0 and self.x == px):
                    print("down")
                    if not self.collide_with_walls(0, 1) and not self.collide_with_Player(0,1):
                        self.y += 1
                        self.attackMove = True
                    if self.collide_with_Player(0,1):
                        healthLost = random.randint(1,5)
                        self.game.player.health -= healthLost
                        self.game.player.health -= healthLost
                if (py - self.y < 0 and self.x == px):
                    print("up")
                    if not self.collide_with_walls(0, -1) and not self.collide_with_Player(0,-1):
                        self.y -= 1
                        self.attackMove = True
                    if self.collide_with_Player(0,-1):
                        healthLost = random.randint(1,5)
                        self.game.player.health -= healthLost
                        self.game.player.health -= healthLost
                if(self.attackMove == False):
                    if not self.collide_with_walls(dx, dy):
                        self.x += dx
                        self.y += dy

                print(self.game.player.health)

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
    def collide_with_Player(self, dx=0, dy=0):
        if self.game.player.x == self.x + dx and self.game.player.y == self.y + dy:
            print("collided")
            return True
        return False

    # Coppied from collide with wall. Will eventually be a door. Probably needs to be edited.
    def collide_with_passableWalls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE