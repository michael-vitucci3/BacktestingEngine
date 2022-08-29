"""Edit values for custom brownian properties to utilize in backtesting"""


def get_brownian_config() -> dict:
    brownian_dict = {
        # brownian motion values
        # The Wiener process parameter.
        "delta": 2,
        # Total time.
        "t": 10.0,
        # Number of steps.
        "n": 10000,
        # Number of assets (or number of realizations)
        "m": 20,
        # Initial value
        "x0": 50}
    return brownian_dict
