# Defines the Actor and Critic NN models for use in the Tennis project.
#
# This code is a copy of the model used for my continuous control (Reacher) project.
#
# This code is a slight modification from code provided by the Udacity instructor team.
#

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

def hidden_init(layer):
    """Define a tuple with the range of values desired for initialization of the hidden layer."""

    fan_in = layer.weight.data.size()[0]
    lim = 1. / np.sqrt(fan_in)
    return (-lim, lim)


class Actor(nn.Module):
    """Actor (Policy) Model."""

    def __init__(self, state_size, action_size, seed, fc1_units=256, fc2_units=128):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
            fc1_units (int): Number of nodes in first hidden layer
            fc2_units (int): Number of nodes in second hidden layer
        """
        super(Actor, self).__init__()
        self.fc1 = nn.Linear(state_size, fc1_units)
        self.fc2 = nn.Linear(fc1_units, fc2_units)
        self.fc3 = nn.Linear(fc2_units, action_size)
        self.dropout = nn.Dropout(0.2)
        self.reset_parameters()

    def reset_parameters(self):
        """Initialize all of the network's parameters."""

        self.fc1.weight.data.uniform_(*hidden_init(self.fc1))
        self.fc2.weight.data.uniform_(*hidden_init(self.fc2))
        self.fc3.weight.data.uniform_(-3e-3, 3e-3)

    def forward(self, state):
        """Build an actor (policy) network that maps states -> actions."""

        x = F.relu(self.fc1(state))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        return F.tanh(self.fc3(x))


class Critic(nn.Module):
    """Critic (Value) Model."""

    def __init__(self, state_size, action_size, seed, fcs1_units=256, fc2_units=128):
        """Initialize parameters and build model.
           Params:
               state_size (int):  number of values for all agents' state vectors
               action_size (int): number of values for all agents' action vectors
               seed (int):        random seed
               fcs1_units (int):  number of nodes in the first hidden layer
               fc2_units (int):   number of nodes in the second hidden layer

           Note: for the critic we concatenate all agents' states & actions, so the
           state_size and action_size include features for all agents.
        """
        super(Critic, self).__init__()
        self.fcs1 = nn.Linear(state_size, fcs1_units)
        self.fc2 = nn.Linear(fcs1_units + action_size, fc2_units)
        self.fc3 = nn.Linear(fc2_units, 1)
        self.dropout = nn.Dropout(0.2)
        self.reset_parameters()

    def reset_parameters(self):
        """Initialize all of the network's parameters."""

        self.fcs1.weight.data.uniform_(*hidden_init(self.fcs1))
        self.fc2.weight.data.uniform_(*hidden_init(self.fc2))
        self.fc3.weight.data.uniform_(-3e-3, 3e-3)

    def forward(self, state, action):
        """Build a critic (value) network that maps (state, action) pairs -> Q-values."""

        xs = F.leaky_relu(self.fcs1(state))
        xs = self.dropout(xs)
        x = torch.cat((xs, action), dim=1)
        x = F.leaky_relu(self.fc2(x))
        x = self.dropout(x)
        return self.fc3(x)
