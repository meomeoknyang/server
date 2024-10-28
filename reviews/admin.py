from django.contrib import admin
from .models import Review, ReviewImage

class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1  # 빈 추가 필드 개수 (기본 1개로 설정)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'rating', 'created_at')
    search_fields = ('restaurant__name', 'comment')  # 식당 이름과 코멘트로 검색
    inlines = [ReviewImageInline]  # 인라인으로 ReviewImage 모델 추가
