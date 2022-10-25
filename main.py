

import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get("https://www.charlesbordet.com/fr/blog/#")
soup = BeautifulSoup(r.content, 'html.parser')
url_list = []
for ligne in soup.find_all('h2'):
    url = ligne.a["href"]
    url_list.append(url)

description_lists = []
for i in soup.find_all(class_='archive__item-excerpt'):
    description_lists.append(i.text.strip())

result_lists = []
for index in range(len(url_list)):
    r = requests.get(f"https://www.charlesbordet.com{url_list[index]}")
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find(class_="titre-article").get_text().strip()
    reading_time = soup.find(class_="page__meta").get_text().strip()
    summary = []
    for i in soup.find(class_="toc__menu").find_all('li'):
        if i != None:
            summary.append(i.a.text)
    result_lists.append([title, description_lists[index], reading_time, summary])

df = pd.DataFrame(result_lists)
df.columns = ['Article_name', 'descriptions', 'reading_time', 'summary_list']
df.to_csv("article.csv")



