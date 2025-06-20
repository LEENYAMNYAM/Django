from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
from myApp01.models import Board, Comment
import urllib.parse
# Create your views here.

UPLOAD_DIR = "D:/JMT/Django/workspace/upload/"

# 추가폼
def write_form(request):
    return render(request, "board/write.html")

# 추가
@csrf_exempt
def insert(request):
    fname = ''
    fsize = 0

    if 'file' in request.FILES:
        file = request.FILES['file']
        fsize = file.size
        fname = file.name
        fp = open('%s%s' %(UPLOAD_DIR, fname), 'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

    dto = Board(
        writer = request.POST["writer"],
        title = request.POST["title"],
        content = request.POST["content"],
        filename = fname,
        filesize = fsize
    )
    dto.save()
    return redirect("/list/")

# 전체보기 (list)
def list(request):
    boardList = Board.objects.all()
    boardCount = Board.objects.all().count
    print('boardListquery : ', boardList.query)
    context = {'boardList' : boardList,
               'boardCount' : boardCount}
    return render(request, 'board/list.html', context)

# 상세보기 (detail_idx) /detail_idx?idx=1
def detail_idx(request):
    id = request.GET['idx']
    print('id : ', id)
    dto = Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()

    return render(request, 'board/detail.html', {'dto': dto})

# 상세보기 (detail) /detail/1 ==> detail/<int:board_idx>
def detail(request, board_idx):
    dto = Board.objects.get(idx=board_idx)
    dto.hit_up()
    dto.save()

    ## comment list
    commentList = Comment.objects.filter(board_idx=board_idx).order_by('-idx')
    commentCount = Comment.objects.filter(board_idx=board_idx).count
    print('commentList sql :', commentList.query )

    return render(request, 'board/detail.html', {'dto' : dto, 'commentList' : commentList, 'commentCount':commentCount})

# 삭제하기
def delete(request, board_idx):
    Board.objects.get(idx=board_idx).delete()
    return redirect("/list/")

# 수정폼
def update_form(request, board_idx):
    dto = Board.objects.get(idx=board_idx)
    return render(request, 'board/update.html', {'dto' : dto})

# 수정
@csrf_exempt
def update(request):
    id = request.POST['idx']
    dto = Board.objects.get(idx = id)

    fname = dto.filename
    fsize = dto.filesize
    if 'file' in request.FILES:
        file = request.FILES['file']
        fsize = file.size
        fname = file.name
        fp = open('%s%s' %(UPLOAD_DIR, fname), 'wb')    
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

    dto_update = Board(
            id,
            writer = request.POST['writer'],
            title = request.POST['title'],
            content = request.POST['content'],
            filename = fname,
            filesize = fsize    
    )
    dto_update.save()


    return redirect('/list/')  # 업데이트 후 상세보기로 이동

# 다운로드 횟수 증가
def download_count(request):
    id = request.GET['idx']
    print('download_count id : ', id)
    dto = Board.objects.get(idx = id)
    dto.down_up()  # 다운로드 수 1 증가
    dto.save()
    count = dto.down # 다운로드 수
    print('download_count : ', count)
    return JsonResponse({'count' : count, 'idx' : id})

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


# 댓글 
@csrf_exempt
def comment_insert(request):
    id = request.POST['idx'] # 부모게시글
    cdto = Comment(
        board_idx = id,
        writer="aa",
        content = request.POST['content']
    )
    cdto.save()
    return redirect("/detail/"+id)
