import pygame
import sys
import math
import random
import time

pygame.init()

points = 0

text = '0'
font = pygame.font.SysFont(None, 48)
txt_points = font.render(text, True, (255,255,255))

display = pygame.display.set_mode((800,600))
pygame.display.set_caption("Slime Shooter")
clock = pygame.time.Clock()

player_walk_images = [pygame.image.load('player_walk_0.png'), pygame.image.load('player_walk_1.png'),
pygame.image.load('player_walk_2.png'), pygame.image.load('player_walk_3.png')]

player_weapon = pygame.image.load('shotgun.png').convert()
player_weapon.set_colorkey((255,255,255))

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        self.rect = player_walk_images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False
    def handle_weapons(self,display):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - player.rect.x, mouse_y - player.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        player_weapon_copy = pygame.transform.rotate(player_weapon, angle)
        display.blit(player_weapon_copy, (self.rect.x +15-int(player_weapon.get_width()/2), self.rect.y+25-int(player_weapon_copy.get_height()/2)))

    def main(self, display):
        if self.animation_count + 1 >= 16:
            self.animation_count = 0
        self.animation_count += 1
        if self.moving_right:
            display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (32,42)), (self.rect.x, self.rect.y))
        elif self.moving_left:
            display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32,42)), (self.rect.x, self.rect.y))
        #pygame.draw.rect(display, (255,0,0), (self.x, self.y, self.width, self.height))
        else:
            display.blit(pygame.transform.scale(player_walk_images[0], (32,42)), (self.rect.x, self.rect.y))
        self.handle_weapons(display)
        self.moving_right = False
        self.moving_left = False

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,mouse_x,mouse_y, speed):
        self.rect = pygame.rect.Rect(x, y, 5, 5)
        self.rect.x = x
        self.rect.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = speed
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

    def main(self, display):
        self.rect.x -= int(self.x_vel)
        self.rect.y -= int(self.y_vel)

        pygame.draw.circle(display, (0,0,0), (self.rect.x, self.rect.y), 5)

class Slimeenemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.animation_images = [pygame.image.load('slime_animation_0.png'), pygame.image.load('slime_animation_1.png'),
        pygame.image.load('slime_animation_2.png'), pygame.image.load('slime_animation_3.png'),]
        self.cooldown = time.time() + 1
        self.rect = self.animation_images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-150,150)
        self.offset_y = random.randrange(-150,150)
    def main(self, display):
        # if self.cooldown - time.time() <= 0:
        #     self.cooldown = time.time() + 1
        #     enemy_bullets.append(Bullet(self.rect.centerx-display_scroll[0], self.rect.centery-display_scroll[1], player.rect.centerx, player.rect.centery, 5))


        if self.animation_count + 1 == 16:
            self.animation_count = 0
        self.animation_count += 1

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-150,150)
            self.offset_y = random.randrange(-150,150)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1

        if player.rect.x + self.offset_x > self.rect.x-display_scroll[0]:
            self.rect.x += 1
        elif player.rect.x + self.offset_x < self.rect.x-display_scroll[0]:
            self.rect.x -= 1

        if player.rect.y + self.offset_y > self.rect.y-display_scroll[1]:
            self.rect.y += 1
        elif player.rect.y + self.offset_y < self.rect.y-display_scroll[1]:
            self.rect.y -= 1
        
        display.blit(pygame.transform.scale(self.animation_images[self.animation_count//4], (32,30)), (self.rect.x-display_scroll[0], self.rect.y-display_scroll[1]))

enemies: list[Slimeenemy] = [Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300), Slimeenemy(400,300)]

player = Player(400,300,32,32)

display_scroll = [0,0]

# enemy_bullets = []

player_bullets: list[Bullet] = []

while True:
    display.fill((24,164,86))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.QUIT
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bullets.append(Bullet(player.rect.centerx,player.rect.centery, mouse_x, mouse_y, 15))

    keys = pygame.key.get_pressed()

    pygame.draw.rect(display, (255,255,255), (100-display_scroll[0],100-display_scroll[1],16,16))

    if keys[pygame.K_a]:
        display_scroll[0] -= 5
        player.moving_left = True
    if keys[pygame.K_d]:
        display_scroll[0] += 5
        player.moving_right = True
    if keys[pygame.K_w]:
        display_scroll[1] -= 5
    if keys[pygame.K_s]:
        display_scroll[1] += 5

    player.main(display)

    for bullet in player_bullets:
        bullet.main(display)

    # for bullet in enemy_bullets:
    #     bullet.main(display)

    for enemy in enemies:
        enemy.main(display)

    for bullet in player_bullets:
        for enemy in enemies:
            if bullet.rect.colliderect((enemy.rect.left-display_scroll[0], enemy.rect.top-display_scroll[1]), (enemy.rect.width, enemy.rect.height)):
                player_bullets.remove(bullet)
                enemies.remove(enemy)
                points += 1
                txt_points = font.render(str(points), True, (255, 255, 255))
    for enemy in enemies:
        if enemy.rect.colliderect((player.rect.left-display_scroll[0], player.rect.top-display_scroll[1]), (player.rect.width, player.rect.height)):
            enemies.remove(enemy)
            player.remove(player)

    display.blit(txt_points, (10, 60))
    clock.tick(60)
    pygame.display.update()