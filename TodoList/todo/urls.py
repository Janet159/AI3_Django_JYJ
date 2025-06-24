from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todo', views.todo, name='todo'),
    path('create', views.create, name='create'),
    path('delete', views.delete, name='delete'),
    path('ing', views.ing, name='ing'),
    path('done', views.done, name='done'),
    path('wait', views.wait, name='wait'),
    path('update/<int:no>', views.update_page, name='update_page'),  # 수정폼 페이지
    path('update', views.update, name='update'),  # 수정 처리
]