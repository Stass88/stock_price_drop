import yfinance as yf
import smtplib
import time
from email.message import EmailMessage
from datetime import datetime
from config.config import KEY, EMAIL, SERVICE_NAME
import pandas as pd
import utils.app_logger
import logging

logger = logging.getLogger(SERVICE_NAME)

def calculate_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """
    :param data: Dataframe contains datetime and open price columns
    :return: DataFrame if conditions are met,
    such as drop in a stock price
    """
    data['Open_6'] = data['Open'].shift(6)
    data['Open_1'] = data['Open'].shift(1)
    data['Open/Open_1'] = (data['Open'] - data['Open_1']) / data['Open'] * 100
    data['Open/Open_6'] = (data['Open'] - data['Open_6']) / data['Open'] * 100
    data.loc[(data['Open/Open_1'] <= -2) & (data['Open/Open_6'] <= -5), 'Drop'] = 'True'
    return data[data['Drop'] == 'True']

lst = ['SHOP', 'DOW J', 'S&P 500', 'AAPL', 'BA', 'BRK-B', 'DIS', 'GE', 'HD', 'SBUX', 'MSFT', 'AMD', 'TSLA',
     'NIO', 'BNTX', 'MRNA', 'TCEHY', 'SAAB-B.ST', 'NFLX', 'FB', 'GM', 'V', 'SHEL.L', 'NKE', 'NVDA', 'FTCH', 'SHOP']
while True:
    weekno = datetime.today().weekday()
    current_time = datetime.now().strftime('%H:%M:%S')
    # execute code only on working days and NASDAQ working hours (time zone GTM+2)
    if weekno < 5 and current_time >= '16:25:00' and current_time <= '23:35:00':
        for i in lst:
            # extract stock prices
            data = yf.download(tickers=i, period='1d', interval='5m')
            data = data.reset_index()
            # select last 7 rows
            data = data.tail(7)
            data = data[['Datetime', 'Open']]
            # create metrics
            data = calculate_metrics(data)

            if len(data) > 0:
                email_address = EMAIL
                email_password = KEY

                # create email
                msg = EmailMessage()
                msg['Subject'] = i
                msg['From'] = email_address
                msg['To'] = email_address
                msg.set_content('Stock price drop')

                # send email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(email_address, email_password)
                    smtp.send_message(msg)
                # Saving results to log format for historical analyse
                logger.info('Results', extra={'company_name': i, 'open_price' : str(data['Datetime'].tail(1).iloc[0]),
                                              'service_name' : SERVICE_NAME})
    else:
        pass
    # wait for 5 minutes before next iteration starts
    time.sleep(300)
