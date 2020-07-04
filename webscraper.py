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

def query_webpage(date):
    """
    Gets the availabilities of permits from date to date + 5 days
    If successful:
        Returns a list of dicts to be loaded into pandas
    Else:
        Returns None
    """
    opts = Options()
    #opts.headless = True
    opts.headless = False
    with webdriver.Firefox(options=opts) as driver:
        driver.get('https://camping.ehawaii.gov/camping/all,details,1692.html')

        for element in driver.find_elements_by_tag_name('li'):
            if element.get_attribute('aria-labelledby') == 'ui-id-5':
                element.click()

        disabled_states = driver.find_elements_by_class_name('ui-state-disabled')
        print(disabled_states)

        print(date)
        cal_elem = driver.find_element_by_id('availability_calendar')
        cal_elem.send_keys('{}{}'.format(date, Keys.RETURN))

        #element = WebDriverWait(
        #    driver, 5).until(
        #        EC.element_to_be_clickable((By.ID, 'availability_calender')))
        cal_elem = driver.find_element_by_class_name('availability_calendar')
        print(element)
        #'blockUI blockOverlay'
        #time.sleep(5)

        disabled_states = driver.find_elements_by_class_name('ui-state-disabled')
        print(disabled_states)

        table_elem = driver.find_element_by_id('sites_table')
        headers = table_elem.find_elements_by_tag_name('th')[6:]
        dates = [header.text for header in headers]
        pprint(dates)

        cell_data = table_elem.find_elements_by_tag_name('td')[6:11]
        availabilities = [avail.text for avail in cell_data]

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

    return None

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
    print(today)
    # from today 25 days
    t_25 = today+dt.timedelta(days=25)
    print(t_25)
    # from today 30 days
    t_30 = today+dt.timedelta(days=30)
    print(t_30)
    print(t_30.strftime("%m/%d/%Y"))

    # query1
    result = query_webpage(t_25.strftime("%m/%d/%Y"))
    pprint(result)
    save_data(result)

    # query 2
    result = query_webpage(t_30.strftime("%m/%d/%Y"))
    pprint(result)
    save_data(result)

