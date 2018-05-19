#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 18:03:48 2017
This snippet gets a specific channel history and print ou some quick 
analytics from its users.
Some inspiration:
    https://github.com/belgort/python-slack-example/blob/master/slack_demo.py
List of methods to call:
    https://api.slack.com/methods
@author: pierre
"""

#%% Global parameters
CHANNEL_ID = 'G2B1GFDPS'

#%% Imports
import sys
import os
sys.path.append(os.path.abspath("../.."))

from slackclient import SlackClient
from api_keys import SLACK_API_KEY
import matplotlib.pyplot as plt

#%% Create api client
sc = SlackClient(SLACK_API_KEY)

#%% Get channels history
history = sc.api_call('groups.history',
                      channel = CHANNEL_ID,
                      count=1000,
                      pretty=1)

#%% Allocate messages to user(_id)
user_msg = {}
b=0
for msg in history['messages']:
    try:
        if msg['user'] in user_msg:
            user_msg[msg['user']].append(msg['text'])
        else:
            user_msg[msg['user']]=[msg['text']]
    except KeyError:
        b=b+1

print('{} messages without user or text'.format(str(b)))
        
#%% Get real names
user_formatted = {}

for user_id in user_msg:
    user_info = sc.api_call('users.info', user=user_id, pretty=1)
    try:
        user_formatted[user_info['user']['real_name']] = user_msg[user_id]
    except KeyError:
        user_formatted[user_id]=user_msg[user_id]
    
#%% Plot amount per user
    
x = []
y = []

for key in user_formatted:
    x.append(key)
    y.append(len(user_formatted[key]))
    
plt.bar(range(len(y)),y)
plt.xticks(range(len(y)), x,rotation='vertical')