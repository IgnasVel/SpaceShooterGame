from typing import Any
from pygame import *
from random import randint
from time import time, sleep

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
mixer_music.set_volume(0.1)
fire_sound.set_volume(0.1)

font.init()
font2 = font.SysFont('Arial', 36)
font3 = font.SysFont('Arial', 64)
 

img_back = "galaxy.jpg" 
img_hero = "rocket.png" 
img_enemy = "ufo.png" 
img_asteroid = "asteroid.png"
time_start = time()
score = 0 
lost = 0 


class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       
       sprite.Sprite.__init__(self)
 
       
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
        

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fire()
    def check_collision(self):
        for monster in monsters:
            if self.rect.colliderect(monster.rect):
                global ship_collided
                ship_collided = True     
        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                ship_collided = True     

    def fire(self):
        bullet_spawn_x = self.rect.x + 31
        bullet_spawn_y = self.rect.y - 15
        bullet = Bullet("bullet.png", bullet_spawn_x, bullet_spawn_y, 20, 20, 15)
        bullets.add(bullet)
        fire_sound.play()
        #pass
    
 
class Enemy(GameSprite):
   
    def update(self):
       
        self.rect.y += self.speed
        global lost
        
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
    def shot(self):
        self.rect.x = randint(80, win_width - 80)
        self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        for monster in monsters:
            if self.rect.colliderect(monster.rect):
                global score
                score += 1
                monster.shot()
                self.kill()
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()
     
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
 
asteroids = sprite.Group()
for i in range(1,8):
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)
bullets = sprite.Group()

finish = False
run = True
ship_collided = False
time_current = 0
  
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:   
        window.blit(background,(0,0))    
        text_victory = font3.render("You Win!", 1, (30, 255, 30))
        text_Defeat = font3.render("You Lose!", 1, (255, 30, 30))
 
            
    
        
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
    
    
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        

        
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        time_end = time()

        time_current = time_end - time_start
        time_current = round(time_current, 2)
        text_timer = font2.render(str(time_current) + "s", 1, (255, 255, 255))
        window.blit(text_timer, (10, 80))
        
        
        if score >= 10:
            window.blit(text_victory, (250, 250))
            finish = True

        ship.check_collision()
        if ship_collided == True or lost >= 3:
           window.blit(text_Defeat, (250, 250))
           finish = True
        display.update()
    
        sleep(0.05)