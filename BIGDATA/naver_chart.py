import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('naver_movie.csv', encoding='utf-8-sig')
print(df)

####
plt.rcParams['font.family']='Malgun Gothic'
f, ((ax1, ax2),(ax3,ax4)) = plt.subplots(2,2, figsize=(15,10))
## 별점
df['별점'] = np.floor(df['별점'].astype(float)).astype(int)
ax1.bar(df['별점'].value_counts().index, df['별점'].value_counts(), color='blue')
ax1.set_title('네이버 영화 별점 분포')
ax1.set_xlabel('별점')
ax1.set_ylabel('영화개수')

ax2.pie(df['별점'].value_counts(),
        labels =df['별점'].value_counts().index,
        autopct='%1.1f%%', startangle=90 )

## 누적수
# df['누적관객수'] =df['누적관객수'].str.split(' ').str[2].str.replace('만명','').astype(int) 
# 공백으로 구분한 후 2번째 문자에서 숫자만 추출
df['누적관객수'] = df['누적관객수'].str.split(' ').str[2].str.extract(r'(\d+)').astype(int) 
print(df['누적관객수'])
ax3.bar(df['누적관객수'].value_counts().index, df['누적관객수'].value_counts(), color='green')
ax3.set_title('네이버 영화 누적관객수 분포')
ax3.set_xlabel('누적관객수')
ax3.set_ylabel('영화개수')

ax4.pie(df['누적관객수'].value_counts(),
        labels =df['누적관객수'].value_counts().index,
        autopct='%1.1f%%', startangle=90 )
plt.show()