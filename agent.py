import random
import numpy as np
from keras import Sequential
from collections import deque
from keras.layers import Dense
import matplotlib.pyplot as plt
from keras.optimizers import adam

from my_game import *

env = my_game()
np.random.seed(0)


class DeepQNetwork:

    "Initialize a neural net below"

    def __init__(self, action_space, state_space):

        self.action_space = action_space        
        self.state_space = state_space
        self.epsilon = 1
        self.gamma = .95
        self.batch_size = 64
        self.epsilon_min = .01
        self.epsilon_decay = .990
        self.learning_rate = 0.001
        self.memory = deque(maxlen=100000)
        self.model = self.neural_net()

    def neural_net(self):

        model = Sequential()
        model.add(Dense(64, input_shape=(self.state_space,), activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_space, activation='linear'))
        model.compile(loss='mse', optimizer=adam(lr=self.learning_rate))
        return model

    def remember_values(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def take_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self):

        if len(self.memory) < self.batch_size:
            return

        small_batch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in small_batch])
        actions = np.array([i[1] for i in small_batch])
        rewards = np.array([i[2] for i in small_batch])
        next_states = np.array([i[3] for i in small_batch])
        dones = np.array([i[4] for i in small_batch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def train_network(no_of_episodes):

    loss = []
    agent = DeepQNetwork(3, 5)
    for n in range(no_of_episodes):
        state = env.reset()
        state = np.reshape(state, (1, 5))        
        episode_score = 0
        env.set_episode(n)
        max_steps = 2000
        for i in range(max_steps):
            action = agent.take_action(state)
            reward, next_state, done = env.step(action)
            episode_score += reward
            next_state = np.reshape(next_state, (1, 5))
            agent.remember_values(state, action, reward, next_state, done)
            state = next_state
            agent.replay()
            if done:
                print("Episode: {}/{}, Reward: {}".format(n,no_of_episodes, episode_score))
                break
        loss.append(episode_score)
    return loss


if __name__ == '__main__':
    no_of_episodes = 200
    loss = train_network(no_of_episodes)
    plt.plot([i for i in range(no_of_episodes)], loss)
    plt.xlabel('No of Episodes')
    plt.ylabel('Reward obtained')
    plt.show()