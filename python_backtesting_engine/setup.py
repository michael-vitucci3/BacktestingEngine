from setuptools import setup
import sys

sys.path.append('.')
setup(
    name='BacktestingEngine',
    version='4.0.7',
    packages=['python_backtesting_engine', 'python_backtesting_engine.Backtesting',
              'python_backtesting_engine.Brownian_Motion', 'python_backtesting_engine.Coinbase_Fetcher'],
    package_dir={'': 'src'},
    url='https://github.com/michael-vitucci3/BacktestingEngine',
    license='LICENSE',
    author='mike',
    author_email='author@example.com',
    description='Backtest your own algo, fetch Coinbase data, and generate Brownian data',
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
