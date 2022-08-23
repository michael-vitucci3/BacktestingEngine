def strat_file(ret):
    """
    Example strategy which is not profitable. If you trade based off it, you will lose money....
    don't trade based off of this. Do write your own strategy here. _logical_df must be a dataframe of ones and zeros
    representing days the algorithm is holding the asset (one is holding, zero is not.)
    """
    logical_df = ret.copy()
    logical_df[logical_df > 0] = 1
    logical_df[logical_df < 0] = 0
    return logical_df
