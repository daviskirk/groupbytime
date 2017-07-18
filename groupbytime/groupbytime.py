#!/usr/bin/env python

"""groupbytime assists pandas grouping by providing an easier to grouping
DataFrames and Series by timedeltas and periods.

"""

import pandas as pd

try:
    import matplotlib as mpl
except ImportError as e:
    mpl = None


def since_last(index, freq='H', unit=None, ambiguous='infer'):
    """returns an index indicating the time since the last occurrence of a
    frequency.

    Parameters
    ----------
    index : `pandas.DatetimeIndex`
    freq : `str`
        passed to `pandas.DatetimeIndex.to_period`
    unit : `pandas.Timedelta`
        If given, returns the output Index as a float index instead by dividing
        the timedelta index by the unit given.
    ambiguous : `str`
        passed to `pandas.DatetimeIndex.tz_localize`

    Returns
    -------
    `pandas.DatetimeIndex`

    """

    since = index.to_period(freq).to_timestamp(how='s')
    out = pd.TimedeltaIndex(index.tz_localize(None).values - since.values)
    if unit:
        unit = pd.Timedelta(unit)
        out = (out/unit)
    return out


def plot_timedelta(df, *args, **kwargs):
    if mpl is None:
        raise ImportError('matplotlib is needed for "plot_timedelta"')
    timedelta_index = df.index
    ax = df.reset_index().plot(*args, **kwargs)

    def format_index(i, pos):
        try:
            return(str(timedelta_index[i]))
        except IndexError:
            return ''
    formatter = mpl.ticker.FuncFormatter(format_index)
    ax.xaxis.set_major_formatter(formatter)


def groupby_times(df, kind, unit=None):
    """Groupby specific times

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with `pandas.TimedeltaIndex` as index.
    kind : {'monthly', 'weekly', 'daily', 'hourly', 'minutely', 'all'}
        How to group `df`.
    unit : str (optional)
        What unit to use

    Returns
    -------
    Grouped

    """

    def tmp_since_last(freq):
        if freq:
            return since_last(df.index, freq, unit)
        else:
            return None

    key_dict = {
        'monthly': 'M',
        'weekly': 'w',
        'daily': 'd',
        'hourly': 'h',
        'minutely': 'm',
        'secondly': 's',
        'all': None
    }
    # key_dict.update({v:v for v in key_dict.values()})

    if kind not in key_dict:
        raise NotImplementedError('key must be something else')
        # group_key = since_last(df.index, kind, unit)
    else:
        group_key = tmp_since_last(key_dict[kind])
    grouped = df.groupby(group_key)
    return grouped
