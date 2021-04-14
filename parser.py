from bs4 import BeautifulSoup
import requests
url = 'https://donetskafisha.ru/kurs-dollara-i-grivny-v-dnr/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
page = requests.get(url, headers = headers)
new_li = []
new_news = []
news = []
soup = BeautifulSoup(page.text, "html.parser")
news = soup.findAll('div', class_='uncode_text_column')
string = ''
def valut(string):
    for i in range(len(news)):
        if news[i].find('span', class_='uk-text-large') is not None:
            new_news.append(news[i].text)
    for i in range(len(new_news)):
        print(new_news[i].strip())
        string += str(new_news[i].strip())
        
    return string
print(valut(string))
