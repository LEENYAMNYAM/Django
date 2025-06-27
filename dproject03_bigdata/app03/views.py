from django.shortcuts import render
from app03 import bigdataProcess
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

# 멜론 노래 정보 수집
def melon(request):
    datas = []
    bigdataProcess.melon_crawing(datas)
    return render(request, 
                  'bigdata/melon1.html', 
                  {'data' : datas})
