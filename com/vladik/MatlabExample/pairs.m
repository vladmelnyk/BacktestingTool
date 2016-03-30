function varargout = pairs(series2, series3, M, N, spread, scaling, cost)
% PAIRS returns a trading signal for a simple pairs trading strategy

%%
% Copyright 2010, The MathWorks, Inc.
% All rights reserved.

%% Process input args
if ~exist('scaling','var')
    scaling = 1;
end

if ~exist('cost','var')
    cost = 0;
end

if ~exist('spread', 'var')
    spread = 1;
end

if nargin == 1
    % default values
    M = 420;
    N = 60;
elseif nargin == 2
    error('PAIRS:NoRebalancePeriodDefined',...
        'When defining a lookback window, the rebalancing period must also be defined')
end

% Very often, the pairs will be convincingly cointegrated, or convincingly
% NOT cointegrated.  In these cases, a warning is issued not to read too
% much into the test statistic.  Since we don't use the test statistic, we
% can suppress these warnings.
warning('off', 'econ:egcitest:LeftTailStatTooSmall')
warning('off', 'econ:egcitest:LeftTailStatTooBig')

%% Sweep across the entire time series
% Every N periods, we use the previous M periods' worth of information to
% estimate the cointegrating relationship (if it exists).
%
% We then use this estimated relationship to identify trading opportunities
% until the next rebalancing date.

s = zeros(size(series2));
series = zeros(size(series2));
indicate = zeros(length(series2),1);
s2 = zeros(size(series3));
s3 = zeros(size(series3));
indicate2= zeros(length(series3),1);
isOpenedSeries2 = false; 
isOpenedSeries3 = false;
% M=420; N=60; 
j = max(M,N);
for i = max(M,N) : N : length(s)-N
    % Calibrate cointegration model by looking back.
    [h,~,~,~,reg1] = egcitest(series2(i-M+1:i, :));
    if h ~= 0  
        % Only engage in trading if we reject the null hypothesis that no
        % cointegrating relationship exists.
       
        % The strategy:
        % 1. Compute residuals over next N days
        res(i:i+N-1) = (series2(i:i+N-1, 1)-(reg1.coeff(1) + reg1.coeff(2).*series2(i:i+N-1, 2)));
        
        % 2. If the residuals are large and positive, then the first series
        % is likely to decline vs. the second series.  Short the first
        % series by a scaled number of shares and long the second series by
        % 1 share.  If the residuals are large and negative, do the
        % opposite.
       
            for j = i : 1 : i+N-1
                 indicate(j) = res(j)/reg1.RMSE;
             if(((res(j)/reg1.RMSE) > spread) && (isOpenedSeries2 == false))
               s(j, 2) = (res(j)/reg1.RMSE > spread);
               s(j, 1) = -reg1.coeff(2) .* s(j, 2);
               isOpenedSeries3 = false;
               isOpenedSeries2 = true;
               series (j,:) = series2(j,:);
               s3(j,:) = s(j,:);
               break
             end
             
            end
    end  
        
    
   [h,~,~,~,reg1] = egcitest(series3(j-M+1:i, :));
    if h ~= 0  
        % Only engage in trading if we reject the null hypothesis that no
        % cointegrating relationship exists.
        
        % The strategy:
        % 1. Compute residuals over next N days
       res2(j:i+N-1) = series3(j:i+N-1, 1)-(reg1.coeff(1) + reg1.coeff(2).*series3(j:i+N-1, 2));
%        Importnat to remember the last used index in the inner for cycle
%        and pass it to the next for cycle that checks for different signal
            for j = j : 1 : i+N-1
                indicate2(j) = res2(j)/reg1.RMSE;
             if(((res2(j)/reg1.RMSE) < -spread) && (isOpenedSeries3 == false))
               s2(j, 2) =  - (res2(j)/reg1.RMSE < -spread);
               s2(j, 1) = -reg1.coeff(2) .* s2(j, 2);
                isOpenedSeries2 = false;
               isOpenedSeries3 = true;
               series(j,:) = series3(j,:);
               s3(j,:) = s2(j,:);
             end
            
            end
    end
end

%% Calculate performance statistics


r  = sum([0 0; s(1:end-1, :) .* diff(series2) - abs(diff(s))*cost/2] ,2);
r2  = sum([0 0; s3(1:end-1, :) .* diff(series) - abs(diff(s3))*cost/2] ,2);
sh = scaling*sharpe(r,0); 

if nargout == 0
    %% Plot results
    ax(1) = subplot(6,1,1);
    plot(series2), grid on
    legend('Okcoin','Bitmex')
    title(['Pairs trading results, Sharpe Ratio = ',num2str(sh,3)])
    ylabel('Price (USD)')
    
    ax(2) = subplot(6,1,2);
    plot([indicate,spread*ones(size(indicate)),-spread*ones(size(indicate))])
    grid on
    legend(['Indicator'],'Okcoin: Over bought','Okcoin: Over sold',...
        'Location','NorthWest')
    title(['Pairs indicator: rebalance every ' num2str(N)...
        ' minutes with previous ' num2str(M) ' minutes'' prices.'])
    ylabel('Indicator')
    ax(3) = subplot(6,1,3);
    plot(series3), grid on
    legend('Okcoin','Bitmex')
    title(['Pairs trading results, Sharpe Ratio = ',num2str(sh,3)])
    ylabel('Price (USD)')
    
    ax(4) = subplot(6,1,4);
    plot([indicate2,spread*ones(size(indicate2)),-spread*ones(size(indicate2))])
    grid on
    legend(['Indicator'],'Okcoin: Over bought','Okcoin: Over sold',...
        'Location','NorthWest')
    title(['Pairs indicator: rebalance every ' num2str(N)...
        ' minutes with previous ' num2str(M) ' minutes'' prices.'])
    ylabel('Indicator')
    
    ax(5) = subplot(6,1,5);
    plot([s,s2]), grid on
    legend('Position for Okcoin','Position for Bitmex','Cumulative Return',...
        'Location', 'NorthWest')
    title(['Final Return = ',num2str(sum(r),3),' (',num2str(sum(r)/mean(series2(1,:))*100,3),'%)'])
    ylabel('Return (USD)')
   
    linkaxes(ax,'x')
     ax(6) = subplot(6,1,6);
    plot([s2,cumsum(r2)]), grid on
    legend('Position for Okcoin','Position for Bitmex','Cumulative Return',...
        'Location', 'NorthWest')
    title(['Final Return = ',num2str(sum(r2),3),' (',num2str(sum(r2)/mean(series3(1,:))*100,3),'%)'])
    ylabel('Return (USD)')
    xlabel('Serial time number')
    linkaxes(ax,'x')
    
else
    %% Return values
    for i = 1:nargout
        switch i
            case 1
                varargout{1} = s; % signal
            case 2
                varargout{2} = r; % return (pnl)
            case 3
                varargout{3} = sh; % sharpe ratio
            case 4
                varargout{4} = indicate; % indicator
            otherwise
                warning('PAIRS:OutputArg',...
                    'Too many output arguments requested, ignoring last ones');
        end 
    end
end