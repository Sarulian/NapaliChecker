from selenium import webdriver
from datetime import datetime as dt
from pprint import pprint

def query_webpage(date):
    with webdriver.Firefox() as driver:
        driver.get('https://camping.ehawaii.gov/camping/all,details,1692.html')
        
        for element in driver.find_elements_by_tag_name('li'):
            if element.get_attribute('aria-labelledby') == 'ui-id-5':
                element.click()
        
        table_elem = driver.find_element_by_id('sites_table')
        headers = table_elem.find_elements_by_tag_name('th')[6:]
        dates = [header.text for header in headers]
    
        cell_data = table_elem.find_elements_by_tag_name('td')[6:11]
        availabilities = [avail.text for avail in cell_data] 
        
        timestamp = dt.now()

        # [
        #   { now, date, availability
        #   now, date, availability
        #   now, date, availability
        #   now, date, availability
        #   now, date, availability

        all_rows = []
        for i, date in enumerate(dates):
            row_dict = {
                    'time checked': timestamp,
                    'date': dates[i],
                    'availability': availabilities[i]
                }
            all_rows.append(row_dict)

        pprint(all_rows)

        return 

    return None

if __name__ == '__main__':
    query_webpage(None)
