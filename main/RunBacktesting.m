function RunBacktesting
    
    CreateDialog();
    
    pause(0.5)
    
    [file,path] = uigetfile('*.csv','Select a .csv File');
    
    if isequal(file,0)
        disp('User selected Cancel');
    else
        disp(['User selected ', fullfile(path,file)]);
        disp("Importing Data...");
        inTT = readtimetable(fullfile(path,file));
        fprintf("Completed...\n")
        fprintf("Calculating backtested returns...\n")
        fprintf("Plotting backtested returns...\n")
        Backtester(inTT)
    end

end

function CreateDialog

    d = dialog('Name','IMPORTANNT');
   
    txt = uicontrol('Parent',d,...
        'Style','text',...
        'Position',[150 150 400 240],...
        'String',['***********************************************************************';...
        'Please select .csv file containing price data in following format:     ';...
        'Columns including "Time" followed by the name of each coin             ';...
        'Rows with date followed by closing price that day                      ';...
        'Missing data replaced with zeros                                       ';...
        'example:                                                               ';...
        'Time        coin1    coin2    coin3                                    ';...
        '________    _____    _____    _____                                    ';...
        '01-Jan-1970      1        0        0                                   ';...
        '02-Jan-1970      2        1        0                                   ';...
        '03-Jan-1970      3        2        0                                   ';...
        '04-Jan-1970      4        3        1                                   ';...
        '05-Jan-1970      5        4        2                                   ';...
        '***********************************************************************']);
    
    btn = uicontrol('Parent',d,...
        'Position',[85 20 70 25],...
        'String','Close',...
        'Callback','delete(gcf)');

end

function Backtester(inTT)
    
    coinList = inTT.Properties.VariableNames;
    
    returns = price2ret(inTT);
    returns = removevars(returns,"Interval");
    
    logicTT = [];
    
    logicTT = StratFile(returns);
    
    % Returns * logicTT = returns on each day the algo says your in
    data = times(returns{:,:},logicTT);
    data = CleanIt(data);
    data = fillmissing(data,"constant",0);
    data(isinf(data)) = 0;
    
    [returnsSums,totalRet] = plotIt(data,coinList);
    
    % Assuming seperate balances for each coin, calculate compounding
    % balance factoring in trades generated by strategy file
    for i = 1:length(coinList)
        k=1;
        portfolioVal = 1;
        for j = 1:height(data)
            if data(j,i) ~= 0
                portfolioVal = portfolioVal*data(j,i) + portfolioVal;
                portVal(k,i) = portfolioVal;
                k = k + 1;
            end
            endVals(i) = portfolioVal;
        end
    
    end
    
    endVals
    
    for i = 1:length(returnsSums)
        percentChange(i) = ((endVals(i)-1))*100;
        disp(coinList(i) + " = " + percentChange(i) + "%")
        fprintf("\n")
        disp("Compounded ending balance (initial value $1) = $" + endVals(i))
        fprintf("\n")
    end
    
    avgRet = sum(percentChange)/length(percentChange);
    maxRet = max(percentChange);
    startBal = length(coinList);
    endBal = startBal + sum(percentChange)/100;
    disp("----------------------------------")
    fprintf("\n")
    disp("Average return = " + avgRet + "%")
    disp("Max single asset return = " + maxRet + "%")
    disp("Starting portfolio balance : " + startBal)
    disp("Ending portfolio balance : " + endBal)
    
    
    bar(categorical(coinList),percentChange)
end

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

function cleanData = CleanIt(dirtyData)

    % Make some dirty data sparkle like it used to back in its glory days!
    
    %     if istabular(dirtyData)
    %         dirtyData = dirtyData{:,:};
    %     end
    
    fillmissing(dirtyData,"constant",0);
    %dirtyData(isinf(dirtyData)) = 0;
    
    cleanData = dirtyData;

end

function [returnsSums,totalRet] = plotIt(data, coinList)

    returnsSums = [];
    
    data = fillmissing(data,'constant',0);
    for i = 1:width(data)
        returnsSums(i) = sum(data(:,i));
    end
    returnsSums;
    totalRet = sum(returnsSums);
    bar(categorical(coinList),returnsSums)
    
    if sum(totalRet) > 10
        a = load('photo.mat');
        image(a.ans)
    end

end
