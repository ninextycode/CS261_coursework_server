import bs4
import requests
from datetime import datetime

class StockDataScrapper:
    def split_string(self, s, start, end):
        return (s.split(start))[1].split(end)[0].strip()

    def scrape_stocks_data(self, url):
        response = requests.get(url)
        if(response.status_code == 200):
            soup = bs4.BeautifulSoup(response.content, "lxml")
            table = soup.findAll(attrs={"summary" : "Companies and Prices"})[0]
            body = table.find('tbody')
            rows = body.findAll('tr')
            time = str(datetime.now())
            arr = []
            for r in rows:
                data = r.findAll('td')
                code = data[0].string
                name = data[1].findChildren()[0].string
                current = data[2].string
                price = data[3].string.replace(',','')
                diff = self.split_string(str(data[4]), '">', "<")
                per_diff = data[5].string.strip()
                curr = [code,name,current,price,diff,per_diff,time]
                arr.append(curr)
            return arr
