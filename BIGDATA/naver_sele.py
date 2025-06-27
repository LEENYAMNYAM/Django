# https://m.entertain.naver.com/movie


from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
datas = []
for movie in movies:
    rank = movie.find_element(By.CLASS_NAME,'Home_section_ranking_cover__HVOS9').find_element(By.TAG_NAME,'a').find_element(By.TAG_NAME,'span').text
    title = movie.find_element(By.CLASS_NAME, 'Home_section_ranking_cover__HVOS9').find_element(By.TAG_NAME,'a').find_element(By.CLASS_NAME,'Home_title__p5PQs').text
    grade =movie.find_element(By.CLASS_NAME, 'Home_section_ranking_cover__HVOS9').find_element(By.TAG_NAME,'a').find_element(By.CLASS_NAME,'Home_info__F-d1-').find_element(By.CLASS_NAME,'Home_number__0A85v').text
    custom_count =movie.find_element(By.CLASS_NAME, 'Home_section_ranking_cover__HVOS9').find_element(By.TAG_NAME,'a').find_element(By.CLASS_NAME,'Home_info__F-d1-').find_element(By.CLASS_NAME,'Home_count__R\+hm8').text
    datas.append([rank,title,grade,custom_count])

df = pd.DataFrame(datas, columns=('순위', '제목','별점','누적관객수'))   
df.to_csv('naver_movie.csv', encoding="utf-8-sig", index=False) 

print(datas)   


### chart
plt.rcParams['font.family']='Malgun Gothic'
f, (ax1, ax2) = plt.subplots(1,2, figsize=(10,5))
df['별점'] = np.floor(df['별점'].astype(float)).astype(int)
ax1.bar(df['별점'].value_counts().index, df['별점'].value_counts(), color='blue')
ax1.set_title('네이버 영화 별점 분포')
ax1.set_xlabel('별점')
ax1.set_ylabel('영화개숫')

ax2.pie(df['별점'].value_counts(),
        labels =df['별점'].value_counts().index,
        autopct='%1.1f%%', startangle=90 )

plt.show()







