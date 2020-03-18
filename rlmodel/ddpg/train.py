#!/usr/bin/python
# -*- coding: utf-8 -*-
######################################
# File name : train.py
# Create date : 2019-10-20 19:59
# Modified date : 2020-01-09 00:04
# Author : liuzy
# Describe : not set
# Email : lzygzh@126.com
######################################

from __future__ import division
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

import numpy as np
import math

from . import utils
from . import model

BATCH_SIZE = 128
LEARNING_RATE = 0.001
GAMMA = 0.99
TAU = 0.001


class Trainer:
    def __init__(self, state_dim, action_dim, action_lim, ram, dev, write_loss, epoch=0, model_save_path=None):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.action_lim = action_lim
        self.ram = ram
        self.iter = 0
        self.noise = utils.OrnsteinUhlenbeckActionNoise(self.action_dim)
        self.device = dev
        self.write_loss = write_loss

        self.actor = model.Actor(self.state_dim, self.action_dim, self.action_lim).to(self.device)
        self.target_actor = model.Actor(self.state_dim, self.action_dim, self.action_lim).to(self.device)
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), LEARNING_RATE)

        self.critic = model.Critic(self.state_dim, self.action_dim).to(self.device)
        self.target_critic = model.Critic(self.state_dim, self.action_dim).to(self.device)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), LEARNING_RATE)

        if epoch > 0:
            self.load_models(epoch, model_save_path)

        utils.hard_update(self.target_actor, self.actor)
        utils.hard_update(self.target_critic, self.critic)

    def get_exploitation_action(self, state):
        state = Variable(torch.from_numpy(state).to(self.device))
        action = self.target_actor.forward(state).detach()
        return action.data.cpu().numpy()

    def get_exploration_action(self, state):
        state = Variable(torch.from_numpy(state).to(self.device))
        action = self.actor.forward(state).detach()
        new_action = action.data.cpu().numpy() + (self.noise.sample() * self.action_lim)
        return new_action

    def optimize(self, step):
        s1, a1, r1, s2 = self.ram.sample(BATCH_SIZE)
        s1 = Variable(torch.from_numpy(s1).to(self.device))
        a1 = Variable(torch.from_numpy(a1).to(self.device))
        r1 = Variable(torch.from_numpy(r1).to(self.device))
        s2 = Variable(torch.from_numpy(s2).to(self.device))

        a2 = self.target_actor.forward(s2).detach()
        next_val = torch.squeeze(self.target_critic.forward(s2, a2).detach())
        y_expectd = r1 + GAMMA * next_val

        y_predicted = torch.squeeze(self.critic.forward(s1, a1))

        loss_critic = F.smooth_l1_loss(y_predicted, y_expectd)
        self.critic_optimizer.zero_grad()
        self.write_loss(step, loss_critic.item(), "loss_critic")
        loss_critic.backward()
        self.critic_optimizer.step()

        pred_a1 = self.actor.forward(s1)
        loss_actor = -1 * torch.sum(self.critic.forward(s1, pred_a1))
        self.actor_optimizer.zero_grad()
        self.write_loss(step, loss_actor.item(), "loss_actor")
        loss_actor.backward()
        self.actor_optimizer.step()

        utils.soft_update(self.target_actor, self.actor, TAU)
        utils.soft_update(self.target_critic, self.critic, TAU)

    def get_models_path(self):
        return "./"

    def save_model(self, episode_count, model_save_path=None):
        # torch.save(self.target_actor.state_dict(), './Models/' + str(episode_count) + '_actor.pt')
        if model_save_path == None:
            model_save_path = self.get_models_path()
        # torch.save(self.target_actor.state_dict(), self.get_models_path() + str(episode_count) + '_actor.pt')
        torch.save(self.target_actor.state_dict(), model_save_path + str(episode_count) + '_actor.pt')
        # torch.save(self.target_critic.state_dict(), self.get_models_path() + str(episode_count) + '_critic.pt')
        torch.save(self.target_critic.state_dict(), model_save_path + str(episode_count) + '_critic.pt')
        print('%s Models saved successfully' % episode_count)

    def load_models(self, episode, model_save_path=None):
        if model_save_path == None:
            model_save_path = self.get_models_path()
        # self.critic.load_state_dict(torch.load(self.get_models_path() + str(episode) + '_critic.pt'))
        self.critic.load_state_dict(torch.load(model_save_path + str(episode) + '_critic.pt'))
        # self.actor.load_state_dict(torch.load(self.get_models_path() + str(episode) + '_actor.pt'))
        self.actor.load_state_dict(torch.load(model_save_path + str(episode) + '_actor.pt'))
        utils.hard_update(self.target_actor, self.actor)
        utils.hard_update(self.target_critic, self.critic)
        print("Models loaded successfully")
