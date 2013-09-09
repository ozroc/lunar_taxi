#!/usr/bin/env python

import pygame

try:
    import android
except ImportError:
    android = None
import game

#try:
#    import android.mixer as mixer
#except ImportError:
#    import pygame.mixer as mixer


def main():
    if android:
        android.init()
        android.accelerometer_enable(True)
    pygame.init()

    screen = pygame.display.set_mode((800, 480))
    c=game.Controls(android)
    while True:
        print c.angle/3.14159, c.press

if __name__ == '__main__':
    main()
