from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from datetime import datetime as dt
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
        driver.find_element_by_id(
            'availability_calendar').send_keys(
                '{}{}'.format(date, Keys.RETURN))
        time.sleep(5)

        disabled_states = driver.find_elements_by_class_name('ui-state-disabled')
        print(disabled_states)

        table_elem = driver.find_element_by_id('sites_table')
        headers = table_elem.find_elements_by_tag_name('th')[6:]
        dates = [header.text for header in headers]
        pprint(dates)

        cell_data = table_elem.find_elements_by_tag_name('td')[6:11]
        availabilities = [avail.text for avail in cell_data]

        timestamp = dt.now()

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


if __name__ == '__main__':
    today = dt.date.today()
    # from today 25 days
    t_25 = today-DT.timedelta(days=25)
    # from today 30 days
    t_30 = today-DT.timedelta(days=30)
    pprint(t_30, t_25)
    exit()
    # queery
    result = query_webpage('08/22/2020')
    pprint(result)
    # exit()

    if not os.path.exists('permit_availability.csv'):
        df = pd.DataFrame(columns=['time checked', 'date', 'availability'])
    else:
        df = pd.read_csv('permit_availability.csv', index_col=0)

    # rows_to_add = query_webpage(None)
    rows_to_add_df = pd.DataFrame(result)
    df = pd.concat([df, rows_to_add_df], ignore_index=True, sort=False)

    df.to_csv('permit_availability.csv')

