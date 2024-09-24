from django.urls import path
from .views import (
                    register, home,
                    authors_and_sellers,
                    user_dashboard,
                    upload_books,
                    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('authors-and-sellers/', authors_and_sellers, name='authors_and_sellers'), # noqa
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('upload_books/', upload_books, name='upload_books'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # noqa
