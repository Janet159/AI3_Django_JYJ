from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .forms import TodoForm


from .models import *   # models 의 모든 모델 import

# Create your views here.
def index(request):
    print('메인 화면...')
    return render(request, 'todo/index.html', {})

def todo(request):
    print('할 일 목록 화면...')
    form = TodoForm()
    # 할 일 목록 조회
    # Todo 모델의 대기 목록 조회
    wait_list = Todo.objects.filter(status='WAIT')
    # Todo 모델의 진행 목록 조회
    ing_list = Todo.objects.filter(Q(status='ING') | Q(status='DONE')).order_by('-status')
    
    
    data = {'form': form, 'wait_list': wait_list, 'ing_list': ing_list}
    # render(request, 템플릿 경로, 데이터{})
    # - 데이터{} : 템플릿에 데이터를 전달
    return render(request, 'todo/todo.html', data)

# def create(request):
#     print('할 일 등록...')
#     # POST 방식의 파라미터
#     title = request.POST['title']
#     content = request.POST.get('content')
#     # 등록 요청
#     new_todo = Todo(title = title, content = content)
#     new_todo.save()     # DB에 저장
#     # 할 일 목록(todo)으로 리다이렉트
#     return HttpResponseRedirect(reverse('todo'))

def create(request):
    print('할 일 등록...')

    if request.method == 'POST':
        form = TodoForm(request.POST)

        if form.is_valid():
            form.save()  
            return HttpResponseRedirect(reverse('todo'))
        else:
            print('폼 에러:', form.errors)

    else:
        form = TodoForm()

    wait_list = Todo.objects.filter(status='WAIT')
    ing_list = Todo.objects.filter(Q(status='ING') | Q(status='DONE')).order_by('-status')

    data = {'form': form, 'wait_list': wait_list, 'ing_list': ing_list}

    return render(request, 'todo/todo.html', data)
    
# def update_page(request, no):
#     print("수정 페이지 요청...")
#     try:
#         todo = Todo.objects.get(no=no)
#         return render(request, 'todo/update.html', {'todo': todo})
#     except Todo.DoesNotExist:
#         return HttpResponseRedirect(reverse('todo'))

def update_page(request, no):
    print("수정 페이지 요청...")

    try:
        todo = Todo.objects.get(no=no)
        form = TodoForm(instance=todo)  # 기존 데이터가 들어간 폼 생성
        return render(request, 'todo/update.html', {'todo': todo, 'form': form})
    except Todo.DoesNotExist:
        return HttpResponseRedirect(reverse('todo'))


# def update(request):
#     print('할 일 수정...')
#     # 파라미터 
#     no = request.POST['no']
#     title = request.POST['title']
#     content = request.POST.get('content', '')

#     print(f'no: {no}, title: {title}, content: {content}')

#     try:
#         todo = Todo.objects.get(no=no)
#         todo.title = title
#         todo.content = content
#         todo.save()  # 수정 저장
#         print("수정 완료!")
#     except Todo.DoesNotExist:
#         print('수정할 할 일이 없습니다.')

#     return HttpResponseRedirect(reverse('todo'))

def update(request):
    print('할 일 수정...')

    no = request.POST['no']

    try:
        todo = Todo.objects.get(no=no)
    except Todo.DoesNotExist:
        print('수정할 할 일이 없습니다.')
        return HttpResponseRedirect(reverse('todo'))

    form = TodoForm(request.POST, instance=todo)

    if form.is_valid():
        form.save()
        print("수정 완료")
    else:
        print('폼 에러:', form.errors)
        return render(request, 'todo/update.html', {'todo': todo, 'form': form})

    return HttpResponseRedirect(reverse('todo'))



def delete(request):
    print("삭제 요청...")
    # 파라미터 
    no = request.POST['no']
    print('no : {}'.format(no))
    try:
        todo = Todo.objects.get(no=no)
        todo.delete()   # 할 일 삭제 요청
    except Todo.DoesNotExist:
        print('삭제할 할 일이 없습니다.')
    return HttpResponseRedirect(reverse('todo'))

def ing(request):
    print('진행 상태로 변경...')
    no = request.POST['no']
    print('no : {}'.format(no))
    try:
        todo = Todo.objects.get(no=no)
        # 할 일 상태 수정
        todo.status = 'ING' 
        todo.is_completed = False
        todo.save()
    except Todo.DoesNotExist:
        print('수정할 할 일이 없습니다.')
    return HttpResponseRedirect(reverse('todo'))


def done(request):
    print('완료 상태로 변경...')
    no = request.POST['no']
    print('no : {}'.format(no))
    try:
        todo = Todo.objects.get(no=no)
        # 할 일 상태 수정
        if todo.status == 'DONE':
            todo.status = 'ING' 
            todo.is_completed = False
        else:
            todo.status = 'DONE' 
            todo.is_completed = True
        todo.save()
    except Todo.DoesNotExist:
        print('수정할 할 일이 없습니다.')
    return HttpResponseRedirect(reverse('todo'))


def wait(request):
    print('대기 상태로 변경...')
    no = request.POST['no']
    print('no : {}'.format(no))
    try:
        todo = Todo.objects.get(no=no)
        # 할 일 상태 수정
        todo.status = 'WAIT' 
        todo.is_completed = False
        todo.save()
    except Todo.DoesNotExist:
        print('수정할 할 일이 없습니다.')
    return HttpResponseRedirect(reverse('todo'))
    