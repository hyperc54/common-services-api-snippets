#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 22:42:12 2018

@author: pierre
"""

import sys
import os
sys.path.append(os.path.abspath(".."))
from api_keys import SLACK_API_KEY

from load_messages import SlackMessagesLoader
from simple_analytics import *

from utils import get_range_dates

import matplotlib.pyplot as plt
import seaborn as sns


#%% Global params
CHANNEL_IDS = ["G2B1GFDPS", "G2B1GFDPD"]
DAYS = get_range_dates("20180101", 5)

#%%
Loader = SlackMessagesLoader(SLACK_API_KEY)

#%%
df = Loader.get_df_logs(DAYS, CHANNEL_IDS)

#%%
df_grouped = get_simple_messages_count(df, ['real_name', 'd'])

#%%
sns.set(style="darkgrid")

# Draw a pointplot to show pulse as a function of three categorical factors
g = sns.factorplot(x="d", y="count", hue="real_name", data=df_grouped,
                   capsize=.2, aspect=.75)

#%%