% Get user input to determine what to do
list = {'Fetch Data From Coinbase','Backtest Data','Both'};
[indx,tf] = listdlg('ListString',list,'SelectionMode','single');

% If fetching data from coinbase.... 
if indx == 1 || indx == 3
    GetCoinbaseData();

% If backtesting
elseif indx == 2 || indx == 3
    RunBacktesting();
    
end
