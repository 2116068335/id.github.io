import random

import pygame
from pygame import *


#敌方飞机：
class EnemyPlane(pygame.sprite.Sprite):
    enemy_bullets = pygame.sprite.Group()
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.enemy = pygame.image.load("./feji/小飞机.png")

        self.rect = self.enemy.get_rect()

        x = random.randrange(0, Manager.bg_size[0], 12)
        self.rect.topleft = [x, 0]

        self.speed = 5
        self.screen = screen

        self.bullets = pygame.sprite.Group()
        #self.explosion = Bomb(screen, type="enemy")

        self.directions = ['left', 'right']
        self.direction = random.choice(self.directions)

    def display(self):
        self.screen.blit(self.enemy, self.rect)
        self.bullets.update()
        self.bullets.draw(self.screen)

    def update(self):
        self.fire()
        self.move()
        self.display()

    def move(self):
        if self.direction == 'right':
            self.rect.right += self.speed

        elif self.direction == 'left':
            self.rect.right -= self.speed

        if random.randint(1, 100) <= 5:  # 5% 的概率改变方向
            self.direction = random.choice(self.directions)

        if self.rect.right < 0:
            self.direction = 'right'
        elif self.rect.right > Manager.bg_size[0] - 45:
            self.direction = 'left'

        if self.direction == 'right':
            self.rect.right += self.speed
        elif self.direction == 'left':
            self.rect.right -= self.speed

        self.rect.bottom += self.speed

    def fire(self):
        num = random.randint(1, 10)
        if num == 8:
            enemybullet = EnemyBullet(self.screen, self.rect.left, self.rect.top)
            self.bullets.add(enemybullet)
            EnemyPlane.enemy_bullets.add(enemybullet)

    @classmethod
    def clear_bullets(cls):
        cls.enemy_bullets.empty()


#敌方子弹：
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./feji/子弹2.png")

        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 58 / 2 - 5 / 2, y + 11]

        self.speed = 10
        self.screen = screen

    def update(self):
        self.rect.top += self.speed
        if self.rect.top > 700:
            self.kill()


#我方飞机：
class HeroPlane(pygame.sprite.Sprite):
    bullets = pygame.sprite.Group()
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.player = pygame.image.load("./feji/feiji.png")

        self.rect = self.player.get_rect()
        self.rect.topleft = [480/2-102/2, 600]

        self.speed = 10
        self.screen = screen

        self.bullets = pygame.sprite.Group()

    def key_control(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            self.rect.top -= self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            self.rect.bottom += self.speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            self.rect.left -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            self.rect.right += self.speed
        if key_pressed[K_SPACE]:
            bullet = Bullet(self.screen, self.rect.left, self.rect.top)
            self.bullets.add(bullet)
            HeroPlane.bullets.add(bullet)

    def update(self):
        self.key_control()
        self.display()

    def display(self):
        self.screen.blit(self.player, self.rect)
        self.bullets.update()
        self.bullets.draw(self.screen)

    @classmethod
    def clear_bullets(cls):
        cls.bullets.empty()

#我方子弹：
class Bullet(pygame.sprite.Sprite):

    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./feji/子弹1.png")

        self.rect = self.image.get_rect()
        self.rect.topleft = [x+102/2-5/2, y-11]

        self.speed = 10
        self.screen = screen

    def update(self):
        self.rect.top -= self.speed
        if self.rect.top < -11:
            self.kill()


#爆炸：
class Bomb(object):
    def __init__(self, screen, type):
        self.screen = screen

        if type == "enemy":
            self.mImages = [pygame.image.load("./feji/小飞机" + str(v) + ".png") for v in range(1, 5)]

        else:
            self.mImages = [pygame.image.load("./feji/feiji" + str(v) + ".png") for v in range(1, 5)]

        self.mIndex = 0
        self.mPos = [0, 0]
        self.mVisible = False

    def action(self, rect):
        self.mPos[0] = rect.left
        self.mPos[1] = rect.top
        self.mVisible = True

    def draw(self):
        if not self.mVisible:
            return
        self.screen.blit(self.mImages[self.mIndex], (self.mPos[0], self.mPos[1]))
        self.mIndex += 1
        if self.mIndex >= len(self.mImages):
            self.mIndex = 0
            self.mVisible = False


class Manager(object):
    bg_size = (480, 700)

    creat_enemy_id = 10
    game_over = 11
    is_game_over = False
    over_time = 3

    def __init__(self):
        self.screen = pygame.display.set_mode((480, 700), 0, 32)
        self.background = pygame.image.load("./feji/feji4.png")

        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player_bomb = Bomb(self.screen, "player")
        self.enemy_bomb = Bomb(self.screen, "enemy")

    def exit(self):
        pygame.quit()
        exit()

   # def show_over_text(self):
        #self.drawText("gameover %d" % Manager.over_time, 100, Manager.bg_size[1]/2,
                     # textHeight=50, fohtColor=[255, 0, 0])

    def game_over_timer(self):
        self.show_over_text()
        Manager.game_over -= -1
        if Manager.over_time == 0:
            pygame.time.set_timer(Manager.game_over, 0)
            Manager.over_time = 3
            Manager.is_game_over  = False
            self.start_game()

    def start_game(self):
        EnemyPlane.clear_bullets()
        HeroPlane.clear_bullets()
        manager = Manager()
        manager.main()

    def new_player(self):
        player = HeroPlane(self.screen)
        self.players.add(player)

    def new_enemy(self):
        enemy = EnemyPlane(self.screen)
        self.enemies.add(enemy)

    def main(self):
        self.new_player()
        self.new_player()
        pygame.time.set_timer(Manager.creat_enemy_id, 1000)


        while True:
            self.screen.blit(self.background, (0, 0))

            #self.drawText('hp:10000', 0, 0)
            #if Manager.is_game_over:
                #self.show_over_text()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == Manager.creat_enemy_id:
                    self.new_enemy()

            self.player_bomb.draw()
            self.enemy_bomb.draw()
            #飞机碰撞：
            iscollide = pygame.sprite.groupcollide(self.players, self.enemies, True, True)

            if iscollide:
                Manager.is_game_over = True
                pygame.time.set_timer(Manager.game_over, 1000)
                items = list(iscollide.items())[0]
                print(items)
                x = items[0]
                y = items[1][0]
                self.player_bomb.action(x.rect)
                self.enemy_bomb.action(y.rect)

            #子弹消灭敌机：
            is_enemy = pygame.sprite.groupcollide(HeroPlane.bullets, self.enemies, True, True)

            if is_enemy:
                items = list(is_enemy.items())[0]
                print(items)
                y = items[1][0]
                self.enemy_bomb.action(y.rect)

            #子弹消灭我方飞机：
            """
            if self.players.sprites():
                isover = pygame.sprite.spritecollide(self.players.sprites()[0], EnemyPlane.enemy_bullets, True)
                if isover:
                    Manager.is_game_over = True
                    pygame.time.set_timer(Manager.game_over, 1000)
                    print("中弹")
                    self.player_bomb.action(self.players.sprites()[0].rect)
                    self.players.remove(self.players.sprites()[0])
            """




            self.players.update()
            self.enemies.update()

            pygame.display.update()
            pygame.time.delay(10)

if __name__ == "__main__":
    manager = Manager()
    manager.main()