import logging

logging.basicConfig(filename='app.log',
                    level = logging.INFO,
                    format='%(asctime)s - %(company_name)s - %(open_price)s - %(service_name)s',
                    filemode = 'a')