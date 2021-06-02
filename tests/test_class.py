import os
import sys
sys.path.append(os.path.normpath(os.path.join
                (os.path.dirname(os.path.abspath(__file__)), '..')))

from src.game import Game

WIDTH = 800
HEIGHT = 650
FPS = 30

play = Game(WIDTH, HEIGHT, FPS)
play.mainloop()
play.quit()
