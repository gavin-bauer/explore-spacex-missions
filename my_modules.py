# -*- coding: utf-8 -*-
import requests
from io import BytesIO
from PIL import Image
import json
import math
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import os
import codecs

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name)
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

def process_landing_data(data):
    landings_records = []
    for index in range(len(data)):
        row = flatten_json(data[index]['rocket']['first_stage']['cores'])
        row['flight_number'] = data[index]['flight_number']
        row['rocket_name'] = data[index]['rocket']['rocket_name']
        row['launch_year'] = data[index]['launch_year']
        row['launch_success'] = data[index]['launch_success']
        landings_records.append(row)
    return landings_records

def process_payloads_data(data):
    payloads_records = []
    for index in range(len(data)):
        row = flatten_json(data[index]['rocket']['second_stage']['payloads'])
        row['flight_number'] = data[index]['flight_number']
        row['rocket_name'] = data[index]['rocket']['rocket_name']
        row['launch_year'] = data[index]['launch_year']
        row['launch_success'] = data[index]['launch_success']
        payloads_records.append(row)
    return payloads_records

def is_success_or_failure(element):
    if element == True:
        return 'Success'
    elif element == False:
        return 'Failure'

def load_data(url):
    response = requests.get(url)
    data = response.json()
    landings_records = process_landing_data(data)
    landings = json_normalize(landings_records).dropna(subset=['launch_success'])
    payloads_records = process_payloads_data(data)
    payloads = json_normalize(payloads_records).dropna(subset=['launch_success'])
    df = json_normalize(data)
    df['launch_success_or_failure'] = df['launch_success'].map({True:'Success', False:'Failure'})
    landings['reflown_or_first_flight'] = landings['reused'].map({True:'Reflown', False:'First flight'})
    return df, landings, payloads

def stacked_bar(df, cols, ylabel, title):
    extract = df[cols]
    data = extract.groupby(cols)['launch_year'].count().unstack().fillna(0)
    ax = data.plot(kind='bar', stacked=True, title=title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Years")
    ax.legend(loc="upper left")
    yint = range(0, math.ceil(len(ylabel))+1, 2)
    plt.yticks(yint)

def stacked_payloads(df, cols):
    # ETL
    extract = df[cols]
    grouped = extract.groupby(['launch_year', 'orbit'], as_index=False).sum()
    pivoted = grouped.pivot(index='launch_year', columns='orbit', values='payload_mass_kg').fillna(0)
    thresh = pivoted.sum(axis=0).mean()
    others = pivoted[pivoted.columns[pivoted.sum(axis=0) <= thresh]].sum(axis=1).rename('OTHERS')
    majors = pivoted[pivoted.columns[pivoted.sum(axis=0) > thresh]]
    to_plot = pd.concat([majors, others], axis='columns')
    # plot
    GTO = to_plot['GTO']
    ISS = to_plot['ISS']
    PO = to_plot['PO']
    VLEO = to_plot['VLEO']
    OTHERS = to_plot['OTHERS']
    years = to_plot.index
    ind = np.arange(to_plot.shape[0])
    plt.bar(ind, GTO, width=0.6, label='GTO', bottom=OTHERS+VLEO+PO+ISS)
    plt.bar(ind, ISS, width=0.6, label='ISS', bottom=OTHERS+VLEO+PO)
    plt.bar(ind, PO, width=0.6, label='PO', bottom=OTHERS+VLEO)
    plt.bar(ind, VLEO, width=0.6, label='VLEO', bottom=OTHERS)
    plt.bar(ind, OTHERS, width=0.6, label='OTHERS')
    plt.xticks(ind, years)
    plt.ylabel("Payload mass (kg)")
    plt.xlabel("Years")
    plt.legend(loc="upper left")
    plt.title("Payload Upmass by Orbit")
    return plt.show()

def load_img(IMG_URL):
    response = requests.get(IMG_URL)
    image = Image.open(BytesIO(response.content))
    return image

def scrape_wikipedia_table(wikipage):
    wiki = wikipage
    header = {
    'User-Agent': 'Mozilla/5.0'
    }  # needed to prevent 403 error on Wikipedia
    page = requests.get(wiki, headers=header)
    soup = BeautifulSoup(page.content)

    #tables = soup.findAll("table", {"class": "wikitable"}) # scrape all tables
    tables = soup.findAll("table", {"class": "infobox hproduct"}) # scrape infobox only

    for tn, table in enumerate(tables):

        # preinit list of lists
        rows = table.findAll("tr")
        row_lengths = [len(r.findAll(['th', 'td'])) for r in rows]
        ncols = max(row_lengths)
        nrows = len(rows)
        data = []
        for i in range(nrows):
            rowD = []
            for j in range(ncols):
                rowD.append('')
            data.append(rowD)

        # process html
        for i in range(len(rows)):
            row = rows[i]
            rowD = []
            cells = row.findAll(["td", "th"])
            for j in range(len(cells)):
                cell = cells[j]

                # deal with cells span cols and rows
                cspan = int(cell.get('colspan', 1))
                rspan = int(cell.get('rowspan', 1))
                l = 0
                for k in range(rspan):
                    # shifts to the first empty cell of this row
                    while data[i + k][j + l]:
                        l += 1
                    for m in range(cspan):
                        cell_n = j + l + m
                        row_n = i + k
                        # in some cases the colspan can overflow the table, in those cases just get the last item
                        cell_n = min(cell_n, len(data[row_n])-1)
                        data[row_n][cell_n] += cell.text

            data.append(rowD)

        # write data out to tab seperated format
        df = pd.DataFrame(data, columns=data[0])
        df = df.drop([0])
        df = df.dropna()
        return df
