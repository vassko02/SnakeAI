import torch 
import random
import numpy as np
from collections import deque
from game import SnakeGameAI,Point,Direction

MAX_MEMORY=100_000
BATCH_SIZE=1000
LR=0.001 #learning rate

class Agent:
    def __init__(self):
        self.n_games=0
        self.epsilon=0 #randomság
        self.gamma=0 #discount rate
        self.memory=deque(maxlen=MAX_MEMORY)
        self.model=None
        self.trainer=None
        
    def get_state(self,game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        #veszély vizsgálata
        state = [

            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            #mozgás iránya
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            game.food.x < game.head.x,  #étel balra
            game.food.x > game.head.x,  #étel jobbra
            game.food.y < game.head.y,  #étel fel
            game.food.y > game.head.y  #étel le
            ]

        return np.array(state, dtype=int)
        
    def remember(self,state,action,reward,next_state,done):
        self.memory.append(state,action,reward,next_state,done)

    def train_long_memory(self):
        pass

    def train_short_memory(self,state,action,reward,next_state,done):
        pass

    def get_action(self,state):
        pass

def train():
    plot_scores=[]
    plot_mean_scores=[]
    total_score=0
    record=0
    agent=Agent()
    game=SnakeGameAI()
    #game loop
    while True:
        state_old=agent.get_state(game)

        final_move=agent.get_action(state_old)

        reward,done,score=game.play_step(final_move)
        state_new= agent.get_state(game)
    
        agent.train_short_memory(state_old,final_move,reward,state_new,done)

        agent.remember(state_old,final_move,reward,state_new,done)

        if done:
            #hosszutavu memoria képzés
            game.reset()
            agent.n_games+=1
            agent.train_long_memory()
            if score>record:
                record=score
            print(agent.n_games,'. kör: Pont:', score, 'Rekord: ',record)



if __name__=='__main__':
    train()