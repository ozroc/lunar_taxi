#!/usr/bin/env python

import pygame

try:
    import android
except ImportError:
    android = None
import game

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer

import game

def load_image(filename):
    return pygame.image.load(filename).convert_alpha()

def main():
    if android:
        android.init()
        android.accelerometer_enable(True)
    pygame.init()

    screen = pygame.display.set_mode((800, 480))
    
    space = game.Space(load_image('background.jpg'))
    camera = game.Camera(space)
    direction = game.DIR_STOP

    in_game = True
    while in_game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            elif (event.type == pygame.KEYDOWN and
                  event.key == pygame.K_ESCAPE):
                in_game = False
            elif (event.type == pygame.KEYDOWN and
                  event.key == pygame.K_LEFT):
                direction = game.DIR_LEFT
            elif (event.type == pygame.KEYDOWN and
                  event.key == pygame.K_RIGHT):
                direction = game.DIR_RIGHT
            elif ((event.type == pygame.KEYUP) and
                  (event.key == pygame.K_LEFT) and
                  (direction == game.DIR_LEFT)):
                direction = game.DIR_STOP
            elif ((event.type == pygame.KEYUP) and
                  (event.key == pygame.K_RIGHT) and
                  (direction == game.DIR_RIGHT)):
                direction = game.DIR_STOP
            elif (event.type == pygame.KEYDOWN and
                  event.key == pygame.K_UP):
                direction = game.DIR_UP
            elif (event.type == pygame.KEYDOWN and
                  event.key == pygame.K_DOWN):
                direction = game.DIR_DOWN
            elif ((event.type == pygame.KEYUP) and
                  (event.key == pygame.K_UP) and
                  (direction == game.DIR_UP)):
                direction = game.DIR_STOP
            elif ((event.type == pygame.KEYUP) and
                  (event.key == pygame.K_DOWN) and
                  (direction == game.DIR_DOWN)):
                direction = game.DIR_STOP

        camera.move_camera(direction)
        dirty = screen.blit(camera.view, (0, 0))
        pygame.display.flip()
    
if __name__ == '__main__':
    main()
