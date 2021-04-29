import sys
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


def scatter1(df):

    x = df['time delta'].dt.total_seconds()/60/60/24
    y = df['availability']
    plt.scatter(
        x,
        y,
        c=df['days until deadline'],
        cmap=plt.get_cmap('coolwarm_r')
    )

    plt.xticks(
        range(
            int(x.min())-1,
            int(x.max())+1
        )
    )

    plt.vlines(30, y.min(), y.max(), colors='lightgray',
               linestyles='dashed')
    plt.hlines(8, x.min(), x.max(), colors='lightgray',
               linestyles='dashed')

    cbar = plt.colorbar()
    cbar.set_ticks(range(int(df['days until deadline'].min())-1,
                         int(df['days until deadline'].max())+1))
    cbar.minorticks_on()
    cbar.set_label('Days from Time Checked Until Deadline', rotation=-90,
                   va='bottom')
    plt.xlabel('Days from Time Checked')
    plt.ylabel('Availability at Time Checked')
    plt.show()


def scatter2(df):

    fig, ax = plt.subplots()
    dfs = [
        df[
            df['days until deadline'] == day
        ] for day in df['days until deadline'].unique()
    ]
    for data_df in dfs:
        x = data_df['time delta'].dt.total_seconds()/60/60/24
        y = data_df['availability']
        ax.plot(
            x,
            y
        )

    #ax.xticks(
    #    range(
    #        int(x.min())-1,
    #        int(x.max())+1
    #    )
    #)

    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))

    plt.vlines(30, y.min(), y.max(), colors='lightgray',
               linestyles='dashed')
    plt.hlines(8, x.min(), x.max(), colors='lightgray',
               linestyles='dashed')

    plt.xlabel('Days from Time Checked')
    plt.ylabel('Availability at Time Checked')
    plt.show()


def heatmap(df):
    print(df)


df = pd.read_csv('permit_availability_hobbiton.csv')
print(df)

df['time checked'] = pd.to_datetime(df['time checked'])
df['time checked'] = df['time checked'] - timedelta(hours=3)
df['date'] = pd.to_datetime(df['date'], format='%b %d')
df['date'] = df['date'].apply(lambda x: x.replace(year=2020))

df['time delta'] = df['date'] - df['time checked']

deadline = dt.strptime('07-22-21 00:00:00', '%m-%d-%y %H:%M:%S')
df['days until deadline'] = ((deadline - df['time checked']).dt.total_seconds()/60/60/24)
#df['days until deadline'] = ((deadline - df['time checked']).dt.total_seconds()/60/60/24).astype(int)

scatter1(df)

