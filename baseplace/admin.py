from django.contrib import admin
from .models import Menu
# Register your models here.
@admin.register(Menu)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'object_id', 'content_type_id')  # 목록에 표시할 필드 지정
    search_fields = ('name',)  # 식당 이름으로 검색 가능