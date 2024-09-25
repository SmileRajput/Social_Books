from django.urls import path
from .views import (
                    register, home,
                    authors_and_sellers,
                    user_dashboard,
                    upload_books,
                    UserUploadedFilesView,
                    my_books_dashboard
                    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('authors-and-sellers/', authors_and_sellers, name='authors_and_sellers'), # noqa
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('upload_books/', upload_books, name='upload_books'),
    path('my-files/', UserUploadedFilesView.as_view(), name='user-uploaded-files'), # noqa
    path('my-books/', my_books_dashboard, name='my_books_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # noqa
