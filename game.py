#!/usr/bin/env python

import pygame

class Camera(object):
    def __init__(self, aim=(0, 0), zoom=1.0, viewport=None):
        self.__aim = aim
        self.__zoom = zoom

        self.__viewport = None

    @property
    def offset(self):
        return self.__aim

    @property
    def zoom(self):
        return self.__zoom

    def set_viewport(self, viewport):
        self.__viewport = viewport


class Game(object):
    def __init__(self, destination, static_background=None):
        self.__scr = destination
        self.__background = static_background

        self.__camera = Camera(viewport=self.__scr.get_size())

        self.__ingame = True

    def update(self):
        if self.__background:
            self.__scr.blit(self.__background.subsurface(self.__camera),
                            (0, 0))
        pygame.display.update()

class Space(object):
    def __init__(self):
        pass

class Planet(object):
    def __init__(self):
        pass
