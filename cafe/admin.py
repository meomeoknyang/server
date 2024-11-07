from django.contrib import admin
from .models import Cafe
# Register your models here.
# 모델을 관리자 페이지에 등록
@admin.register(Cafe)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'address', 'open_date')  # 목록에 표시할 필드 지정
    search_fields = ('name',)  # 식당 이름으로 검색 가능
