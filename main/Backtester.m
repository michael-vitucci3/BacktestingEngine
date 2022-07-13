% Backtester class contains all necessary operations (besides StratFile which
% is stored in the main folder) to fully execute a backtest. Furthermore,
% it is a convient data storage object. Apon calling obj.constructor 
% all data will populate including 
%   fileLoc : Location of user input csv data
%   inTT : Timetable of dates and prices gathered from a user input csv
%   Returns : Daily returns of each asset during all provided data points
%   coinList : List of assets gathered from csv file
%   data : Using StratFile, a new version of returns is generated. If the 
%           algorithm is holding an asset on that day, the data points
%           remain, otherwise it is changed to zero. This yeilds the actual
%           returns assuming instintanious rebalancing at 12:00:00 UTC
%           daily.  
classdef Backtester
    properties
        name
        fileLoc 
        inTT
        returns
        coinList
        data
    end
    methods
        function obj = construct(obj,name)
            obj.name = name;
            obj.createDialog;
            obj.fileLoc = obj.setLocation;
            obj.inTT = obj.getTimeTable;
            obj.returns = obj.calcReturns;
            obj.coinList = obj.getCoinList;
            obj.data = obj.runStrategy;
        end
        function createDialog(obj)
            d = dialog('Name','IMPORTANNT');

            txt =  uicontrol('Parent',d,...
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

        function fileLoc = setLocation(obj)
            [file,path] = uigetfile('*.csv','Select a .csv File');
            try
                fileLoc = [fullfile(path,file)];
                disp(['User selected ', fullfile(path,file)])
            catch
                error('Error, invalid input or cancle selected')
            end
            

        end

        function obj = getTimeTable(obj)

            disp("Importing Data...");
            obj.inTT = readtimetable(obj.fileLoc);
            fprintf("Completed...\n")

        end

        function returns = calcReturns(obj)
            tempTT = price2ret(obj.inTT.inTT);
            returns = removevars(tempTT,"Interval");
        end

        function coinList = getCoinList(obj)
            coinList = obj.inTT.inTT.Properties.VariableNames;
        end

        function data = runStrategy(obj)
            logicTT = StratFile(obj.returns);
            data = times(obj.returns{:,:},logicTT);
            data = fillmissing(data,"constant",0);
            data(isinf(data)) = 0;
        end

        function [returnsSums,totalRet] = plotIt(obj, data)

            returnsSums = zeros(width(data));
            for i = 1:width(data)
                returnsSums(i) = sum(data(:,i));
            end
            totalRet = sum(returnsSums);
            bar(categorical(obj.coinList),returnsSums)
        end

        function [avgRet, maxRet, startBal, endBal, percentChange, endVals] = calcPerformance(obj,data,returnsSums)
           
            coins = obj.coinList;
            endVals = zeros(length(coins));


            % Assuming seperate balances for each coin, calculate compounding
            % balance factoring in trades generated by strategy file
            for i = 1:length(coins)
                portfolioVal = 1;
                for j = 1:height(data)
                    if data(j,i) ~= 0
                        portfolioVal = portfolioVal*data(j,i) + portfolioVal;
                    end
                    endVals(i) = portfolioVal;
                end

            end
            
            percentChange = zeros(1,length(returnsSums));
            for i = 1:length(returnsSums)
                percentChange(i) = ((endVals(i)-1))*100;
            end

            avgRet = sum(percentChange)/length(percentChange);
            maxRet = max(percentChange);
            startBal = length(coins);
            endBal = startBal + sum(percentChange)/100;
            

            bar(categorical(coins),percentChange)
            
        end

    end
end

