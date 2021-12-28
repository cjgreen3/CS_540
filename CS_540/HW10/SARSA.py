from collections import deque
import gym
import random
import numpy as np
import time
import pickle

from collections import defaultdict


EPISODES =   20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999



def default_Q_value():
    return 0


if __name__ == "__main__":




    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v0")
    env.seed(1)
    env.action_space.np_random.seed(1)


    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.

    episode_reward_record = deque(maxlen=100)


    for i in range(EPISODES):
        # episode_reward = 0
       
        #TODO perform SARSA learning
        obs = env.reset()
        done = False
        total_reward = 0
        prev_reward = None
        prev_state = None
        prev_action = None
        while done == False:
            s = obs
            if random.uniform(0, 1) < EPSILON:
                action = env.action_space.sample()
            else:
                prediction = np.array([Q_table[(obs, i)] for i in range(env.action_space.n)])
                action = np.argmax(prediction)
            obs, reward, done, info = env.step(action)
            total_reward += reward

            # new_state = np.array([Q_table[(obs, i)] for i in range(env.action_space.n)])

            if prev_state is None:
                prev_reward = reward
                prev_state = s
                prev_action = action
                continue
            if done == True:
                episode_reward_record.append(total_reward)
                # Q_table[(s, action)] = s + LEARNING_RATE(prev_reward-s)
                Q_table[(s,action)] = Q_table[(s,action)] + LEARNING_RATE*(reward-Q_table[(s,action)])


            else:
                # Q_table[(s, action)] = Q_table[(s, action)] + LEARNING_RATE * (
                #         reward + DISCOUNT_FACTOR * s - Q_table[(s, action)])
                Q_table[(prev_state, prev_action)] = Q_table[(prev_state, prev_action)] + LEARNING_RATE * (
                         prev_reward + DISCOUNT_FACTOR * Q_table[(s,action)] - Q_table[(prev_state, prev_action)])

            prev_reward = reward
            prev_state = s
            prev_action = action

        EPSILON *= EPSILON_DECAY


        if i%100 ==0 and i>0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    ####DO NOT MODIFY######
    model_file = open('SARSA_Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    #######################



