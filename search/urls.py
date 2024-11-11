from django.urls import path
from .views import SearchView

urlpatterns = [
    path('search/<str:place_type>/', SearchView.as_view(), name='search'),
]
