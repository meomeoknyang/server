# reviews/admin.py
from django.contrib import admin
from .models import Review, ReviewImage

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('place', 'user', 'rating', 'created_at')
    search_fields = ('place__name', 'user__username', 'comment')
    list_filter = ('rating', 'created_at')

admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewImage)
