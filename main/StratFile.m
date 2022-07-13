function [logicTT] = StratFile(returns)
    
    % INPUT:
    %        inTT: input timetable containing dates and daily close values
    %           of any amount of coins/stocks/commodities/derivatives/etc....
    % OUTPUT:
    %        logicTT: output time table with same dates and variable names
    %           as inTT, however filled with a 1 if the strategy says you are
    %           holding the asset on that day, 0 if you are not (Assuming
    %           portfolio rebalancing once daily at the open of each day)
    
    %************************************************************************
    % Example stratagy file, delete the following code and replace with
    % your own in order to run backtesting.
    %************************************************************************
    
    % Buys and sells are determined off of closing price for the day prior.
    % If % change for day(n) is positive, day(n+1) the algorithum will hold
    % the asset, only to sell if % change is negative
    
    % Fill logicTT with 1 or 0 based off price change of prior day
    logicTT = (returns{:,:} > 0);
    
    % Move all values forward by one day, remove last day
    logicTT = [zeros(1,width(logicTT));logicTT];
    logicTT(end,:) = [];
    
end