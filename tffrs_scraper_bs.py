"""
Parses tables on a tffrs page into into csvs.
"""

from bs4 import BeautifulSoup
import requests as r
import pandas as pd
import re
import os

#url= 'https://www.tfrrs.org/results/xc/13454/Spartan_Classic_-_Aurora_Unversity'
# url = 'https://www.tfrrs.org/top_performances/IL_college_m_Wheaton_IL.html?list_hnd=2278&season_hnd=414'
#url = 'https://www.tfrrs.org/lists/2209/CCIW_Outdoor_Performance_List/2018/o'




def dfs_to_csv(url):
    title, tables = tables_to_dfs(url)

    root_directory = '/Users/hudsonthomas/Desktop/Tffrs_data/'
    data_dir = root_directory + title
    try:
        os.mkdir(data_dir)
    except FileExistsError:
        pass

    for table_name, table in tables.items():
        write_path = data_dir + '/' + table_name + '.csv'

        table.to_csv(write_path)


def get_title(url):
    html_doc = r.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    title = soup.find_all('div', class_="panel-heading")
    assert len(title) == 1
    title = title.pop().text.strip()
    return title


def tables_to_dfs(url):
    dfs = {}
    html_doc = r.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    body = soup.find_all('div', class_='panel-body').pop()
    tables = body.find_all('div', class_=re.compile('(col-lg)'))

    for table in tables:
        table_title = table.find_all('h3').pop().text
        table_data = table.find_all('table').pop()

        col_titles = [col.text.strip() for col in table_data.find('thead').find_all('th')]
        table_rows = []
        for row in table_data.find('tbody').find_all('tr'):

            row_data = []
            for cell in row.find_all('td'):
                link = cell.find('a', href=True)
                row_data.append((cell.text.strip(), 'https:' + link['href']) if link else (cell.text.strip(), None))
            table_rows.append(row_data)

        df = pd.DataFrame(table_rows, columns=col_titles)
        dfs[table_title] = df
    return dfs


# url = 'https://www.tfrrs.org/results/xc/13454/Spartan_Classic_-_Aurora_Unversity'
url = "https://www.tfrrs.org/leagues/1398.html"
tables = tables_to_dfs(url)

mens_teams = tables['TEAMS']['MEN\'S TEAM']

for team, team_url in mens_teams:
    team_data = tables_to_dfs(team_url)
    # TODO: fix table heading parsing. Should be "ROSTER" instead of "TOP MARKS"
    runners = team_data['ROSTER']['NAME']

    for runner, runner_url in runners:
        a = 1


