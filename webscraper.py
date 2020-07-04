from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import datetime as dt
import time
from pprint import pprint
import pandas as pd
import os
import logging

logging.basicConfig(
    filename='webscraper.log',
    format='%(levelname)s %(asctime)s: %(message)s',
    level=logging.DEBUG
)


def query_webpage(date):
    """
    Gets the availabilities of permits from date to date + 5 days
    If successful:
        Returns a list of dicts to be loaded into pandas
    Else:
        Returns None
    """
    logging.info('Starting query.')

    opts = Options()
    #opts.headless = True    # Uncomment to run headless
    opts.headless = False
    with webdriver.Firefox(options=opts) as driver:
        driver.get('https://camping.ehawaii.gov/camping/all,details,1692.html')

        for element in driver.find_elements_by_tag_name('li'):
            if element.get_attribute('aria-labelledby') == 'ui-id-5':
                element.click()

        all_rows = []

        # 25-30 days from today
        #
        t_25 = date + dt.timedelta(days=25)
        t_25_str = t_25.strftime("%m/%d/%Y")
        all_rows.extend(get_availability(driver, t_25_str))

        # 30-35 days from today
        #
        t_30 = date + dt.timedelta(days=30)
        t_30_str = t_30.strftime("%m/%d/%Y")
        all_rows.extend(get_availability(driver, t_30_str))

        return all_rows

    return None


def get_availability(driver, date):
    logging.info('Getting availability for {}'.format(date))

    # Enter desired date into calender input
    #
    cal_elem = driver.find_element_by_id('availability_calendar')
    cal_elem.clear()
    cal_elem.send_keys('{}{}'.format(date, Keys.RETURN))

    # Wait until "Processing" element appears and disappears
    #
    block_elem = WebDriverWait(
        driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'blockUI')))
    WebDriverWait(
        driver, 10).until(
            EC.staleness_of(block_elem))

    # Extract availability information from table
    #
    table_elem = driver.find_element_by_id('sites_table')
    headers = table_elem.find_elements_by_tag_name('th')[6:]
    dates = [header.text for header in headers]
    cell_data = table_elem.find_elements_by_tag_name('td')[6:11]
    availabilities = [avail.text for avail in cell_data]

    # Move data into list of dictionaries
    #
    timestamp = dt.datetime.now()
    all_rows = []
    for i, date in enumerate(dates):
        row_dict = {
                'time checked': timestamp,
                'date': dates[i],
                'availability': availabilities[i]
            }
        all_rows.append(row_dict)

    return all_rows


def save_data(result):
    """
    Save data to a new csv otherwise append to old

    """
    # todo add logging
    if not os.path.exists('permit_availability.csv'):
        df = pd.DataFrame(columns=['time checked', 'date', 'availability'])
    else:
        df = pd.read_csv('permit_availability.csv', index_col=0)

    # rows_to_add = query_webpage(None)
    rows_to_add_df = pd.DataFrame(result)
    df = pd.concat([df, rows_to_add_df], ignore_index=True, sort=False)

    df.to_csv('permit_availability.csv')


if __name__ == '__main__':

    today = dt.datetime.now().date()
    results = query_webpage(today)
    pprint(results)
    save_data(results)


