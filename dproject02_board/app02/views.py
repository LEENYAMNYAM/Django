from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from app02.models import Board, Comment
import urllib.parse
from django.http.response import JsonResponse, HttpResponse

# Create your views here.
UPLOAD_DIR = "D:/JMT/Django/workspace/dproject02_board/static/images"

def home(request):
    return render(request, 'base.html')

# write_form
def write_form(request):
    return render(request, 'board/insert.html')

# insert
@csrf_exempt
def insert(request):
    fname = ''
    fsize = 0

    if 'file' in request.FILES:
        file = request.FILES['file']
        fsize = file.size
        fname = file.name
        fp = open('%s%s' %(UPLOAD_DIR, fname),'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

    dto = Board(
        writer = request.POST['writer'],
        title = request.POST['title'],
        content = request.POST["content"],
        filename = fname,
        filesize = fsize
    )
    dto.save()
    return redirect("/list/")

def list(request):
    boardList = Board.objects.all()
    boardCount = Board.objects.all().count
    context = {'boardList' : boardList,
               'boardCount' : boardCount}
    return render(request, 'board/list.html', context)

def detail(request, board_id):
    dto = Board.objects.get(id=board_id)
    dto.hit_up()
    dto.save()
    return render(request, 'board/detail.html', {'dto' : dto})

# 다운로드 횟수 증가
def download_count(request, board_id):
    dto = Board.objects.get(id=board_id)
    dto.down_up()
    dto.save()
    count = dto.down
    return JsonResponse({'count' : count, 'id' : board_id})

# 다운로드
def download(request):
    id= request.GET['idx']
    dto = Board.objects.get(idx = id)
    path = UPLOAD_DIR + dto.filename
    filename = urllib.parse.quote(dto.filename)
    # filename =dto.filename

    with open(path ,'rb') as file :
        response = HttpResponse(file.read(),
                            content_type='application/octet-stream')
        response['Content-Disposition']="attachment;filename*=UTF-8''{0}".format(filename)    

    return response

