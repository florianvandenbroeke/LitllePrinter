from bs4 import BeautifulSoup
import requests

url = requests.get("https://www.vrt.be/vrtnieuws/en.rss.articles.xml")

soup = BeautifulSoup(url.content, "lxml")
entries = soup.find_all('entry')

for entry in entries:
    title = entry.title.text
    summary = entry.summary.text
    link = entry.link['href']
    print(title)
    print(summary)
    print(link)