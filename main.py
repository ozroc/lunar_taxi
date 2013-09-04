#!/usr/bin/env python

import pygame

try:
    import android
except ImportError:
    android = None

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer

def main():
    if android:
        android.init()
        android.accelerometer_enable(True)
    pygame.init()

if __name__ == '__main__':
    main()