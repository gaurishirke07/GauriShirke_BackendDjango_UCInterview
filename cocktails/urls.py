from django.urls import path
from .views import search_page, detail_page, popular_cocktails, delete_cocktail

urlpatterns = [
    path('', search_page, name='search page'),
    path('cocktail/<int:item_id>/', detail_page, name='detail page'),
    path('popular/', popular_cocktails, name ='popular cocktails'),
    path('delete/<int:cocktail_id>/', delete_cocktail, name='delete cocktail')
]