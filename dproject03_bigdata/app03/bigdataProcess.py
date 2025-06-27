from bs4 import BeautifulSoup
import requests
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from dproject03_bigdata.settings import STATIC_DIR
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np
import os

#  네이버 영화 차트
def movie_chart():
    # font_location="c:/Windows/fonts/malgun.ttf"
    # font_name=font_manager.FontProperties(fname=font_location).get_name()
    # rc('font',family=font_name)
    plt.rcParams['font.family']='Malgun Gothic'
    df = pd.read_csv('naver_movie.csv', encoding='utf-8-sig')
    print(df)
    ## 별점
    df['별점'] = np.floor(df['별점'].astype(float)).astype(int)
    plt.figure(figsize=(10,6))
    plt.bar(df['별점'].value_counts().index, df['별점'].value_counts(), color='blue')
    plt.title('네이버 영화 별점 분포')
    plt.xlabel('별점')
    plt.ylabel('영화개수')
    # os.path.join함수는 운영체제에 맞게 폴더 구분자를 다뤄서 경로를 생성
    plt.savefig(os.path.join(STATIC_DIR, 'images\\movie_naver_bar.png'),dpi=300)
    
    plt.cla()
    plt.pie(df['별점'].value_counts(), labels=df['별점'].value_counts().index, 
            autopct='%1.1f%%', startangle=90)
    plt.title('네이버 영화 별점 비율')
    plt.legend(title='별점', loc='upper right')
    plt.savefig(os.path.join(STATIC_DIR, 'images\\movie_naver_pie.png'),dpi=300)

    plt.cla()
    # 누적관객수가 20만명 넘는 것만 파이 그래프 출력
    df['누적관객수'] = df['누적관객수'].str.split(' ').str[2].str.extract(r'(\d+)').astype(int) 
    df_sample20 = df[df['누적관객수'] >20]
    plt.pie(df_sample20['누적관객수'].value_counts(),
        labels =df_sample20['누적관객수'].value_counts().index,
        autopct='%1.1f%%', startangle=90 )
    plt.title('네이버 영화 누적관객수(20만명 이상) 비율')

    plt.savefig(os.path.join(STATIC_DIR, 'images\\movie_count_pie.png'),dpi=300)
    image_dic = {'grade_bar' : 'movie_naver_bar.png',
                 'grade_pie' : 'movie_naver_pie.png' ,
                 'count_pie' : 'movie_count_pie.png'} 
    return image_dic



def movie_crawing(datas):
    driver = wd.Chrome()
    driver.implicitly_wait(2)

    driver.get('https://m.entertain.naver.com/movie')

    # '순위','제목','별점','누적관객수' 형태로  naver_movie.csv 파일로 저장

    boxOffice_btn = driver.find_element(By.XPATH, '//*[@id="feed-v2-renderer-root"]/div/div[1]/div[1]/div/div[2]/div/button[1]')
    boxOffice_btn.click()
    driver.implicitly_wait(2)
    more_btn = driver.find_element(By.XPATH, '//*[@id="feed-v2-renderer-root"]/div/div[1]/div[1]/div/div[4]/button')
    more_btn.click()

    driver.implicitly_wait(2)

    movies = driver.find_elements(By.XPATH, '//*[@id="feed-v2-renderer-root"]/div/div[1]/div[1]/div/div[3]/ol/li')
    # print(movies)
    # datas = []
    for movie in movies:
        rank = movie.find_element(By.CLASS_NAME,'Home_section_ranking_cover__HVOS9').find_element(By.TAG_NAME,'a').find_element(By.TAG_NAME,'span').text
        title = movie.find_element(By.CLASS_NAME, 'Home_section_ranking_cover__HVOS9').find_element(By.TAG_NAME,'a').find_element(By.CLASS_NAME,'Home_title__p5PQs').text
        grade =movie.find_element(By.CLASS_NAME, 'Home_section_ranking_cover__HVOS9').find_element(By.TAG_NAME,'a').find_element(By.CLASS_NAME,'Home_info__F-d1-').find_element(By.CLASS_NAME,'Home_number__0A85v').text
        custom_count =movie.find_element(By.CLASS_NAME, 'Home_section_ranking_cover__HVOS9').find_element(By.TAG_NAME,'a').find_element(By.CLASS_NAME,'Home_info__F-d1-').find_element(By.CLASS_NAME,'Home_count__R\+hm8').text
        datas.append([rank,title,grade,custom_count])
    df = pd.DataFrame(datas, columns=('순위', '제목','별점','누적관객수'))   
    df.to_csv('naver_movie.csv', encoding="utf-8-sig", index=False) 
    driver.quit() 




def melon_crawing(datas):
    header = {'User-Agent' : 'Mozilla/5.0'}
    req = requests.get('https://www.melon.com/chart/index.htm', headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    # print(soup)


    # 1~ 50  순위 앨범 곡정보
    #frm > div > table > tbody
    tbody = soup.select_one("#frm > div > table > tbody")
    #lst50
    trs = tbody.select('tr#lst50')

   
    for tr in trs[:10]:
        #lst50 > td:nth-child(2) > div > span.rank
        rank = tr.select_one('span.rank').get_text()
        #lst50 > td:nth-child(6) > div > div > div.ellipsis.rank01 > span > a
        name = tr.select_one('div.ellipsis.rank01 > span > a').get_text()
        #lst50 > td:nth-child(6) > div > div > div.ellipsis.rank02 > a
        singer = tr.select_one('div.ellipsis.rank02 > a').get_text()
        #lst50 > td:nth-child(7) > div > div > div > a
        album =  tr.select_one('div.rank03 > a').get_text()
        # datas.append([rank, name,singer,album])
        tmp = dict()
        tmp['rank'] = rank 
        tmp['song'] = name 
        tmp['singer'] = singer 
        tmp['ralbumank'] = album 
        datas.append(tmp)