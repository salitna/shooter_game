#Создай собственный Шутер!

from pygame import *
from random import *
lost = 0 
chet = 0

class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= 10
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += 10

        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 10
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += 10
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y <= 630:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(80, win_w - 80)
            self.speed = randint(1, 5)
            lost = lost + 1

class Enemy_ast(GameSprite):
    def update(self):
        if self.rect.y <= 630:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(80, win_w - 80)
            self.speed = randint(4, 7)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill

win_w = 700
win_h = 500

window = display.set_mode((win_w, win_h))
display.set_caption('Maze')

font.init()
font1 = font.SysFont("Calibri", 70)
win = font1.render("YOU WIN!", True, (225, 215, 0))
lose = font1.render("YOU LOSE!", True, (225, 0, 0))

background = transform.scale(image.load('galaxy.jpg'), (700, 500))
hero = Player('rocket.png', 0, win_h - 100, 80, 100, 4)
monsters = sprite.Group()
asts = sprite.Group()
bullets = sprite.Group()

for i in range(1, 5):
    monster = Enemy('ufo.png', randint(80, win_w - 80), -50, 80, 50, randint(1,5))
    monsters.add(monster)

for i in range(1, 3):
    ast = Enemy_ast('asteroid.png', randint(80, win_w - 80), -50, 80, 50, randint(1,5))
    asts.add(ast)

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()

game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            hero.fire()
            fire_sound.play()
                
    if finish != True:
        window.blit(background, (0, 0))
        hero.update()
        hero.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asts.update()
        asts.draw(window)
        font2 = font.SysFont("Calibri", 30)
        lostt = font2.render("Пропущено: " + str(lost), True, (255, 255, 255))
        losttt = font2.render("Cчёт: " + str(chet), True, (255, 255, 255))
        window.blit(lostt, (0, 37))
        window.blit(losttt, (0, 9))
        
        if sprite.groupcollide(bullets, monsters, True, True):
            chet += 1
            monster = Enemy('ufo.png', randint(80, win_w - 80), -50, 80, 50, randint(1,5))
            monsters.add(monster)
        
        sprite.groupcollide(bullets, asts, True, False)

        
        if sprite.collide_rect(hero, ast):
            window.blit(lose, (200, 200))
            finish = True

        
        if lost >= 3:
            window.blit(lose, (200, 200))
            finish = True

        if chet >= 11:
            window.blit(win, (200, 200))
            finish = True



    clock.tick(FPS)
    display.update()