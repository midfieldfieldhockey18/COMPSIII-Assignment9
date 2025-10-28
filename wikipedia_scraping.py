import requests
from bs4 import BeautifulSoup
import re
import sqlite3
connection = sqlite3.connect('movies.db')
cursor = connection.cursor()

cursor.execute('''DROP TABLE IF EXISTS movies;''')

cursor.execute('''
CREATE TABLE movies (
    title TEXT,
    worldwide_gross INTEGER,
    year INTEGER
);
''')
def scrape_wikipedia():
    url = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"class": "wikitable"})
    rows = table.find_all("tr")

    movies = []
    for row in rows[1:]:  # skip header
        cols = row.find_all(["th", "td"])
        if len(cols) >= 3:
            title = cols[1].get_text(strip=True)
            worldwide_gross = cols[2].get_text(strip=True)
            year = cols[-1].get_text(strip=True)

            # Clean data
            worldwide_gross = re.sub(r'[^0-9]', '', worldwide_gross)
            if worldwide_gross:
                worldwide_gross = int(worldwide_gross)
            else:
                worldwide_gross = 0

            movies.append({
                "title": title,
                "worldwide_gross": worldwide_gross,
                "Year": int(year)
            })
    return movies
movie_data = scrape_wikipedia()

for movie in movie_data:
    cursor.execute('''
        INSERT INTO movies (title, worldwide_gross, year)
        VALUES (?, ?, ?);
    ''', (movie['title'], movie['worldwide_gross'], movie['Year']))
connection.commit()



