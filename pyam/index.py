import pandas as pd
import numpy as np


def get_index_levels(df, level):
    """Return the category-values for a specific level"""
    return list(df.index.levels[df.index._get_level_number(level)])


def replace_index_values(df, level, mapping):
    """Replace one or several category-values at a specific level"""
    index = df if isinstance(df, pd.Index) else df.index

    n = index._get_level_number(level)

    # replace the levels
    _levels = index.levels[n].map(lambda l: mapping.get(l, l))
    _unique_levels = _levels.unique()

    # if no duplicate levels exist after replace, set new levels and return
    if len(_levels) == len(_unique_levels):
        return index.set_levels(_levels, n)

    # if duplicate levels exist, re-map the codes
    level_mapping = _unique_levels.get_indexer(_levels)
    _codes = np.where(index.codes[n] != -1, level_mapping[index.codes[n]], -1)
    return index.set_codes(_codes, n).set_levels(_unique_levels, n)


def append_index_level(index, codes, level, name, order=False):
    """Append a level to a pd.MultiIndex"""
    new_index = pd.MultiIndex(
        codes=index.codes + [codes],
        levels=index.levels + [level],
        names=index.names + [name])
    if order:
        new_index = new_index.reorder_levels(order)
    return new_index
