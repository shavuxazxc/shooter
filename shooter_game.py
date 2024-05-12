#Создай собственный Шутер!

from pygame import *
from random import randint
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
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_s] and self.rect.y < 450:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1
class Asteroidss(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
galaxy = transform.scale(image.load('galaxy.jpg'), (700, 500))
ufo = Enemy('ufo.png', 600, 350, 60, 60, 2)
asteroid = Asteroidss('asteroid.png', 600, 350, 60, 60, 2)
hero = Player('rocket.png', 0, 0, 80, 100, 10)
mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()
game = True
Finish = False
ufos = sprite.Group()
ufos.add(ufo)
asteroids = sprite.Group()
asteroids.add(asteroid)

clock = time.Clock()
FPS = 60
lost = 0
score = 0
max_lost = 3
goal = 10
font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 150)
text_win = font2.render('YOU ARE WIN', 1, (0, 255, 0))
text_porazhenie = font2.render('YOU ARE LOSE', 1, (255, 0, 0))


while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                hero.fire()
    if Finish != True:
        window.blit(galaxy, (0, 0))
        collides = sprite.groupcollide(ufos, bullets, True, True)
       
        for c in collides:
            score = score + 1
            ufo = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            ufos.add(ufo)
        if sprite.spritecollide(hero, ufos, False) or lost >= max_lost:
            Finish = True
            window.blit(text_porazhenie, (0, 250))
        if sprite.spritecollide(hero, asteroids, False) or lost >= max_lost:
            Finish = True
            window.blit(text_porazhenie, (0, 250))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (20, 40))
        text = font1.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (20, 20))
        if score >= goal:
            Finish = True
            window.blit(text_win, (0, 150))
        if lost >= max_lost:
            inish = True
            window.blit(text_porazhenie, (0, 150)) 
        
        
        
        hero.update()
        ufo.update()
        ufos.update()
        asteroid.update()
        asteroids.update()
        bullets.update()
        hero.reset()    
        ufo.reset()
        asteroid.reset()
        ufos.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        display.update()
        clock.tick(FPS)
    
time.delay(50)