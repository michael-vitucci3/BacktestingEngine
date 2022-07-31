import pandas as pd

def StratFile(ret):
    logical_df = ret.copy()
    ind = logical_df.index
    logical_df[logical_df > 0] = 1
    logical_df[logical_df < 0] = 0
    return logical_df
