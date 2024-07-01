from bs4 import BeautifulSoup
import requests

url = requests.get("https://www.vrt.be/vrtnieuws/nl.rss.articles.xml")

soup = BeautifulSoup(url.content, "xml")
entries = soup.find_all('entry')

titles = [entry.title.text for entry in entries]
summaries = [entry.summary.text for entry in entries]
items = [(entry.title.text, entry.summary.text) for entry in entries]

print(items)

# for entry in entries:
#     title = entry.title.text
#     summary = entry.summary.text
#     link = entry.link['href']
#     print(title)
#     print(summary)
#     print(link)