#!/usr/bin/env python

import pygame
import math
try:
    import android
except ImportError:
    android = None


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


class Controls(object):
    def __init__(self, android):
        self.__android = android
        self.__instant_presses=0
        self.__pressed=False
        try:
            self.__android.accelerometer_enable(True)
            self.__get_angle = self.__get_angle_android
        except:
            self.__get_angle = self.__get_angle_pc

    @property
    def angle(self):
        return self.__get_angle()

    @property
    def press(self):
        self.__get_presses()
        if self.__instant_presses > 0:
            return True
        else:
            return self.__pressed

    def __get_angle_android(self):
        accs = self.__android.accelerometer_reading()
        x = accs[1]
        y = accs[0]
        offset = math.pi if x < 0 else 0
        if x != 0:
            return offset-math.atan(y/x)
        else:
            return 0
    
    def __get_angle_pc(self):
        accs = pygame.mouse.get_pos()
        x = accs[0]-400.
        y = accs[1]-240.
        offset = math.pi if x < 0 else 0
        if x != 0:
            return offset-math.atan(y/x)
        else:
            return 0

    def __get_presses(self):
        self.__instant_presses = 0
        for ev in pygame.event.get():
            # Not sure if this is a good way to control when touch is holded
            if ev.type == pygame.MOUSEBUTTONDOWN:
                self.__pressed = True
                self.__instant_presses += 1
            if ev.type == pygame.MOUSEBUTTONUP:
                self.__pressed = False





class Starship(object):
    def __init__(self,screen,pos,vel):
        self.__screen=screen
        self.__pos=pos
        self.__vel=vel

    def update(self,control):
        if control.press():
            self.vel+=1



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
