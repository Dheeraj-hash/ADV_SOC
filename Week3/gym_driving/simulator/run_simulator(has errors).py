from importlib.resources import path
from gym_driving.assets.car import *
from gym_driving.envs.environment import *
from gym_driving.envs.driving_env import *
from gym_driving.assets.terrain import *

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import numpy as np
import time
import pygame, sys
from pygame.locals import *
import random
import math
import argparse
import numpy as np

# Do NOT change these values
TIMESTEPS = 1000
FPS = 30
NUM_EPISODES = 10

class Task1():

    def __init__(self):
        """
        Can modify to include variables as required
        """
        # x=random.randint(-300,300)
        # y=random.randint(-300,300)
        value_matrix=np.zeros((72**2)*11)

        for num in range(0,100):

            state_matrix=np.zeros((72**2)*11)
            simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath='../configs/config.json')
            state,info_dict=simulator.environment.get_state()
            x,y,vel,angle=state[0],state[1],state[2],state[3]
            terminate=False
            
            while True:
        # state,info_dict=simulator.environment.get_state()
        # x,y,vel,angle=state[0],state[1],state[2],state[3]

                new_state=[]
                value_list=[]
                value_max=-100000
                final_x,final_y=0,0
                print(x,y)
                for i in range(0,360,90):
                    new_x = x + 10*math.cos(i*math.pi/180)
                    new_y = y + 10*math.sin(i*math.pi/180)
                    # new_x=326.15966394
                    # new_y=-2.25426889
                    # print(new_x,new_y)
                    simulator.environment.set_state(new_x,new_y,vel,angle)
                    simulator.environment.update_state()
                    state,info_dict=simulator.environment.get_state()
                    terrain_collisions = info_dict['terrain_collisions']
                    for t in terrain_collisions:
                        print(t.texture)
                    done_ice = any([t.texture == 'ice' for t in terrain_collisions])
                    done_road = any([t.texture == 'road' for t in terrain_collisions])
                    if done_ice and not done_road:
                        reward = -100
                    if done_road:
                        print("Yes")
                        reward=100 
                        terminate = True
                        reached_road = True
                    else:
                        reward=-1
                        new_state.append([new_x,new_y])
                    for i in range(0,11):
                        index=(72**2)*i + math.floor((new_x+10-i)/10) + math.floor((new_y+10-i)/10)*72
                        state_matrix[index]=1
                    value = reward + np.dot(value_matrix,np.transpose(state_matrix))
                    value_list.append(value)
                    if value> value_max:
                        final_x,final_y=new_x,new_y
                        value_max=value
                    state_matrix=np.zeros((72**2)*11)

            
                for i in range(0,11):
                    index=(72**2)*i + math.floor((x+10-i)/10) + math.floor((y+10-i)/10)*72
                    state_matrix[index]=1

                value_final=max(value_list)
                value_matrix = value_matrix + (0.01/11)*(value_final - np.dot(value_matrix,np.transpose(state_matrix)))*state_matrix
                state_matrix=np.zeros((72**2)*11)
                value_list=[]
                print(value_final)
                if terminate == True:
                    break
                x,y=final_x,final_y
                
        self.value_matrix=value_matrix
        super().__init__()

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED
        """
        # edir= math.atan(state[1]/(state[0]-350)) * 180 / math.pi
        # if edir <0:
        #     edir=360 + edir
        # if state[3] - edir >=2 :
        #     action_steer=0
        #     action_acc=0
        # elif state[3] - edir <=-2:
        #     action_steer=2
        #     action_acc=0
        # else:
        #     action_steer=1
        #     action_acc=4
        state_matrix=np.zeros((72**2)*11)
        x,y,vel,angle=state[0],state[1],state[2],state[3]
        action_steer=[-3,0,3]
        action_acc=[-5,-3.95,0,3.95,5]
        final_steer,final_acc=0,0
        value=-100000
        for steer in range(3):
            for acc in range(5):

                angle1 = angle+action_steer[steer]
                angle1 %= 360.0
                acceleration = action_acc[acc]

                mu = 0.4
                acceleration = max(min(acceleration, 20 - vel), -vel) - mu*9.81
 
                if vel <= 0 and acceleration < 0.00001:
                    acceleration = 0

                t = 1
                dist = vel * t + 0.5 * acceleration * (t ** 2)

                if dist<0:
                    dist = 0

                dx = dist * np.cos(np.radians(angle1))
                dy = dist * np.sin(np.radians(angle1))
                new_x += dx
                new_y += dy
                for i in range(0,11):
                    index=(72**2)*i + math.floor((new_x+10-i)/10) + math.floor((new_y+10-i)/10)*72
                    state_matrix[index]=1
                if new_y > 350 or new_y < -350:
                    continue
                elif new_x > 350 and new_y>-150 and new_y<150:
                    final_steer=steer
                    final_acc=acc
                elif new_x < -350:
                    continue
                elif new_x>350:
                    continue
                new_value=-1 + np.dot(self.value_matrix,np.transpose(state_matrix))
                if new_value > value:
                    value = new_value
                    final_steer=steer
                    final_acc=acc
                 
        action = np.array([final_steer, final_acc])  

        return action

        # Replace with your implementation to determine actions to be taken
       

    def controller_task1(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
    
        ######### Do NOT modify these lines ##########
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath=config_filepath)

        time.sleep(3)
        ##############################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):
        
            ######### Do NOT modify these lines ##########
            
            # To keep track of the number of timesteps per epoch
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset()
            
            # Variable representing if you have reached the road
            road_status = False
            ##############################################

            # The following code is a basic example of the usage of the simulator
            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            # Writing the output at each episode to STDOUT
            print(str(road_status) + ' ' + str(cur_time))

class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED

        You can modify the function to take in extra arguments and return extra quantities apart from the ones specified if required
        """

        # Replace with your implementation to determine actions to be taken
        action_steer = None
        action_acc = None

        action = np.array([action_steer, action_acc])  

        return action

    def controller_task2(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ################ Do NOT modify these lines ################
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        time.sleep(3)
        ###########################################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):

            ################ Setting up the environment, do NOT modify these lines ################
            # To randomly initialize centers of the traps within a determined range
            ran_cen_1x = random.randint(120, 230)
            ran_cen_1y = random.randint(120, 230)
            ran_cen_1 = [ran_cen_1x, ran_cen_1y]

            ran_cen_2x = random.randint(120, 230)
            ran_cen_2y = random.randint(-230, -120)
            ran_cen_2 = [ran_cen_2x, ran_cen_2y]

            ran_cen_3x = random.randint(-230, -120)
            ran_cen_3y = random.randint(120, 230)
            ran_cen_3 = [ran_cen_3x, ran_cen_3y]

            ran_cen_4x = random.randint(-230, -120)
            ran_cen_4y = random.randint(-230, -120)
            ran_cen_4 = [ran_cen_4x, ran_cen_4y]

            ran_cen_list = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]            
            eligible_list = []

            # To randomly initialize the car within a determined range
            for x in range(-300, 300):
                for y in range(-300, 300):

                    if x >= (ran_cen_1x - 110) and x <= (ran_cen_1x + 110) and y >= (ran_cen_1y - 110) and y <= (ran_cen_1y + 110):
                        continue

                    if x >= (ran_cen_2x - 110) and x <= (ran_cen_2x + 110) and y >= (ran_cen_2y - 110) and y <= (ran_cen_2y + 110):
                        continue

                    if x >= (ran_cen_3x - 110) and x <= (ran_cen_3x + 110) and y >= (ran_cen_3y - 110) and y <= (ran_cen_3y + 110):
                        continue

                    if x >= (ran_cen_4x - 110) and x <= (ran_cen_4x + 110) and y >= (ran_cen_4y - 110) and y <= (ran_cen_4y + 110):
                        continue

                    eligible_list.append((x,y))

            simulator = DrivingEnv('T2', eligible_list, render_mode=render_mode, config_filepath=config_filepath, ran_cen_list=ran_cen_list)
        
            # To keep track of the number of timesteps per episode
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset(eligible_list=eligible_list)
            ###########################################################

            # The following code is a basic example of the usage of the simulator
            road_status = False

            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            print(str(road_status) + ' ' + str(cur_time))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config filepath", default=None)
    parser.add_argument("-t", "--task", help="task number", choices=['T1', 'T2'])
    parser.add_argument("-r", "--random_seed", help="random seed", type=int, default=0)
    parser.add_argument("-m", "--render_mode", action='store_true')
    parser.add_argument("-f", "--frames_per_sec", help="fps", type=int, default=30) # Keep this as the default while running your simulation to visualize results
    args = parser.parse_args()

    config_filepath = args.config
    task = args.task
    random_seed = args.random_seed
    render_mode = args.render_mode
    fps = args.frames_per_sec

    FPS = fps

    random.seed(random_seed)
    np.random.seed(random_seed)

    if task == 'T1':
        
        agent = Task1()
        agent.controller_task1(config_filepath=config_filepath, render_mode=render_mode)

    else:

        agent = Task2()
        agent.controller_task2(config_filepath=config_filepath, render_mode=render_mode)
