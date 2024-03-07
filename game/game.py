import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font=pygame.font.Font('arial.ttf',20)

#irányok beállítása
class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4

Point=namedtuple('Point','x,y')

BLOCK_SIZE=20
SPEED=10

GREEN=(125,255,50)

WHITE=(255,255,255)
WHITE2=(228,228,228)
BLACK=(0,0,0)

BLUE1=(0,100,255)
BLUE2=(0,0,255)

class SnakeGameAI:
    def __init__(self,w=640,h=480):
        self.w=w
        self.h=h

        #ablak létrehozása
        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('SnakeAI')
        self.clock=pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction=Direction.RIGHT

        self.head=Point(self.w/2,self.h/2)
        self.snake=[self.head,Point(self.head.x-BLOCK_SIZE,self.head.y),Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]

        self.score=0
        self.food=None

        self._place_food()
        self.frame_iteration=0

    #étel randomizálása
    def _randomize_food(self):
        colorint=random.randint(0,3)
        match colorint:
            case 0:
                self.ftype='images/apple.png'
            case 1:
                self.ftype='images/lemon.png'
            case 2:
                self.ftype='images/orange.png'
            case 3:
                self.ftype='images/plum.png'
        self.f=pygame.image.load(self.ftype)
        self.foodtype= pygame.transform.scale(self.f, (BLOCK_SIZE*1.25,BLOCK_SIZE*1.25))

    #étel helyének randomizálása
    def _place_food(self):
        self._randomize_food()
        x = random.randint(1, (self.w-2*BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(1, (self.h-2*BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food=Point(x,y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self,action):  
        self.frame_iteration+=1

        #bemenet kezelése
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        #mozgás
        self._move(action)
        self.snake.insert(0,self.head)

        #játék végének vizsgálata
        reward=0
        game_over=False
        if self.is_collision() or self.frame_iteration>70*len(self.snake): #ha egy ideig nem történik semmi akkor is reset
            game_over=True
            reward= -10
            return reward, game_over,self.score

        #új étel vagy mozgás
        if self.head== self.food:
            self.score+=1   
            reward =10  
            self._place_food()
        else:
            self.snake.pop()

        #ui frissités
        self._update_ui()

        #sebesség növelése
        self.clock.tick(SPEED+self.score)

        #játék vége
        return reward, game_over,self.score
    
    def is_collision(self,pt=None):
        if pt is None:
            pt=self.head

        #falba ütközés
        if pt.x > self.w - 2*BLOCK_SIZE or pt.x < BLOCK_SIZE or pt.y > self.h - 2*BLOCK_SIZE or pt.y < BLOCK_SIZE:
            return True
        
        #magába ütközés
        if pt in self.snake[1:]:
            return True
        return False
        
    def _update_ui(self):
        self.display.fill(GREEN)

        #keret rajzolása
        for x in range(0,self.w,BLOCK_SIZE):
            for y in range(0,self.h,BLOCK_SIZE):
                pt=Point(x,y)
                if x==0 or x==self.w-BLOCK_SIZE or y==0 or y==self.h-BLOCK_SIZE:
                    pygame.draw.rect(self.display,WHITE2,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
                    pygame.draw.rect(self.display,WHITE,pygame.Rect(pt.x+2,pt.y+2,14,14))

        #kígyó rajzolása             
        idx=0
        for pt in self.snake:
            if idx==0:
                pygame.draw.rect(self.display,BLUE2,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
                pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x+4,pt.y+4,12,12))
            else:
                pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
                pygame.draw.rect(self.display,BLUE2,pygame.Rect(pt.x+4,pt.y+4,12,12))
            idx+=1

        #étel rajzolása
        pygame.draw.rect(self.display,GREEN,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        self.display.blit(self.foodtype,(self.food.x-0.125*BLOCK_SIZE,self.food.y-0.125*BLOCK_SIZE))

        #szöveg kírása az ablak tetejére
        text=font.render("Pontszám: "+str(self.score),True,BLACK)
        self.display.blit(text,[0,0])
        pygame.display.flip()

    def _move(self,action):

        # [egyenes, jobb, bal]
        clock_wise=[Direction.RIGHT,Direction.DOWN,Direction.LEFT,Direction.UP]
        idx=clock_wise.index(self.direction)

        if np.array_equal(action,[1,0,0]):
            new_dir=clock_wise[idx] #nincs irányváltás
        elif np.array_equal(action,[0,1,0]):
            next_idx=(idx+1)%4
            new_dir=clock_wise[next_idx] #jobbra fordulás
        else: 
            next_idx=(idx-1)%4
            new_dir=clock_wise[next_idx] #balra fordulás
        self.direction=new_dir
        
        x=self.head.x
        y=self.head.y
        if self.direction==Direction.RIGHT:
            x+=BLOCK_SIZE
        elif self.direction==Direction.LEFT:
            x-=BLOCK_SIZE
        elif self.direction==Direction.UP:
            y-=BLOCK_SIZE
        elif self.direction==Direction.DOWN:
            y+=BLOCK_SIZE
        self.head= Point(x,y)
