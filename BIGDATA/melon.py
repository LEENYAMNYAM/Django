import requests
from bs4 import BeautifulSoup


# 크롤링가능여부 : 사이트/robots.txt
header = {'User-Agent' : 'Mozilla/5.0'}
req = requests.get('https://www.melon.com/chart/index.htm', headers=header)
soup = BeautifulSoup(req.text, 'html.parser')
print(soup)


# 1~ 50  순위 앨범 곡정보
#frm > div > table > tbody
tbody = soup.select_one("#frm > div > table > tbody")
#lst50
trs = tbody.select('tr#lst50')

datas = []
for tr in   trs[:10]:
    #lst50 > td:nth-child(2) > div > span.rank
    rank = tr.select_one('span.rank').get_text()
    #lst50 > td:nth-child(6) > div > div > div.ellipsis.rank01 > span > a
    name = tr.select_one('div.ellipsis.rank01 > span > a').get_text()
    #lst50 > td:nth-child(6) > div > div > div.ellipsis.rank02 > a
    singer = tr.select_one('div.ellipsis.rank02 > a').get_text()
    #lst50 > td:nth-child(7) > div > div > div > a
    album =  tr.select_one('div.rank03 > a').get_text()
    datas.append([rank, name,singer,album])

print(datas)    


