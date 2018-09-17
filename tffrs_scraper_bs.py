from bs4 import BeautifulSoup
import requests as r
import pandas as pd
import re
import os
url= 'https://www.tfrrs.org/results/xc/13454/Spartan_Classic_-_Aurora_Unversity'
#url = 'https://www.tfrrs.org/top_performances/IL_college_m_Wheaton_IL.html?list_hnd=2278&season_hnd=414'
#url = 'https://www.tfrrs.org/lists/2209/CCIW_Outdoor_Performance_List/2018/o'
html_doc = r.get(url).text
soup = BeautifulSoup(html_doc, 'html.parser')

tables = soup.find_all('table')

# get headings
headings = [' '.join(re.findall(r'[A-Za-z0-9\.\:\-\(\)\," "]+', title.text.strip())) for title in soup.find_all('h3')]
title = headings.pop(0)

root_directory = '/Users/hudsonthomas/Desktop/Tffrs_data/'
data_dir = root_directory + title
try:
    os.mkdir(data_dir)
except FileExistsError:
    pass

headings = [name for name in headings if 'Note' not in name]

for table_name, table_data in zip(headings, tables):

    col_titles = [col.text.strip() for col in table_data.find('thead').find_all('th')]
    table_rows = []
    for row in table_data.find('tbody').find_all('tr'):
        table_rows.append([cell.text.strip() for cell in row.find_all('td')])

    df = pd.DataFrame(table_rows, columns=col_titles)

    write_path = data_dir +'/' + table_name + '.csv'

    df.to_csv(write_path)


