"""程序入口"""
import pygame
import sys

from core import App

if __name__ == "__main__":
    m = App()
    t = m.run()
    print(t)
    pygame.quit()
    sys.exit(0)