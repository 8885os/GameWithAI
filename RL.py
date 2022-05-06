import gym
import random
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense,Flatten
from keras.models import Sequential
from keras.optimizer_v2.adam import Adam
from rl.agents import DQNAgent#agent that trains the model
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory#maintains memory for DQN
from pong import PongEnv
import pygame
from pygame.locals import *

env = PongEnv()

episodes = 10000
for episode in range(1,episodes+1):
    state = env.reset()
    done = False
    score = 0

    while not done:
        
        #env.render()
        action = env.action_space.sample()
        n_state,reward,done,info = env.step(action)
        score+=reward
    print('Episode:{} Score: {}'.format(episode,score))
states = env.observation_space.shape
actions = env.action_space.n
def build_model(states,actions):
    model = Sequential()#instantiate sequential model
    #model.add(Flatten(input_shape=(1,states)))#flatten node with a flat node that has 4 states 
    model.add(Dense(24, activation='relu',input_shape=states))#2 dense nodes
    model.add(Dense(24, activation='relu'))#to start building out the deep learning model
    model.add(Dense(actions, activation='linear'))#last dense node with actions
    #determines actions at the bottom based on states at the top
    return model
model =build_model(states,actions)#
model.summary()

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model,memory=memory,policy=policy,nb_actions=actions,nb_steps_warmup=10,target_model_update=1e-2)
    return dqn

dqn =  build_agent(model,actions)
dqn.compile(Adam(lr=1e-3),metrics=['mae'])
#dqn.fit(env,nb_steps=50000,visualize=False,verbose=1)
#dqn.load_weights('dqn_weights.h5f')
dqn.load_weights('dqn_weights.h5f')
dqn.test(env,nb_episodes=10000,visualize=True)