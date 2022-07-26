function GetCoinbaseData

    disp("fetching all daily values of all coins from coinbase....")
    disp("See included .csv for predownloaded data...")
    
    % Create and move into working forlder
    currentFolder = cd;
    mkdir("BacktestingData")
    cd("BacktestingData")
    
    % Fetch Coin List
    url =  'https://api.pro.coinbase.com/currencies';
    coins = webread(url);
    coinList =  {coins.id}.';
    
    % Fetch all daily values
    get_data(coinList);
    
    % Create singe time table from csv files
    finalTT = BigData(coinList);
    cd(currentFolder);
    writetimetable(finalTT,'bigCSVData.csv');
    disp("____________________________________________________ " + ...
        "...Completed..."                                       + ...
        "_____________________________________________________");

end

function finalTT = BigData(coinList)
    
    % Initialize final timetable
    finalTT = datetime('1/1/2015'):days(1):datetime('today');
    finalTT = timetable(finalTT');
    
    % Create array of file names
    coinListFiles = [];
    for i = 1:height(coinList)
        temp =  [cell2mat(coinList(i))];
        temp = horzcat(temp, '.xlsx');
        temp = string(temp);
        coinListFiles = [coinListFiles, temp];
    end
    
    coinListFiles = sort(coinListFiles);
    
    % Import files
    temp = [];
    for i = 1:height(coinList)
    
        try
            TT = readtimetable(coinListFiles(i));
            finalTT = synchronize(finalTT,TT,"union",'fillwithconstant','Constant',0);
            temp = [temp ; string(cell2mat(coinList(i)))];
        catch
            disp(cell2mat(coinList(i)) + " Not imported")
        end
    end


% Create final TT
finalTT.Properties.VariableNames = temp;

finalTT([2,end],:) = [];

finalTT = retime(finalTT, "daily","previous");

end


function get_data(coin_name)
    
    % Get start date and current date
    rn = datetime('today', 'Format', 'uuuu-MM-dd''T''HH:mm:ss''Z');
    starttime = datetime('2015-01-01T00:00:00Z','Format','uuuu-MM-dd''T''HH:mm:ss''Z');
    
    % Initialize Stuff
    flag = false;
    a=0;
    
    for i=1:length(coin_name)
        coin = coin_name{i};
        Data= [];
    
        % Fetch 300 days at a time (Coinbase's max fetch amount)
        for ii=starttime:days(300):rn-1
            try
                % Variable for cheecking if catch was hit
                flag = false;
    
                % API call
                url = "https://api.pro.coinbase.com/products/" + coin_name(i) + "-USD" + "/candles?start="+ string(ii) ...
                    + "&end="+ string(ii + days(300))+"&granularity="+ string(86400);
                price=webread(url);
                Data = [price;Data];
    
            catch
                flag = true;
                break;
            end
    
            % Coinbase only allows 10 requests per second
            pause(0.05);
    
            if a ~= i
                disp(i + "/" + length(coin_name) + " completed")
            end
            a = i;
        end
    
        % if Coin is successfully fetched, clean up data
        if flag == false
            % Throw out any errors and keep going, I have not encountered
            % any that needed to be handled, let me know if you do
            try
                Data = table(datetime(Data(:,1),'ConvertFrom','posixtime'),Data(:,4));
                Data.Properties.VariableNames = {'Date', 'Close'};
                Data = sortrows(Data,'Date','ascend');
    
                %Save data to *.xlsx files
                filename = strcat(coin, ".xlsx");
                writetable(Data,filename);
                Data = [];
            end
        end
    end
end