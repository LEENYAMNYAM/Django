from django.shortcuts import redirect, render
from app03 import bigdataProcess

import pandas as pd
from .models import Movie
from django.db.models.aggregates import Avg
import json

from django.contrib.auth import authenticate, login
from .form import UserForm

# Create your views here.

def home(request):
    return render(request,'base.html' )

def wordcloud(request):
    path = 'D:/JMT/Django/workspace/dproject03_bigdata/data'
    data = json.loads(open(path + '/4차 산업혁명.json', encoding='utf-8').read())
    print('wordcloud : ', data)
    
    bigdataProcess.wordcloud(data)
    return render(request, 
                  'bigdata/wordcloud.html', 
                  {'image_data' : 'wordcloud.png'} )

def wordcloud2(request):
    path = 'D:/JMT/Django/workspace/dproject03_bigdata/data'
    data = json.loads(open(path + '/4차 산업혁명.json', encoding='utf-8').read())
    print('wordcloud : ', data)
    
    bigdataProcess.wordcloud2(data)
    return render(request, 
                  'bigdata/wordcloud.html', 
                  {'image_data' : 'wordcloud2.png'} )

def wordcloud3(request):
    path = 'D:/JMT/Django/workspace/dproject03_bigdata/data'
    df = pd.read_csv(path +"/starbucks.csv", encoding='cp949')
    print('wordcloud : ', df)
    print('df.columns : ', df.columns)
    
    data = [{'message': f"{row['지점명']} {row['주소']}"} for idx, row in df.iterrows()]
    
    bigdataProcess.wordcloud3(data)
    return render(request, 
                  'bigdata/wordcloud.html', 
                  {'image_data' : 'wordcloud3.png'} )

def map(request):
    bigdataProcess.map()
    return render(request, 'bigdata/map.html')

def naver_map(request):
    bigdataProcess.naver_map()
    return render(request, 'bigdata/naver_map.html')

# 네이버 영화 차트
def movie_chart(request):
   image_dic = bigdataProcess.movie_chart()
   return render(request, 
                 'bigdata/moviechart.html',
                 {"image_data" : image_dic} )

# 네이버 영화 정보 수집
def movie(request):
    datas = []
    bigdataProcess.movie_crawing(datas)
    print('datas :' , print(datas)     )     
    return render(request, 
                  'bigdata/movie.html', 
                  {'data' : datas})

# 네이버 영화 정보 수집(DB)
def movie_db(request):
    # 이미크롤링으로 생성된 csv 파일이 있다는 전제하에 진행
    df = pd.read_csv('naver_movie.csv', index_col='순위', encoding='utf-8-sig')
    print("칼럼명 : ", df.columns.tolist())

    for index, r in df.iterrows():
        print('r : ', r)
        # Movie 모델에 저장
        movie = Movie(rank=index, 
                title=r['제목'], 
                grade=r['별점'], 
                custom_count=r['누적관객수'])
        movie.save()
    return redirect('/')

# 네이버 영화 차트
def movie_dbchart(request):
    # movie 테이블에서 제목(title)에 해당하는 평점(grade) 평균을 구하기
    data = Movie.objects.values('title').annotate(avg_grade=Avg('grade'))[0:10]

    print('data query : ', data.query)
    df = pd.DataFrame(data)
    image_dic = bigdataProcess.movie_dbchart(df.title, df.avg_grade)
    return render(request, 
                 'bigdata/moviedb.html',
                 {"data" : data,
                  "image_data" : 'movie_db_fg.png'} )


# 멜론 노래 정보 수집
def melon(request):
    datas = []
    bigdataProcess.melon_crawing(datas)
    return render(request, 
                  'bigdata/melon1.html', 
                  {'data' : datas})

# 야구 순위 정보 수집
def baseball_rank(request):
    datas = []
    bigdataProcess.baseball_crawing(datas)
    return render(request, 
                  'bigdata/baseball_rank.html', 
                  {'data' : datas})

############
#  sing up

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)   #import
        if form.is_valid():
            print('signup POST is_valid')
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  #import
            login(request,user)
            return redirect('/')
        else:
            print('signup POST un_valid')
    else:
        form = UserForm()
       
    return render(request,'common/signup.html',{'form':form}) 
