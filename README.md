# groupby

Convenience functions for grouping datetimes in [pandas](http://www.github.com/pydata/pandas).

## Requirements

* [numpy](http://www.github.com/numpy/numpy)
* [pandas](http://www.github.com/pydata/pandas)

## Examples
```python
import groupby
import matplotlib.pyplot as plt
grouped = groupby.groupby_times(df, 'weekly')
weekly_mean = grouped.mean()

# plotting timedeltas doesn't really work in pandas so this helps
import matplotlib.pyplot as plt
grouped.plot_timedelta(weekly_mean)
```
