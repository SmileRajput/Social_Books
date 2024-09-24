from django.shortcuts import render, redirect
from django.contrib.auth import login
# from .forms import RegisterForm
from .forms import CustomUserCreationForm
from .models import CustomUser
import django_filters
from django_filters.views import FilterView
from django.core.paginator import Paginator
from .models import UploadedFiles
from .forms import UploadedFilesForm


# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = RegisterForm()
#     return render(request, 'accounts/register.html', {'form': form})


def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Create a filter class for additional filtering options (optional)
class PublicUserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Name'  # Custom label
    )
    email = django_filters.CharFilter(
        field_name='email',
        lookup_expr='icontains',
        label='Email'  # Custom label
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email']  # Add more fields if you want to allow filtering by name or email # noqa


# Create the view that uses the filter
def authors_and_sellers(request):
    # Get all users who have opted for public visibility
    public_users = CustomUser.objects.filter(public_visibility=True)

    # Optional: Use filtering for users
    user_filter = PublicUserFilter(request.GET, queryset=public_users)

    return render(request, 'accounts/authors_and_sellers.html', {
        'filter': user_filter
    })


# Dashboard to view all registered user
def user_dashboard(request):
    users_list = CustomUser.objects.all()
    paginator = Paginator(users_list, 5)  # Show 10 users per page

    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    return render(request, 'accounts/user_dashboard.html', {
        'users': users
    })


# Upload Books and Files
def upload_books(request):
    if request.method == 'POST':
        form = UploadedFilesForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            print(f"Uploaded File: {uploaded_file.file.url}")  # Debugging line
            return redirect('upload_books')
    else:
        form = UploadedFilesForm()

    uploaded_files = UploadedFiles.objects.all()
    return render(request, 'accounts/upload_books.html', {'form': form, 'uploaded_files': uploaded_files}) # noqa
