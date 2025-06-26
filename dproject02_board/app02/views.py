from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from app02.models import Board, Comment
import urllib.parse
import math
from .form import UserForm

# Create your views here.
UPLOAD_DIR = "D:\\JMT\\Django\\workspace\\upload"

# 회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print("signup POST unvalid")
    else:
        form = UserForm()

    return render(request, 'common/signup.html', {'form' : form})

def home(request):
    return render(request, 'base.html')

# write_form
def write_form(request):
    return render(request, 'board/insert.html')


# insert
@csrf_exempt
def insert(request):
    fname =''
    fsize = 0

    if 'file' in request.FILES:
        file = request.FILES['file']
        fname = file.name
        fsize = file.size

        fp = open('%s%s' %(UPLOAD_DIR, fname) ,'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()    


    board = Board(writer=request.POST['writer'],
              title=request.POST['title'] ,
              content=request.POST['content'] ,
              filename = fname,
              filesize = fsize)
    board.save()

    return redirect('/list')

# list_page
def list_page(request):
    page = request.GET.get('page', 1)
    word = request.GET.get('word', '')

    boardCount = Board.objects.filter(
        Q(writer__contains = word)|
        Q(title__contains = word)|
        Q(content__contains = word)).count()
    
    boardList = Board.objects.filter(
        Q(writer__contains = word)|
        Q(title__contains = word)|
        Q(content__contains = word)).order_by('-id')

    # 페이징 처리
    pageSize = 5

    paginator = Paginator(boardList, pageSize)
    page_obj = paginator.get_page(page)
    print('page_obj : ', page_obj)
    print('boardCount : ', boardCount)
    context = {
        'boardCount' : boardCount,
        'page_list' : page_obj,
        'word' : word
    }

    return render(request, 'board/list_page.html', context)

# list
def list(request):
    page = request.GET.get('page',1)
   
    boardCount = Board.objects.count()

   # 123[다음] [이전]456[다음] [이전] 7 
    pageSize = 5
    blockPage = 3
    currentPage = int(page)
    start = (currentPage-1)*pageSize
    boardList = Board.objects.all().order_by('-id')[start:start+pageSize]
    # 총페이지
    totPage = math.ceil(boardCount/pageSize)  # 7
    # 블럭의 시작페이지
    startPage = math.floor((currentPage-1)/blockPage)*blockPage +1

    # 블럭의 마지막페이지
    endPage = startPage + blockPage -1  # 7 8 9   endPage=9
    if endPage > totPage :
        endPage = totPage
 
    return render(request, 'board/list.html', {
        'blist'  : boardList,
        'bcount' : boardCount,
        'startPage' : startPage,
        'endPage':endPage,
        'totPage' : totPage,
        'currentPage' : currentPage,
        'blockPage' : blockPage,
        'range' : range(startPage, endPage+1)
    })

# 상세보기
def detail(request, board_id):
    board = Board.objects.get(id = board_id)
    board.hit_up() # 조회수 증가
    board.save()

    return render(request,
                  'board/detail.html',
                   {'board' : board})

# 삭제
def delete(request,board_id):
    Board.objects.get(id=board_id).delete()
    return redirect("/list/") 
# 수정 폼
def update_form(request,board_id):
    board =Board.objects.get(id=board_id)
    return render(request,'board/update.html', 
                  {'board': board})

# 수정
@csrf_exempt
def update(request):
    id = request.POST['id']
    board =Board.objects.get(id=id)
    fname = board.filename
    fsize = board.filesize
    if 'file' in request.FILES:
        file = request.FILES['file']
        fname = file.name
        fsize = file.size
        fp = open('%s%s' %(UPLOAD_DIR,fname),'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

    update_board = Board(id,
                         writer = request.POST['writer'],
                         title  = request.POST['title'],
                         content = request.POST['content'],
                         filename = fname,
                         filesize = fsize  )     
    update_board.save()   

    return redirect("/list/") 

##############

def  download_count(request):
    id = request.GET['id']
    board = Board.objects.get(id=id)
    board.down_up() # 다운로드 횟수 1증가
    board.save()
    count = board.down # 다운로드 수

    return  JsonResponse({'count' : count , 'id' : id})


# 다운로드
def download(request):
    id = request.GET['id']

    board = Board.objects.get(id=id)
    path = UPLOAD_DIR+board.filename
    filename = urllib.parse.quote(board.filename)

    with open (path, 'rb') as file:
        response = HttpResponse(file.read(),
          content_type='application/octet-stream')
    response['Content-Disposition']="attachment;filename*=UTF-8''{0}".format(filename)

    return  response  

#### comment insert
@csrf_exempt
def comment_insert(request):
    id = request.POST['id']
    # comment = Comment(writer='aa',
    #                   board_id = id,
    #                   content = request.POST['content'])
    board = Board.objects.get(id=id)
    comment = Comment(writer='aa', 
                      board =board,
                      content = request.POST['content'] )
    comment.save()
    return redirect('/detail/'+id)







