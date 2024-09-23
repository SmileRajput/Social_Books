from django.urls import path
from .views import register, home, authors_and_sellers

urlpatterns = [
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('authors-and-sellers/', authors_and_sellers, name='authors_and_sellers'), # noqa
]
