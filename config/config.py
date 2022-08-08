from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

# Credentials
KEY = getenv("KEY")
EMAIL = getenv("EMAIL")

# Model name
SERVICE_NAME = 'stock_price'

