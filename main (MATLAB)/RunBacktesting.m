% This script stitches together the various methods in backtester in order
% to generate profit and loss of the algorithm as well as various other statistics
% simply from a csv file of data points.
port = Backtester;
port = port.construct('someName');
[returnsSums,totalRet] = port.plotIt(port.data);
[avgRet, maxRet, startBal, endBal, percentChange, endVals] = port.calcPerformance(port.data,returnsSums);

format("bank");

for i = 1:length(port.coinList)
    disp(port.coinList(i) + "  =   " + percentChange(i) + "%  ");
    disp("Compounded ending balance (initial value $1) = $" + endVals(i));
end

disp("----------------------------------")
fprintf("\n")
disp("Average return = " + avgRet + "%")
disp("Max single asset return = " + maxRet + "%")
disp("Starting portfolio balance : " + startBal)
disp("Ending portfolio balance : " + endBal)