import pygame
import random
import sys
from pygame.locals import *
from os import path


H = 800
W = 600
Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Blue = (0, 0, 255)
Green = (0, 255, 0)
Yellow = (255, 255, 0)
FPS = 60
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, Blue)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (80, 150))
        self.image.set_colorkey(White) 
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        self.rect.centerx = W/2
        self.rect.bottom = H-10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > W:
            self.rect.right = W
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


class MoB(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(baby_img, (50, 50))
        self.image.set_colorkey(White)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.85/2)
        self.rect.x = random.randrange(W - self.rect.width)
        self.rect.y = random.randrange(-150, -110)
        self.speedy = random.randrange(3, 10)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > H + 10 or self.rect.left < -25 or self.rect.right > W + 20:
            self.rect.x = random.randrange(W - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(Red)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


def newmob():
    m = MoB()
    all_sprites.add(m)
    mobs.add(m)


def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return


pygame.init()
pygame.mixer.init()
surface = pygame.display.set_mode((W, H))
pygame.display.set_caption('Воздушные баталии')
mainClock = pygame.time.Clock()

snd_dir = path.join(path.dirname(__file__), 'snd')
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'fonbit.mp3'))
pygame.mixer.music.set_volume(0.4)
gameOverSound = pygame.mixer.Sound(path.join(snd_dir, 'gameover.wav'))

img_dir = path.join(path.dirname(__file__), 'img')

pole = pygame.image.load(path.join(img_dir, 'pole.jpg')).convert()
pole_rect = pole.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'player.jpg')).convert()
exit_menu = pygame.image.load(path.join(img_dir, 'tet_exit.jpg')).convert()
ex_rect = exit_menu.get_rect()
menu_img = pygame.image.load(path.join(img_dir, 'tet1_menu.jpg')).convert()
menu_rect = menu_img.get_rect()

baby_img = pygame.image.load(path.join(img_dir, 'baby.jpg')).convert()
mod_img = pygame.image.load(path.join(img_dir, 'mod.jpg')).convert()

while True:
    score = 0
    menu = 1
    surface.fill(Black)
    surface.blit(menu_img, menu_rect)
    pygame.display.update()
    while score == 0:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    score += 1
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_2:
                    if menu % 2 != 0:  
                        pole = pygame.image.load(path.join(img_dir, 'pole3.jpg')).convert()
                        pole_rect = pole.get_rect()
                        player_img = pygame.image.load(path.join(img_dir, 'player2.jpg')).convert()
                        exit_menu = pygame.image.load(path.join(img_dir, 'kon_exit.jpg')).convert()
                        ex_rect = exit_menu.get_rect()
                        menu_img = pygame.image.load(path.join(img_dir, 'koc1_menu.jpg')).convert()
                        menu_rect = menu_img.get_rect()
                        baby_img = mod_img
                        surface.fill(Black)
                        surface.blit(menu_img, menu_rect)
                        pygame.display.update()
                        menu += 1
                        continue
                    else: 
                        pole = pygame.image.load(path.join(img_dir, 'pole.jpg')).convert()
                        pole_rect = pole.get_rect()
                        player_img = pygame.image.load(path.join(img_dir, 'player.jpg')).convert()
                        exit_menu = pygame.image.load(path.join(img_dir, 'tet_exit.jpg')).convert()
                        ex_rect = exit_menu.get_rect()
                        menu_img = pygame.image.load(path.join(img_dir, 'tet1_menu.jpg')).convert()
                        menu_rect = menu_img.get_rect()
                        baby_img = pygame.image.load(path.join(img_dir, 'baby.jpg')).convert()
                        surface.fill(Black)
                        surface.blit(menu_img, menu_rect)
                        pygame.display.update()
                        menu += 1
                        continue
                if event.key == K_3:
                    continue
                if event.key == K_4:
                    terminate()
    player = Player()
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    all_sprites.add(player)
    for i in range(8):
        newmob()

    surface.fill(Black)
    surface.blit(pole, pole_rect)
    all_sprites.draw(surface)
    score = 0
    pygame.mixer.music.play(loops=-1)
    game_over = True
    running = True
    while running:
        if game_over:
            game_over = False
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            for i in range(8):
                newmob()
            score = 0

        mainClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 50-hit.radius
            newmob()

        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            running = False

        surface.fill(Black)
        surface.blit(pole, pole_rect)
        all_sprites.draw(surface)
        draw_text(surface, str(score), 30, W/2, 20)
        pygame.display.flip()
    pygame.mixer.music.stop()
    gameOverSound.play()
    surface.fill(Black)
    surface.blit(exit_menu, ex_rect)
    pygame.display.update()
    waitForPlayerToPressKey()
    gameOverSound.stop()

  