#CSE 3104 Final Project: Coded By Owen, Aleyda, Fred

#libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

pd.set_option('display.max_rows', None)



#header to alert of scraping
headers = {
  "User-Agent": "Student/Practicing_Web_Scraping_WASHU_CSE3104"
}
#genreally working with Wikipedia
general_url = "https://en.wikipedia.org"

#Funct opens each individual page of the URL from the dataframe, then it finds the person who
def add_director(movies):
    directors = []
    for index, row in movies.iterrows():
        time.sleep(1)
        url = row["url"]
        res = requests.get(url, headers=headers)
        #finds table headers for directed by, then finds the table data if that exists
        soup = BeautifulSoup(res.text, "html.parser")
        label = soup.find('th', string='Directed by')
        if label and label.find_next_sibling('td'):
            director = label.find_next_sibling('td').text.strip()
        else:
            director = "Unknown"
        directors.append(director)
        print(director)
    movies['director'] = directors
    return movies

# #Scrapes all movies recorded by Wikipedia in a specific year.
def scrape_movies(year: int, general_url: str):
    movies = []
    url = "https://en.wikipedia.org/wiki/Category:" + str(year) + "_films"
    i = 0
    #reads movies through the first URL, then follows the next page button to move through subsequent pages
    while url:
        res = requests.get(url, headers = headers)
        print(res)
        soup = BeautifulSoup(res.text, "html.parser")
        #Locates the list of movies on the speciic page
        for li in soup.select("#mw-pages li"):
            title = li.text.strip()
            link = general_url + li.find("a")["href"]
            #Puts each movie in dict.
            movies.append({
                "title": title,
                "url": link
            })
        #Finds the next destination by finding the next page button
        next_link = soup.find("a", string="next page")

        #determmines if the next page exists or not
        if next_link:
            next_link = next_link["href"]
            url = general_url + next_link
            time.sleep(1)
        else:

            url = None
        #counts pages, returns how many pages were scraped and then turns dict into DF
        i = i + 1
    print(i)
    df = pd.DataFrame(movies)
    print("Year " + str(year) + " Scraped, " + str(i) + " pages")
    return(df)

#Cycles through years after 2020 to create a df and csv for each

for i in range(3, 6):
    df = pd.DataFrame()
    value = 2020+i
    df_new = scrape_movies(value, general_url)
    df_new['year'] = value
    df = pd.concat([df, df_new])
    add_director(df).to_csv("results_" + str(value) + ".csv")



#Creates a final Df with directors for each movie name.
df_2020 = pd.read_csv("results_2020.csv")
df_2021 = pd.read_csv("results_2021.csv")
df_2022 = pd.read_csv("results_2022.csv")
df_2023 = pd.read_csv("results_2023.csv")
df_2024 = pd.read_csv("results_2024.csv")
df_2025 = pd.read_csv("results_2025.csv")

results = pd.concat([df_2025, df_2024, df_2023, df_2022, df_2021, df_2020])

results.to_csv("results.csv")