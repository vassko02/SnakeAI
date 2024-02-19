import pygame
import random
from enum import Enum
from collections import namedtuple
pygame.init()

#irányok beállítása
class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4

Point=namedtuple('Point','x','y')

BLOCK_SIZE=20

class SnakeGame:
    def __init__(self,w=640,h=480):
        self.w=w
        self.h=h

        #ablak létrehozása
        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('SnakeAI')
        self.clock=pygame.time.Clock()

        self.direction=Direction.UP

        self.head=Point(self.w/2,self.h/2)
        self.snake=[self.head,Point(self.head.x,self.head.y-BLOCK_SIZE),Point(self.head.x,self.head.y-(2*BLOCK_SIZE))]

        self.score=0
        self.food=None
        self._place_food()

    #étel helyének randomizálása
    def _place_food(self):
        x=random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y=random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food=Point(x,y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self):
        pass

if __name__=='__main__':
    game=SnakeGame()

    #játék loop
    while True:
        game.play_step()


    pygame.quit()