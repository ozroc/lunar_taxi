#!/usr/bin/env python

import pygame

DIR_STOP = 0
DIR_UP = 1
DIR_DOWN = 2
DIR_LEFT = 3
DIR_RIGHT = 4

class Camera(object):
    def __init__(self, space):
        self.space = space
        self.__speed = 8
        self.__offset = (0, 0)

        screen = pygame.display.get_surface()
        self.__image = pygame.Surface(screen.get_size())
        self.__image.blit(self.space.image.subsurface(pygame.Rect(self.__offset,
                                                                  self.__image.get_size())), self.__offset)

    def move_camera(self, direction):
        view_size = self.__image.get_size()
        src_size = self.space.image.get_size()

        if direction == DIR_LEFT:
            if self.__offset[0] - self.__speed < 0:
                self.__offset = (0, self.__offset[1])
            else:
                self.__offset = (self.__offset[0] - self.__speed,
                                 self.__offset[1])

        elif direction == DIR_RIGHT:
            if ((self.__offset[0] + view_size[0] + self.__speed) > src_size[0]):
                self.__offset = (src_size[0] - view_size[0], self.__offset[1])
            else:
                self.__offset = (self.__offset[0] + self.__speed,
                                 self.__offset[1])

        elif direction == DIR_UP:
            if self.__offset[1] - self.__speed < 0:
                self.__offset = (self.__offset[0], 0)
            else:
                self.__offset = (self.__offset[0],
                                 self.__offset[1] - self.__speed)

        elif direction == DIR_DOWN:
            if ((self.__offset[1] + view_size[1] + self.__speed) > src_size[1]):
                self.__offset = (self.__offset[0], src_size[1] - view_size[1])
            else:
                self.__offset = (self.__offset[0],
                                 self.__offset[1] + self.__speed)

        src_rect = pygame.Rect(self.__offset, view_size)
        self.__image.blit(self.space.image.subsurface(src_rect), (0, 0))


    @property
    def view(self):
        return self.__image


class Game(object):
    def __init__(self, space):
        self.space = space

    def update(self):
        self.space.update()

class Space(object):
    def __init__(self, static_background=None):
        self.background = static_background

    def update(self):
        pass

    @property
    def render(self):
        self.update()
        return self.background

    @property
    def image(self):
        return self.background

class Planet(object):
    def __init__(self):
        pass
