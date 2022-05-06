import pygame
import sys
from pygame.locals import *
import os
import random
from gym import Env
from gym.spaces import Discrete,Box
import numpy as np
import random

class PongEnv(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}
    state= 325+ random.randint(-7,7)
    def __init__(self) -> None:
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.light_grey = (64,64,64)
        self.lighter_grey = (32,32,32)
        self.FPS = 90
        self.VEL = 10
        self.LEFTPADDLE_WIDTH =10
        self.LEFTPADDLE_HEIGHT =100
        self.RIGHTPADDLE_WIDTH = 10
        self.RIGHTPADDLE_HEIGHT =100
        self.BALL_WIDTH = 25
        self.BALL_HEIGHT = 25
        self.ballspeed_x = 5
        self.ballspeed_y = 5
        self.count = 0
        self.speedconstant = 1
        #Actions we can take: up,down
        self.action_space = Discrete(2)
        #Y axis array
        self.observation_space = Box(low=np.array([0]),high=np.array([100]))
        #start position
        #Game Length
        self.game_length = 60
        #Paddle image and scale
        self.PONGPADDLE_LEFT = pygame.image.load(os.path.join('images','Pongpaddleblue.png'))
        self.PONGPADDLE_LEFT = pygame.transform.scale(self.PONGPADDLE_LEFT,(self.LEFTPADDLE_WIDTH,self.LEFTPADDLE_HEIGHT))
        self.PONGPADDLE_RIGHT = pygame.image.load(os.path.join('images','Pongpaddlered.png'))
        self.PONGPADDLE_RIGHT = pygame.transform.scale(self.PONGPADDLE_RIGHT,(self.RIGHTPADDLE_WIDTH,self.RIGHTPADDLE_HEIGHT))
        self.score_time = None
        self.bgimage = pygame.image.load(os.path.join('images','bgimage.jpg'))
        #Ball image and scale
        self.BALL = pygame.image.load(os.path.join('images','ball.png'))
        self.BALL = pygame.transform.scale(self.BALL,(self.BALL_WIDTH,self.BALL_HEIGHT))
        #Text variables
        self.left_score = 0
        self.right_score = 0
        self.screen_width = 1000
        self.screen_height =650
        self.ball = pygame.Rect(self.screen_width/2 + 12.5,self.screen_height/2 + 12.5,self.BALL_WIDTH,self.BALL_HEIGHT)
        self.left = pygame.Rect(30,250,self.LEFTPADDLE_WIDTH,self.LEFTPADDLE_HEIGHT)
        self.right = pygame.Rect(960,250,self.RIGHTPADDLE_WIDTH,self.RIGHTPADDLE_HEIGHT)
        self.screen = None
        self.clock = None
        self.isopen = True
    def step(self,action):
        #Apply action
        if action == 1:
            self.state += 7
            if (self.right.y - self.state) <0:
                reward = 1
            else:
                reward = -1
        elif action == 0:
            self.state -= 7
            if (self.right.y - self.state) >0:
                reward = 1
            else:
                reward = -1
        #Reduce game length
        #Calculate Reward
        #check if game has ended
        if self.left_score == 3:
            done = True
        else:
            done = False
        

        info = {}

        return self.state,reward,done,info
        
    def render(self,mode="human"):
        import pygame
        pygame.font.init()
        pygame.init()
        global score_time
        pygame.display.set_caption("Pong")
        #screen settings
        score_time = None
        global ballspeed_y
        global ballspeed_x
        
        if self.state is None:
            return None
        
        x = self.state
        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        if self.clock is None:
            self.clock = pygame.time.Clock()
        
        self.ball_movement(self.ball)
        if score_time:
            self.start()
        self.keys_pressed = pygame.key.get_pressed()
        self.left_movement(self.keys_pressed,left=self.left)
        self.right_movement(self.keys_pressed,right=self.right)
        if mode == "human":
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])
            self.draw_window(self.left,self.right,self.ball,self.left_score,self.right_score,self.screen)
            pygame.display.flip()
        if mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )
        elif self.left_score == 3:
            self.close()
            return self.isopen

    def close(self):
        if self.screen is not None:
            import pygame
            pygame.QUIT
            self.isopen = False
            
    def draw_window(self,left, right,ball,left_score,right_score,screen):
        import pygame
        screen.blit(self.bgimage,(0,0))
        if score_time:
            self.start()

        #screen.blit(lefttext,(self.screen_width/2 -200,50))
        #screen.blit(righttext,(self.screen_width/2 +150,50))
        screen.blit(self.PONGPADDLE_LEFT,(left.x,left.y))
        screen.blit(self.PONGPADDLE_RIGHT,(right.x,right.y))
        print(right.y)
        screen.blit(self.BALL,(ball.x,ball.y))
        
        
        pygame.display.update()

    def left_movement(self,keys_pressed,left):
        if keys_pressed[pygame.K_w] and left.y - self.VEL > -1: 
            left.y -= self.VEL
        if keys_pressed[pygame.K_s] and left.y + self.VEL < 651 - self.LEFTPADDLE_HEIGHT:
            left.y += self.VEL

    def right_movement(self,keys_pressed,right):
        if keys_pressed[pygame.K_UP] and right.y - self.VEL > -1:
                right.y -= self.VEL
        if keys_pressed[pygame.K_DOWN] and right.y + self.VEL < 651 - self.RIGHTPADDLE_HEIGHT:
                right.y += self.VEL
        right.y = self.state

    def ball_movement(self,ball):
        global score_time,before_goal
        ball.x += self.ballspeed_x
        ball.y += self.ballspeed_y
        if ball.top <= 0 or ball.bottom >= self.screen_height:
            self.ballspeed_y *= -1
        if ball.left <= 30:
            before_goal = ball.y
            self.right_score += 1
            score_time = pygame.time.get_ticks()
            
        if ball.right >= 970:
            before_goal = ball.y
            self.left_score +=1
            score_time = pygame.time.get_ticks()
           

        if ball.colliderect(self.left) or ball.colliderect(self.right):
            self.ballspeed_x *= -1
            self.count += 1
            if self.count == 10:
                self.speedconstant += 0.01     
                self.ballspeed_x *= self.speedconstant
                self.ballspeed_y *= self.speedconstant     
            elif self.count == 20:
                self.speedconstant += 0.02
                self.ballspeed_x *= PongEnv.speedconstant
                self.ballspeed_y *= PongEnv.speedconstant     
            elif self.count ==25:
                self.speedconstant += 0.03
                self.ballspeed_x *= PongEnv.speedconstant
                self.ballspeed_y *= PongEnv.speedconstant     
            elif self.count == 30:
                self.speedconstant += 0.1
                self.ballspeed_x *= PongEnv.speedconstant
                self.ballspeed_y *= PongEnv.speedconstant     
            elif self.count == 35:
                self.speedconstant += 0.3
                self.ballspeed_x *= PongEnv.speedconstant
                self.ballspeed_y *= PongEnv.speedconstant     

    def start(self,):
        global ballspeed_x,ballspeed_y,score_time
        current_time = pygame.time.get_ticks()
        self.ball.center = (self.screen_width/2, self.screen_height/2)

        #if current_time - score_time < 700:
        #    three = self.game_font.render("3",1,self.BLACK)
        #    screen.blit(three,(self.screen_width/2- 25,self.screen_height/2))
        #elif current_time - score_time < 1400:
        #    two = self.game_font.render("2",1,self.BLACK)
        #    screen.blit(two,(self.screen_width/2-25,self.screen_height/2))
        #elif current_time - score_time < 2100:
        #    one = self.game_font.render("1",1,self.BLACK)
        #    screen.blit(one,(self.screen_width/2-25,self.screen_height/2))
        if current_time - score_time < 2100:
            ballspeed_x = 0
            ballspeed_y = 0
        else:
            ballspeed_x = 5* random.choice((1,-1)) * self.speedconstant
            ballspeed_y = 5* random.choice((1,-1)) * self.speedconstant
            score_time = None

    
    def reset(self):
        self.state= 325 + random.randint(-3,3)
        self.game_length = 60
        return self.state

if __name__ == "__main__":
    PongEnv.render()
