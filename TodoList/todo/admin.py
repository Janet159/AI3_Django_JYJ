from django.contrib import admin
from django.db import models
from django.forms import Textarea
from .models import Todo

# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    # 목록에 표시할 필드
    list_display = ('title', 'status', 'is_completed', 'created_at')

    # 필터
    list_filter = ('is_completed', 'status')

    # 검색
    search_fields = ('title',)

    # 읽기 전용 필드
    readonly_fields = ('created_at', 'updated_at')

    # TextField 입력창 커스터마이징 (content용)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 60})}
    }

    # 정렬 기본 설정
    ordering = ['-created_at']

    # 액션 예시
    actions = ['mark_completed']

    @admin.action(description='선택한 할 일 완료 처리')
    def mark_completed(self, request, queryset):
        queryset.update(is_completed=True)
