from bs4 import BeautifulSoup
import requests
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dproject03_bigdata.settings import STATIC_DIR, TEMPLATE_DIR
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from matplotlib import font_manager, rc
import numpy as np
import os, re, time, folium
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import pytagcloud
import pygame

# wordcloud
def wordcloud(data):

    # s = '좋은 아침이에요.안녕하세요'
    # m = re.search('^안녕', s)
    # print('m:', m)

    message = ''

    # message 중에서 문자만 가져옴
    # 정규표현식에서 ^는 문자열의 시작을 의미, 하지만 [] 안에서 사용하면 제외를 의미
    # [0-9] 숫자인 패턴 찾기, [^0-9]는 숫자 패턴 제외
    for item in data:
        if 'message' in item.keys():
            # message 안에서  
            message = message + re.sub(r'[^\w]', ' ', item['message'])+''

    # print('message : ', message)

    nlp = Okt()
    message_N = nlp.nouns(message)  # 명사만 추출
    count = Counter(message_N) # 명사 빈도수 계산

    word_dic = dict()
    for tag, counts in  count.most_common(80):
        if(len(str(tag)) > 1) :
           word_dic[tag] = counts
        #    print("%s : %d" % (tag, counts))

    font_location = "c:/Windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_location).get_name()
    rc('font', family=font_name)

    wc = WordCloud(font_path=font_location,
                    background_color='ivory',
                    width=800, height=600)
    cloud = wc.generate_from_frequencies(word_dic) # 빈도수로부터 워드클라우드 생성
    plt.figure(figsize=(5, 5))
    plt.imshow(cloud) # 워드클라우드 출력
    plt.axis('off') # 축 제거
    cloud.to_file(os.path.join(STATIC_DIR, 'images\\wordcloud.png')) # 이미지 저장

# wordcloud2
def wordcloud2(data):
    pygame.init()
    pygame.font.init()
    message = ''

    for item in data:
        if 'message' in item.keys():
            # message 안에서  
            message = message + re.sub(r'[^\w]', ' ', item['message'])+''

    # print('message : ', message)

    nlp = Okt()
    message_N = nlp.nouns(message)  # 명사만 추출
    count = Counter(message_N) # 명사 빈도수 계산

    word_dic = dict()
    for tag, counts in  count.most_common(80):
        if(len(str(tag)) > 1) :
           word_dic[tag] = counts
        #    print("%s : %d" % (tag, counts))

    taglist = pytagcloud.make_tags(word_dic.items(), maxsize=80) # 단어 빈도수로 워드클라우드 생성
    pytagcloud.create_tag_image(taglist,
                                os.path.join(STATIC_DIR, 'images', 'wordcloud2.png'),
                                size=(800, 600),
                                fontname='Nanum_Handwriting_Darui_Gweodo',
                                rectangular=False)

# wordcloud3(startbuck.csv)
def wordcloud3(data):
    pygame.init()
    pygame.font.init()
    message = ''

    for item in data:
        if 'message' in item.keys():
            # message 안에서  
            message = message + re.sub(r'[^\w]', ' ', item['message'])+''

    # print('message : ', message)

    nlp = Okt()
    message_N = nlp.nouns(message)  # 명사만 추출
    count = Counter(message_N) # 명사 빈도수 계산

    word_dic = dict()
    for tag, counts in  count.most_common(80):
        if(len(str(tag)) > 1) :
           word_dic[tag] = counts
        #    print("%s : %d" % (tag, counts))

    taglist = pytagcloud.make_tags(word_dic.items(), maxsize=80) # 단어 빈도수로 워드클라우드 생성
    pytagcloud.create_tag_image(taglist,
                                os.path.join(STATIC_DIR, 'images', 'wordcloud3.png'),
                                size=(800, 600),
                                fontname='Nanum_Handwriting_Darui_Gweodo',
                                rectangular=False)


