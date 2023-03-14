'''
This is a driver class which helps us to extract the share market from current market and history and showcase
the daily weekly and monthly returns in turms of percentage 
'''

#import the necessary library into driver program
import ckbvm_returns,ckbvm_stocks
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

#Create needful variables to process the data
current_date = date.today()
starting_date = current_date - relativedelta(months=4)


df = ckbvm_stocks.get_data(symbol='RELIANCE', start_date=starting_date.strftime('%d-%m-%Y'), end_date=current_date.strftime('%d-%m-%Y'))
stock_returns = ckbvm_returns.calculate_returns(df, make_csv = True, name = "Returns1")
print(stock_returns)