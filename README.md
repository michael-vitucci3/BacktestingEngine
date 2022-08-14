# BacktestingEngine
 MATLAB scripts to fetch data from Coinbase and backtest an algorithm on the data. Start by running **main.m**. This will fetch all of the
 necissary backtesting data and execute the defult algorithm. Once you do this, feel free to adjust StratFile.m to your own algorithm and 
 test profitability. StratFile is practically infinity customizable as long as it still returns a logical timetable for the same dates/assets.
 This means that from StratFile.m you can call other files or even languages, import more data, or just about anything else you can possibly think of
 without disrupting the backtest analysis built in.
 
 
## Files Overview
=======================================================================================================

Backtester.m

                         Backtester class contains all necessary operations (besides StratFile which
                         is stored in the main folder) to fully execute a backtest. Furthermore,
                         it is a convient data storage object. Apon calling obj.constructor 
                         all data will populate including 
                           fileLoc : Location of user input csv data
                           inTT : Timetable of dates and prices gathered from a user input csv
                           Returns : Daily returns of each asset during all provided data points
                           coinList : List of assets gathered from csv file
                           data : Using StratFile, a new version of returns is generated. If the 
                                   algorithm is holding an asset on that day, the data points
                                    remain, otherwise it is changed to zero. This yeilds the actual
                                    returns assuming instintanious rebalancing at 12:00:00 UTC
                                    daily.  
--------------------------------------------------------------------------------------------------------------                                    
GetCoinbaseData.m      

                         This script will fetch a list of all poroducts on coinbase, import the entire
                         daily close value history, then save each one to a .xlsx file. Next, it will read 
                         back in each file and save each one to a combined .csv file containing all data 
                         points of all coins. Finally, it will read in the .csv file inorder to make a matlab 
                         timetable which can be used for analysis. Of course that system could be simplified 
                         drasticly, however I left in some unneccisary steps so the data being fed in can be 
                         taylored to excactly what is needed. 
--------------------------------------------------------------------------------------------------------------                                        
main.m                   

                         Main file which calls every other file. **Start Here**
-------------------------------------------------------------------------------------------------------------- 
RunBacktesting.m         

                         This script stitches together the various methods in backtester in order
                         to generate profit and loss of the algorithm as well as various other statistics
                         simply from a csv file of data points.
-------------------------------------------------------------------------------------------------------------- 
StratFile.m              

                            INPUT:
                                   inTT: input timetable containing dates and daily close values
                                      of any amount of coins/stocks/commodities/derivatives/etc....
                            OUTPUT:
                                   logicTT: output time table with same dates and variable names
                                      as inTT, however filled with a 1 if the strategy says you are
                                      holding the asset on that day, 0 if you are not (Assuming
                                      portfolio rebalancing once daily at the open of each day
                                      
                            Example stratagy file, delete the following code and replace with
                            your own in order to run backtesting.

                            Buys and sells are determined off of closing price for the day prior.
                            If % change for day(n) is positive, day(n+1) the algorithm will hold
                            the asset, only to sell if % change is negative
