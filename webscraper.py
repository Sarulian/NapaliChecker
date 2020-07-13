import requests
from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
import os
import logging
import sys
import time
from pprint import pprint

logging.basicConfig(
    filename='webscraper.log',
    format='%(levelname)s %(asctime)s: %(message)s',
    level=logging.INFO
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

    all_rows = []

    # 25-30 days from today
    #
    t_25 = date + dt.timedelta(days=25)
    t_25_str = t_25.strftime("%Y%m%d")
    all_rows.extend(get_availability(t_25_str))

    # 30-35 days from today
    #
    t_30 = date + dt.timedelta(days=30)
    t_30_str = t_30.strftime("%Y%m%d")
    all_rows.extend(get_availability(t_30_str))

    return all_rows


def get_availability(date_str):
    logging.info('Getting availability for {}'.format(date_str))
    res = requests.get(
        'https://camping.ehawaii.gov/camping/all,sites,0,25,1,1692,,,,' \
        '{},5,,,1,1594601235210.html'.format(date_str)
    )
    soup = BeautifulSoup(res.text, 'html.parser')

    table = soup.find('table')
    table_rows   = table.find_all('tr')

    for i, tr in enumerate(table_rows):
        if i == 0:
            th = tr.find_all('th')
            row = [i.text.replace('\n', '').strip() for i in th]
            dates = row[6:11]
        elif i == 1:
            td = tr.find_all('td')
            row = [i.text.replace('\n', '').strip() for i in td]
            availabilities = row[6:11]

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
    out_file = '/home/pi/Github/NapaliChecker/permit_availability.csv'
    # todo add logging
    if not os.path.exists(out_file):
        df = pd.DataFrame(columns=['time checked', 'date', 'availability'])
    else:
        df = pd.read_csv(out_file, index_col=0)

    # rows_to_add = query_webpage(None)
    rows_to_add_df = pd.DataFrame(result)
    df = pd.concat([df, rows_to_add_df], ignore_index=True, sort=False)

    df.to_csv(out_file)


if __name__ == '__main__':

    today = dt.datetime.now().date()
    results = query_webpage(today)
    pprint(results)
    save_data(results)


