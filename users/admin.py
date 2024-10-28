from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # 관리자 페이지에 표시할 필드 설정
    list_display = ('username', 'user_id', 'nickname', 'email', 'title', 'department', 'is_staff', 'is_active')
    search_fields = ('username', 'user_id', 'nickname', 'email')
    list_filter = ('title', 'is_staff', 'is_active', 'department')
    
    # 사용자 편집 페이지에 표시할 필드 그룹 설정
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_id', 'title', 'nickname', 'department', 'recent_stamp_restaurants')
        }),
    )
    
    # 사용자 생성 페이지에서 표시할 필드 설정
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_id', 'title', 'nickname', 'department')
        }),
    )
