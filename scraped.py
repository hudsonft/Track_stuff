import requests as r
import re
from bs4 import BeautifulSoup
import pandas as pd
import os

"""
cciw page -> "leagues"
augustana -> "teams"
michael johnson -> "athletes"
NCAA DIII nationals -> "results"
-> "top performances"
"""
page_types = ['leagues']

class TfrrsWebPage(object):

    def __init__(self, url):

        self.url = re.sub('\s+', '', url)  # because tffrs is trash
        self.html_text = r.get(self.url).text
        self.soup = BeautifulSoup(self.html_text, 'html.parser')

        if "results" in self.url:
            self.page_type = "meet"
        elif "athletes" in self.url:
            self.page_type = "athlete"
        else:
            self.page_type = "other"


        self.title = self._get_title()
        self.tables = self._get_athlete_tables() if self.page_type == "athlete" else self._get_tables()

    def _get_title(self):
        title = self.soup.find('h3', class_="panel-title")
        title = title.text.strip()
        return title

    def _get_athlete_tables(self):
        tables = {}
        table_soups = self.soup.find_all('div', class_=re.compile('(tab-pane)'))
        for table_soup in table_soups:

            title = table_soup['id']
            athlete_page_table_columns = {"event-history": ["distance", "time", "meet", "date"],
                                          "meet-results": ["meet", "distance", "time", "place"],
                                          "season-history": ["season", "distance", "time", "meet", "date"],
                                          "progression": ["distance", "year", "time", "meet"]}


            sections = table_soup.find_all('table')
            for section in sections:
                section_header = section.find('thead').find('a').text

                table_rows = []
                row_data = [section_header]
                for cell in section.find_all('td'):
                    link = cell.find('a', href=True)
                    row_data.append((cell.text.strip(), 'https:' + link['href']) if link else cell.text.strip())
                table_rows.append(row_data)

            tables[title] = pd.DataFrame(table_rows, columns=athlete_page_table_columns[title])


    def _get_tables(self):
        tables = {}

        #body = self.soup.find_all('div', class_='panel-body').pop()
        table_soups = self.soup.find_all('div', class_=re.compile('(col-lg)'))

        table_headers = self.soup.find_all('th')

        for table_soup in table_soups:
            title = table_soup.find_all('h3')
            if len(title) < 1:
                continue
            elif len(title) > 1:
                raise Exception("Parse design error: more than one heading found in table (using tag h3)")

            title = title.pop().text
            if self.page_type == "meet":
                title = process_meet_result_table_titles(title)


            table_data = table_soup.find_all('table')
            assert len(table_data) == 1, "Parse design error: more than one table found (using tag table)"
            table_data = table_data.pop()

            col_titles = [col.text.strip() for col in table_data.find('thead').find_all('th')]
            table_rows = []
            for row in table_data.find('tbody').find_all('tr'):

                row_data = []
                for cell in row.find_all('td'):
                    link = cell.find('a', href=True)
                    row_data.append((cell.text.strip(), 'https:' + link['href']) if link else cell.text.strip())
                table_rows.append(row_data)

            tables[title] = pd.DataFrame(table_rows, columns=col_titles)

        return tables

    def to_csv(self, root_directory):

        page_folder_name = self.title.replace(" ", "_")
        data_dir = os.path.join(root_directory, page_folder_name)

        try:
            os.mkdir(data_dir)
        except FileExistsError:
            pass

        for table_name, table in self.tables.items():
            write_path = data_dir + '/' + table_name + '.csv'
            try:
                os.mkdir(data_dir)
            except FileExistsError:
                pass

            table.to_csv(write_path)


def process_meet_result_table_titles(title):
    # remove unwanted characters
    title = bytes(title, 'ascii', errors='ignore').decode('utf-8')
    title = re.sub('(\s+){2,}|(Top)|(\n)', '', title)

    gender = "Women's " if 'women' in title.lower() else "Men's "

    race_type = "Individual " if "individual" in title.lower() else "Team "

    open = "Open " if "open" in title.lower() else ""

    race_length = re.findall('\((.+)\)', title.lower()).pop()

    return "{g}{o}{t}{r}".format(g=gender, o=open, t=race_type, r=race_length)





