from django.shortcuts import render,redirect
from app03 import bigdataProcess


from django.contrib.auth import authenticate, login
from .form import UserForm
from .models import Movie
from django.db.models.aggregates import Avg 
import pandas as pd

# Create your views here.

def home(request):
    return render(request,'base.html' )

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
    print('movie_db')
   
    df = pd.read_csv('naver_movie.csv', index_col='순위', encoding='utf-8-sig')
    print(df)
    for index, row in df.iterrows():
        # print(r)
        moive = Movie(rank = index,
                      title = row['제목'],
                      grade = row['별점'],
                      custom_count = row['누적관객수'] )
        moive.save()
    return redirect('/') 

# 네이버 영화 차트
def movie_dbchart(request):
   # movie  테이블에서 제목(title)에 해당하는 평점(grade) 평균을 구하기
   data = Movie.objects.values('title').annotate(avg_grade=Avg('grade'))[0:10]
   print('data query:', data.query) # sql문 확인
   df = pd.DataFrame(data)
   bigdataProcess.movie_dbchart(df.title, df.avg_grade)
   return render(request, 
                 'bigdata/moviedb.html',
                 {"data" : data ,
                  "image_data" : 'movie_db_fig.png'} )   

  

# 멜론 노래 정보 수집
def melon(request):
    datas = []
    bigdataProcess.melon_crawing(datas)
    return render(request, 
                  'bigdata/melon1.html', 
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
