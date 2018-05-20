#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 23:42:45 2018

This module gathers some chat dataframe log processing

@author: pierre
"""
#%%
import re
import datetime as dt


def count_occ_pattern(text, pattern):
    return len(re.findall(pattern, text))

def count_occurences_pattern_in_messages(df_logs, agg_fields, pattern):
    df_logs['nb_occ_pattern'] = df_logs['text'].apply(lambda x:count_occ_pattern(x,pattern))
    df_logs = df_logs.groupby(agg_fields, as_index=False).agg({'nb_occ_pattern':'sum'})    
    return df_logs

def get_simple_messages_count(df_logs, agg_fields):
    df_logs['count'] = 1
    return df_logs.groupby(agg_fields, as_index=False)[['count']].count()

def get_hour_from_ts(ts):
    date = dt.datetime.fromtimestamp(float(ts))
    return date.strftime('%H')

def get_messages_counts_by_hour(df_logs, agg_fields):
    df_logs['h'] = df_logs['ts'].apply(get_hour_from_ts)
    
    return get_simple_messages_count(df_logs, agg_fields + ['h'])
