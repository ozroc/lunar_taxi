#!/usr/bin/env python

import pygame
import math
try:
    import android
except ImportError:
    android = None


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


class Controls(object):
    def __init__(self, android):
        self.__android = android
        self.__instant_presses=0
        self.__pressed=False
        try:
            self.__android.init()
            self.__android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
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
        offset = math.pi/2 if x < 0 else 0
        if x != 0:
            return math.atan(y/x)+offset
        else:
            return 0
    
    def __get_angle_pc(self):
        accs = pygame.mouse.get_pos()
        x = accs[0]-400.
        y = accs[1]-240.
        if x != 0:
            return abs(x)/x*math.atan(y/x)
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
    def __init__(self):
        pass

class Planet(object):
    def __init__(self):
        pass
