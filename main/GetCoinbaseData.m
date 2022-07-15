function GetCoinbaseData

    disp("fetching all daily values of all coins from coinbase....")
    disp("See included .csv for predownloaded data...")
    
    % Fetch Coin List
    url =  'https://api.pro.coinbase.com/currencies';
    coins = webread(url);
    coinList =  {coins.id}.';
    
    % Fetch all daily values
    get_data(coinList);
    
    % Create singe time table from csv files
    bigCVSData = BigData(coinList); 
    
    disp("Completed")
    head(bigCVSData)

end

function finalTT = BigData(coinList)

    finalTT = datetime('1/1/2015'):days(1):datetime('today');
    finalTT = timetable(finalTT');
    
    coinListFiles = [];

    for i = 1:height(coinList)
    temp =  [cell2mat(coinList(i))];
    temp = horzcat(temp, '.xlsx');
    temp = string(temp);
    coinListFiles = [coinListFiles, temp];
    end

    disp(coinListFiles)

    temp = [];
    for i = 1:height(coinList)
    
        try
        opts = detectImportOptions(coinListFiles(i));
        opts.SelectedVariableNames = {'Time', 'Close'};
        T = readtable(coinListFiles(i),opts);
        TT = table2timetable(T);
        finalTT = synchronize(finalTT,TT,"union",'fillwithconstant','Constant',0);
        temp = [temp ; string(cell2mat(coinList(i)))];
        catch

        end
    end
    
    
    finalTT.Properties.VariableNames = temp;
    
    finalTT([1,end],:) = [];

    retime(finalTT, "daily","previous")
    
    writetimetable(finalTT,'bigCSVData.csv')

end

% The following two functions are adapted to fit this usecase from the
% MATLAB file exchange: Cong Dong Ngoc Minh (2022). Building Crypto Currency Prediction
% (https://www.mathworks.com/matlabcentral/fileexchange/92905-building-crypto-currency-prediction),
% MATLAB Central File Exchange. Retrieved July 13, 2022. 

function price = getprices(coinName,startdate,stopdate,granularity)
    
    %https://docs.pro.coinbase.com/#get-historic-rates
    %all cryptocurrency products returned in USD
    org_url='https://api.pro.coinbase.com/products/';
    product = strcat(coinName,'-USD');

    % t=datetime('now','Format','uuuu-MM-dd''T''HH:mm:ss''Z');
    startdate=char(startdate);
    stopdate = char(stopdate);

    %granularity is in seconds, so we are getting 1-minute candle: The granularity field must be one of the following values: {60, 300, 900, 3600, 21600, 86400}.
    % Otherwise, your request will be rejected.
    % granularity = period;
    %Returns back: [time, low, high, open, close, volume];
    %https://api.pro.coinbase.com/products/BTC-USD/candles?start=2015-01-01T00:00:00Z&end=2015-01-08T00:00:00Z&granularity=3600
    url=strcat(org_url,product,'/candles?start=',startdate,'&end=',stopdate,'&granularity=',num2str(granularity));

    % url=strcat(org_url,product,'/candles?start=',startdate,'&end=',stopDate,'&granularity=',granularity);
    variables = {'Time', 'Low', 'High', 'Open', 'Close', 'Volume'};
    Data=webread(url);
    if isempty(Data)
        price = Data;
    else
        price=array2table(Data,'VariableNames',variables);
        price.Time=datetime(price.Time,'ConvertFrom','posixtime');
    end
    
    end
    
    function get_data(coin_name)
    
    %Get raw data from Coinbase in duration 01-Jan-2018 to 08-jan-2021
    %T1 = datetime(2015,01,1,0,0,0,'Format','uuuu-MM-dd''T''HH:mm:ss''Z');

    % T2 = datetime(2021,01,21,0,0,0,'Format','uuuu-MM-dd''T''HH:mm:ss''Z');
    %T2=datetime('now','Format','uuuu-MM-dd''T''HH:mm:ss''Z');
    %totalNumDays = days(T2-T1);
    %complete = arrayfun(@(x) T1+x, 0:totalNumDays, 'UniformOutput', false);

    % coin_name ={'ETH','LTC','BCH'};
    % coin_name ={'BTC'};
    %Output variable from API: {'Time', 'Low', 'High', 'Open', 'Close', 'Volume'};
    %Granularity is in seconds, so we are getting 1-minute candle:
    % The granularity field must be one of the following values: {60, 300, 900, 3600, 21600, 86400}.
    granularity = 86400;%6hrs candle
    rn = datetime(datetime('2022-01-01 00:00:00'),'Format','uuuu-MM-dd''T''HH:mm:ss''Z');
    starttime = datetime('2015-01-01T00:00:00Z','Format','uuuu-MM-dd''T''HH:mm:ss''Z');
    a=0;
    flag = false;
    for i=1:length(coin_name)
        product = coin_name{i};
        %Initialize first line fo concatenating
        Data=table(starttime,0,0,0,0,0,'VariableNames',{'Time', 'Low', 'High', 'Open', 'Close', 'Volume'});
        %Loop for getting data
     %   numDays = days(datetime('2022-01-01 00:00:00')-datetime('2015-01-01 00:00:00'));
        for ii=starttime:days(250):rn-1
            try
                flag = false;
                price = getprices(product,ii,ii+250,86400);
            catch
                flag = true;
                break;
            end
            Data = [price;Data];
    
            % Coinbase only allows 10 requests per second
            pause(0.05);
    
            if ~(a == i)
    
                disp(i + "/" + length(coin_name) + " completed")
    
            end
    
            a=i;
        end
    
        if flag == false
            Data = sortrows(Data,'Time','ascend');
            Data(2,:)=[];%Remove initialized Data
            %Save data to *.xlsx files
            filename = strcat(product,".xlsx");
            writetable(Data,filename);
        end
    end
end

