#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : utils.py
# Create date : 2019-10-20 20:20
# Modified date : 2019-10-20 21:05
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

import numpy as np
import torch
import shutil
import torch.autograd as Variable

def soft_update(target, source, tau):
    for target_param, param in zip(target.parameters(), source.parameters()):
        target_param.data.copy_(
            target_param.data*(1.0-tau) + param.data*tau
            )


def hard_update(target, source):
    for target_param, param in zip(target.parameters(), source.parameters()):
        target_param.data.copy_(param.data)


def save_training_checkpoint(state, is_best, episode_count):
    filename = str(episode_count) + 'checkpoint.path.rar'
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, 'model_best.pth.tar')

class OrnsteinUhlenbeckActionNoise:
    def __init__(self, action_dim, mu=0, theta=0.15, sigma=0.2):
        self.action_dim = action_dim
        self.mu = mu
        self.theta = theta
        self.sigma = sigma
        self.X = np.ones(self.action_dim) * self.mu

    def reset(self):
        self.X = np.ones(self.action_dim) * self.mu

    def sample(self):
        #dx = self.theta *(self.mu - self.X)
        dx = self.theta * (self.mu - self.X)

        dx = dx + self.sigma * np.random.randn(len(self.X))
        self.X = self.X + dx
        return self.X

