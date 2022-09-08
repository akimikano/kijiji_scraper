import os

KIJIJI_URL = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{0}/c37l1700273'
CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver/chromedriver'
PAGE_FROM = 1
PAGE_TILL = 3

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DATABASE_URL = "sqlite:///db.sqlite"
# DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
