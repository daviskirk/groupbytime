#!/usr/bin/env python

"""
Groupby handles.
"""

import pandas as pd
import numpy as np
try:
    import matplotlib as mpl
except ImportError as e:
    print(('matplotlib could not be imported. '
           'Some functions may not work correctly!'))


def since_last(index, freq='1h', unit=None):
    index = pd.DatetimeIndex(index)
    freq = pd.Timedelta(freq)
    freq_float = float(freq.value)
    index_i8 = index.asi8
    out = pd.to_timedelta(index_i8 - np.floor(index_i8/freq_float)*freq_float)
    if unit:
        unit = pd.Timedelta(unit)
        out = (out/unit)
    return out

# def get_timedelta_formatter(timedelta_index, format_str):
#     def format_index(i, pos):
#         return(i*pd.Timedelta(unit))

#     return mpl.ticker.FuncFormatter(format_index)

def plot_timedelta(df, *args, **kwargs):
    timedelta_index = df.index
    ax = df.reset_index().plot(*args, **kwargs)

    def format_index(i, pos):
        return(str(timedelta_index[i]))
    formatter = mpl.ticker.FuncFormatter(format_index)
    ax.xaxis.set_major_formatter(formatter)


def groupby_times(df, kind, unit=None):
    if True: #unit is not None:
        key_dict = {
            'weekly':since_last(df.index, '7D', unit),
            'daily':since_last(df.index, '1D', unit),
            'hourly':since_last(df.index, '1h', unit),
            'minutely':since_last(df.index, '1m', unit),
            'secondly':since_last(df.index, '1s', unit),
            'all':None
        }
        if kind not in key_dict:
            group_key = since_last(df.index, kind, unit)
        else:
            group_key = key_dict[kind]
    else:
        key_dict = {
            'yearly':(df.year, df.index.day, df.index.time),
            'monthly':(df.index.day, df.index.time),
            'weekly':(df.index.weekday, df.index.time),
            'daily':df.index.time,
            'hourly':since_last(df.index, '1h', '1m'),
            'minutely':since_last(df.index, '1m', '1s'),
            'secondly':since_last(df.index, '1s', '1ms'),
            'all':None
        }
        if kind not in key_dict:
            group_key = since_last(df.index, kind, '1s')
        else:
            group_key = key_dict[kind]
    grouped = df.groupby(group_key)
    return grouped


def demo():
    pd.date_range('2015-1-1 00:00', '2016-1-1 00:00', freq='1m')
    np.sin()

if __name__ == '__main__':
    sys.exit()
