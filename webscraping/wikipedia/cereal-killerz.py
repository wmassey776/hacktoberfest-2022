#!/usr/bin/env python3

import csv

from requests_html import HTMLSession
URL = 'https://en.wikipedia.org/wiki/List_of_serial_killers_in_the_United_States'


def save_to_csv(data):
    with open('serial-killers.csv', 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Rank', 'Title', 'Year', 'Rating'])
        writer.writerows(data)


def scrape_site(url):
    session = HTMLSession()
    page = session.get(url)

    records = []

    table_rows = page.html.find('tbody', first=True).find('tr')

    for col in table_rows[1:]:
        name = [t.text for t in col.find('td')][0]
        activeYears = [t.text for t in col.find('td')][1]
        provenVictims = [t.text for t in col.find('td')][2]
        possibleVictims = [t.text for t in col.find('td')][3]
        status = [t.text for t in col.find('td')][4]
        notes = [t.text for t in col.find('td')][5]
        record = (name, activeYears, provenVictims, possibleVictims, status, notes)
        records.append(record)
    return records


scraped_data = scrape_site(URL)
save_to_csv(scraped_data)
