from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.common.by import By
from src.db.config import engine
from sqlalchemy.orm import Session
from src.db.models import Apartment
from src import settings
from selenium.webdriver.chrome.options import Options
from loguru import logger


def get_options():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")


def validate_price(price: str):
    prices = price.split('\n')
    middle = len(prices) // 2
    average = prices[middle]
    average = average.replace(',', '')
    try:
        average = float(average[1:])
        return average
    except:
        return None


def validate_beds(beds: str):
    validated = beds.replace('Beds: ', '')
    return validated


def validate_date(date: str):
    date_parts = date.split('/')
    if len(date_parts) == 3:
        return datetime(year=int(date_parts[2]),
                        month=int(date_parts[1]),
                        day=int(date_parts[0]))

    else:
        return datetime.today()


def find_image(apartment):
    try:
        img = apartment.find_element(By.CSS_SELECTOR, 'div > div.left-col > div.image > picture > img')
        src = img.get_attribute('src')
        return src
    except NoSuchElementException:
        return None


def save(instances):
    with Session(engine) as session:
        session.add_all(instances)
        session.commit()
        session.close()


def collect_data(apartment):
    img = find_image(apartment)
    title = apartment.find_element(By.CSS_SELECTOR, 'div > div.title > a')
    price = apartment.find_element(By.CSS_SELECTOR, 'div > div.price')
    date = apartment.find_element(By.CSS_SELECTOR, 'div > div.location > span:nth-child(2)')
    desc = apartment.find_element(By.CSS_SELECTOR, 'div > div.description')
    city = apartment.find_element(By.CSS_SELECTOR, 'div > div.location > span:nth-child(1)')
    beds = apartment.find_element(By.CSS_SELECTOR, 'div > div.rental-info > span.bedrooms')

    valildated_price = validate_price(price.text)
    validated_beds = validate_beds(beds.text)
    validated_date = validate_date(date.text)

    data = {
        'name': title.text,
        'description': desc.text,
        'city': city.text,
        'img': img,

        'date': validated_date,
        'beds': validated_beds,
        'price': valildated_price,
        'currency': price.text[:1] if valildated_price else None,
    }

    # print(f'TITLE: {title.text}')
    # print(f'IMG: {img}')
    # print(f'PRICE: {price.text}')
    # print(f'CITY: {city.text}')
    # print(f'DATE: {date.text}')
    # print(f'DESC: {desc.text}')
    # print(f'BEDS: {beds.text}')
    # print('')

    return data


def init_driver():
    logger.info('Initializing Chrome Driver')
    options = get_options()
    # driver = webdriver.Chrome(settings.CHROME_DRIVER_PATH, chrome_options=options)
    driver = Remote('http://selenium:4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.CHROME, options=options)
    return driver


def get_apartments(driver: Remote, page: int):
    sleep(5)

    logger.info('Getting apartments from web')
    driver.get(settings.KIJIJI_URL.format(page))

    logger.info('Searching for elements in html')
    fetched_apartments = driver.find_elements(By.CLASS_NAME, 'search-item')

    apartments = []

    logger.info('Collect data from found elements')
    for i, a in enumerate(fetched_apartments):
        data = collect_data(a)
        apartments.append(Apartment(**data))
        logger.info(f'Data collected for element {i}')
    return apartments


def scrap():
    driver = init_driver()
    for page in range(settings.PAGE_FROM, settings.PAGE_TILL + 1):
        apartments = get_apartments(driver, page)
        save(apartments)
        logger.info(f'Page {page} was scraped successfully')
    driver.quit()
