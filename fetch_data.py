import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
import gzip
import io
import xml.etree.ElementTree as ET

def fetch_data():
    url = 'http://prices.shufersal.co.il/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    # Find the number of pages
    footer = str(soup.find("tr", {"class": "webgrid-footer"}))
    pages = re.findall(r'href="(/\?page=\d+)"', footer)
    last_page = int(pages[-1].split('=')[1])

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/58.0.3029.110 Safari/537.3'}
    download_links = []
    dates = []
    locations = []
    categories = []
    df_expanded_price_list = []
    for i in range(1, 2):
        print(f'Page{i}')
        url = f"http://prices.shufersal.co.il/?page={i}"
        response = requests.get(url, headers=headers)
        soup = bs(response.text, 'html.parser')
        for row in soup.find_all('tr', class_=['webgrid-row-style', 'webgrid-alternating-row']):
            # Extract the values from each column in the row
            download_link = row.find('td').find('a')['href']
            date = row.find_all('td')[1].text
            location = row.find_all('td')[5].text
            category = row.find_all('td')[4].text

            if location == "" or "BE" in location or "GOOD MARKET" in location:
                continue
            if category != "price":
                continue

            try:
                response = requests.get(download_link)
                with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
                    xml_data = f.read()
                    tree = ET.fromstring(xml_data)
                    myArray = []
                    for elem in tree.iter('Item'):
                        ItemCode = elem.find('ItemCode').text
                        ItemName = elem.find('ItemName').text
                        ItemPrice = elem.find('ItemPrice').text
                        myArray.append([location, date, category, ItemCode, ItemName, ItemPrice])
                    df_xml = pd.DataFrame(myArray,
                                          columns=['location', 'date', 'category', 'ItemCode', 'ItemName', 'ItemPrice'])
                    df_expanded_price_list.append(df_xml)

                # Add the values to the appropriate list
                download_links.append(download_link)
                dates.append(date)
                locations.append(location)
                categories.append(category)
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
    df_expanded_price = pd.concat(df_expanded_price_list)
    df_expanded_price = df_expanded_price.reset_index(drop=True)
    df_expanded_price['branch_number'] = df_expanded_price.location.str.split(" - ", expand=True)[0]
    df_expanded_price['branch'] = df_expanded_price.location.str.split(" - ", expand=True)[1]
    df_expanded_price["date"] = pd.to_datetime(df_expanded_price["date"], format="%m/%d/%Y %I:%M:%S %p")
    df_expanded_price['date'] = df_expanded_price['date'].dt.date

    return df_expanded_price
