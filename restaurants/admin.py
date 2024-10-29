from django.contrib import admin
from .models import Restaurant, Category, Department

# 모델을 관리자 페이지에 등록
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'address', 'open_date')  # 목록에 표시할 필드 지정
    search_fields = ('name',)  # 식당 이름으로 검색 가능

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# @admin.register(Menu)
# class MenuAdmin(admin.ModelAdmin):
#     list_display = ('name', 'restaurant', 'price', 'is_special')
#     search_fields = ('name', 'restaurant__name')

# Department 모델 등록 및 학과 이름 검색 기능 추가
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 학과 이름 표시
    search_fields = ('name',)  # 학과 이름으로 검색 가능