#map
def map():
    ex = {'경도' : [127.061026,127.047883,127.899220,128.980455,127.104071,127.102490,127.088387,126.809957,127.010861,126.836078
                    ,127.014217,126.886859,127.031702,126.880898,127.028726,126.897710,126.910288,127.043189,127.071184,127.076812
                    ,127.045022,126.982419,126.840285,127.115873,126.885320,127.078464,127.057100,127.020945,129.068324,129.059574
                    ,126.927655,127.034302,129.106330,126.980242,126.945099,129.034599,127.054649,127.019556,127.053198,127.031005
                    ,127.058560,127.078519,127.056141,129.034605,126.888485,129.070117,127.057746,126.929288,127.054163,129.060972],
          '위도' : [37.493922,37.505675,37.471711,35.159774,37.500249,37.515149,37.549245,37.562013,37.552153,37.538927,37.492388
                    ,37.480390,37.588485,37.504067,37.608392,37.503693,37.579029,37.580073,37.552103,37.545461,37.580196,37.562274
                    ,37.535419,37.527477,37.526139,37.648247,37.512939,37.517574,35.202902,35.144776,37.499229,35.150069,35.141176
                    ,37.479403,37.512569,35.123196,37.546718,37.553668,37.488742,37.493653,37.498462,37.556602,37.544180,35.111532
                    ,37.508058,35.085777,37.546103,37.483899,37.489299,35.143421],
          '구분' : ['음식','음식','음식','음식','생활서비스','음식','음식','음식','음식','음식','음식','음식','음식','음식','음식'
                    ,'음식','음식','소매','음식','음식','음식','음식','소매','음식','소매','음식','음식','음식','음식','음식','음식'
                    ,'음식','음식','음식','음식','소매','음식','음식','의료','음식','음식','음식','소매','음식','음식','음식','음식'
                    ,'음식','음식','음식']}
    map_df = pd.DataFrame(ex)

    # 지도 중심 지정을 위해 위도, 경도 평균값 구하기
    first_lat = map_df['위도'][0]
    first_lon = map_df['경도'][0]

    # 지도 생성
    map = folium.Map(location=[first_lat, first_lon], zoom_start=12)

    for i in range(len(map_df)):
        folium.Marker(
            location=[map_df['위도'][i], map_df['경도'][i]],
            popup=map_df['구분'][i],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(map)
    
    # 지도 저장
    map.save(os.path.join(TEMPLATE_DIR, 'bigdata\\mapEx.html'))

#naver_map
def naver_map():
    
    df = pd.read_csv("data/starbucks.csv", encoding='cp949')
    
    # 필요한 열만 추출하여 리스트 구성
    data = [
        {'lat': row['위도'], 'lng': row['경도'], 'type': row['지점명']}
        for _, row in df.iterrows()
    ]

    client_id = 'q00681326d'

        # HTML 문자열 생성
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>네이버 지도 - 스타벅스 지점</title>
      <script type="text/javascript" src="https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId={client_id}"></script>
    </head>
    <body>
      <h2>스타벅스 지점 지도</h2>
      <div id="map" style="width:100%;height:600px;"></div>

      <script>
        var map = new naver.maps.Map('map', {{
          center: new naver.maps.LatLng({data[0]['lat']}, {data[0]['lng']}),
          zoom: 11
        }});

        var locations = {data};

        locations.forEach(function(loc) {{
          new naver.maps.Marker({{
            position: new naver.maps.LatLng(loc.lat, loc.lng),
            map: map,
            title: loc.type
          }});
        }});
      </script>
    </body>
    </html>
    """

    # HTML 파일 저장
    output_path = os.path.join(TEMPLATE_DIR, 'bigdata', 'naver_mapEx.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


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

#  네이버 영화 차트(DB이용)
def movie_dbchart(titles, points):
    font_location="c:/Windows/fonts/malgun.ttf"
    font_name=font_manager.FontProperties(fname=font_location).get_name()
    rc('font',family=font_name)

    plt.cla()
    plt.ylabel('영화평점평균')
    plt.xlabel('영화제목')
    plt.title('네이버 TOP10 영화 평점 평균')
    plt.bar(range(len(titles)), points, color='blue', align='center')
    plt.xticks(range(len(titles)), list(titles), rotation=30, fontsize=5)
    plt.savefig(os.path.join(STATIC_DIR, 'images\\movie_db_fg.png'), dpi=300)

    

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

def baseball_crawing(datas):
    options = Options()
    options.add_argument("--headless")  # 창 없이 실행
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = wd.Chrome(options=options)

    url = "https://m.sports.naver.com/kbaseball/record/kbo?seasonCode=2025&tab=teamRank"
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup)
    driver.quit()

    # 순위 팀명 경기 승 무 패 승률 연속승패 최근경기
    tbody = soup.select_one('.record_table_group')
    if not tbody:
        print("'.record_table_group'를 찾을 수 없습니다.")
        return
    trs = tbody.select('li.TableBody_item__eCenH')

    for tr in trs:
        try : 
            rank = tr.select_one('em.TeamInfo_ranking__MqHpq').text.strip()
            team = tr.select_one('div.TeamInfo_team_name__dni7F').text.strip()
            values = tr.select('div.TextInfo_text__ysEqh')

            def clean(tag):
                return ''.join(t for t in tag.contents if isinstance(t, str)).strip()
            
            rate = clean(values[0])
            game_behind = clean(values[1])
            win = clean(values[2])
            draw = clean(values[3])
            lose = clean(values[4])
            total_game = clean(values[5])
            streak = clean(values[6])

            tmp = dict()
            tmp['rank'] = rank 
            tmp['team'] = team 
            tmp['win'] = win 
            tmp['lose'] = lose 
            tmp['draw'] = draw 
            tmp['total_game'] = total_game
            tmp['rate'] = rate 
            tmp['streak'] = streak 
            tmp['game_behind'] = game_behind 

            datas.append(tmp)
        except Exception as e:
            print(f"크롤링 실패 : {e}")
            continue        