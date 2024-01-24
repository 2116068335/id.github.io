import time


import pygame
from pygame import *

def main():

    screen = pygame.display.set_mode((547, 682), 0, 32)
    background = pygame.image.load("./feji/feji1.png")
    player = pygame.image.load("./feji/feji2.png")

    x=547/2-134/2
    y=500

    while True:
        screen.blit(background, (0, 0))
        screen.blit(player, (x, y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            print("上")
            y+=1
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            print("下")
            y-=1
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            print("左")
            x-=1
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            print("右")
            x+=1
        if key_pressed[K_SPACE]:
            print("空格")

        pygame.display.update()
        pygame.time.delay(10)


if __name__ == "__main__":
    main()
