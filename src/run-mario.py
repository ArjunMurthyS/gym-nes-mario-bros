#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Lilian Besson (Naereen)
# https://github.com/Naereen/gym-nes-mario-bros
# MIT License https://lbesson.mit-license.org/
#
from __future__ import division, print_function  # Python 2 compatibility

import os
from collections import deque

import gym
from gym import wrappers
import nesgym
import numpy as np

from dqn.model import DoubleDQN, load_model, save_model
from dqn.utils import PiecewiseSchedule


dqn_model_name = "dqn"
dqn_model_name_file = dqn_model_name + '.h5'


def get_env():
    env = gym.make('nesgym/MarioBros-v0')
    env = nesgym.wrap_nes_env(env)
    expt_dir = '/tmp/mario/'
    env = wrappers.Monitor(env, os.path.join(expt_dir, "gym"), force=True)
    return env


def safe_save_model(dqn, dqn_model_name_file):
    try:
        save_model(dqn, dqn_model_name_file)
    except (ValueError, NotImplementedError, AttributeError):
        print("Unable to save the DQN model to file '{}'...".format(dqn_model_name_file))  # DEBUG


# Keep a log of the max score seen so far, to plot it as a function of time steps
def log_max_seen_score(step, max_seen_score):
    with open("max_seen_score.csv", 'a') as f:
        f.write("\n{}, {}".format(step, max_seen_score))


def mario_main():
    env = get_env()

    last_obs = env.reset()

    max_timesteps = 400000
    max_seen_score = 0

    # Create the log file if needed
    if not os.path.isfile("max_seen_score.csv"):
        with open("max_seen_score.csv", 'w') as f:
            f.write("step, max_seen_score")

    exploration_schedule = PiecewiseSchedule(
        [
            (0, 1.0),
            (1e5, 0.1),
            (max_timesteps / 2, 0.01),
        ], outside_value=0.01
    )

    dqn = None
    # How to save the DQN to a file after every training
    # in order to resume from previous step if training was stopped?
    if os.path.isfile(dqn_model_name_file):
        try:
            dqn = load_model(dqn_model_name_file)
            print("Successfully loaded the DQN model from file '{}'...".format(dqn_model_name_file))  # DEBUG
        except (ValueError, NotImplementedError, AttributeError):
            print("Unable to load the DQN model from file '{}'...".format(dqn_model_name_file))  # DEBUG
    if dqn is None:
        dqn = DoubleDQN(image_shape=(84, 110, 1),
                    num_actions=env.action_space.n,
                    # # XXX Heavy simulations
                    # training_starts=10000,
                    # target_update_freq=4000,
                    # training_batch_size=64,
                    # # XXX light simulations?
                    training_starts=5000,
                    target_update_freq=100,
                    training_batch_size=4,
                    # Other parameters...
                    frame_history_len=4,
                    replay_buffer_size=100000,  # XXX reduce if MemoryError
                    exploration=exploration_schedule
                )

    reward_sum_episode = 0
    num_episodes = 0
    episode_rewards = deque(maxlen=100)

    for step in range(max_timesteps):
        if step > 0 and step % 100 == 0:
            print("step: ", step,
                  "; episodes:", num_episodes,
                  "; epsilon:", exploration_schedule.value(step),
                  "; learning rate:", dqn.get_learning_rate(),
                  "; last 100 training loss mean", dqn.get_avg_loss()
            )
            if len(episode_rewards) > 0:
                print("last 100 episode mean rewards: ", np.mean(np.array(episode_rewards)))
            # also print summary of the model!
            dqn.summary()
            # and save the model!
            safe_save_model(dqn, dqn_model_name_file)

        # XXX Enable this to see the Python view of the screen (PIL.imshow)
        # env.render()

        action = dqn.choose_action(step, last_obs)
        obs, reward, done, info = env.step(action)
        reward_sum_episode += reward
        if done and reward < 0:
            reward = 0  # force this manually to avoid bug of getting -400 10 times in a row!
        dqn.learn(step, action, reward, done, info)

        print("Step {:>6}, action {}, gave reward {:>6}, score {:>6} and max score {:>6}, life {:>2} and level {:>2}.".format(step, action, reward, info['score'], max_seen_score, info['life'], info['level']))  # DEBUG

        if info['score'] > max_seen_score:
            max_seen_score = info['score']
            print("!!New total score record!!", max_seen_score)
            log_max_seen_score(step, max_seen_score)
        if done:
            last_obs = env.reset()
            if info['frame'] > 0:  # we actually played a few frames
                print("\ndone, reward_sum_episode =", reward_sum_episode)
                episode_rewards.append(reward_sum_episode)
                reward_sum_episode = 0
                num_episodes += 1
        else:
            last_obs = obs

        last_obs = obs

if __name__ == "__main__":
    mario_main()
