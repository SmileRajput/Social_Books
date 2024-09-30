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
from rest_framework import generics, permissions
from .serializers import UploadedFilesSerializer
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
import random
from django.contrib.auth.views import LoginView
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required


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

# def dashboard(request):
#     users_list = CustomUser.objects.all()
#     paginator = Paginator(users_list, 5)  # Show 10 users per page

#     page_number = request.GET.get('page')
#     users = paginator.get_page(page_number)

#     return render(request, 'accounts/dashboard.html', {
#         'users': users
#     })

# Upload Books and Files
# def upload_books(request):
#     if request.method == 'POST':
#         form = UploadedFilesForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = form.save()
#             print(f"Uploaded File: {uploaded_file.file.url}")
#             return redirect('upload_books')
#     else:
#         form = UploadedFilesForm()

#     uploaded_files = UploadedFiles.objects.all()
#     return render(request, 'accounts/upload_books.html', {'form': form, 'uploaded_files': uploaded_files}) # noqa

def upload_books(request):
    if request.method == 'POST':
        form = UploadedFilesForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)  # Don't save yet
            uploaded_file.user = request.user  # Associate the file with the logged-in user # noqa
            uploaded_file.save()  # Now save the file with the user association
            print(f"Uploaded File: {uploaded_file.file.url}")  # Debugging line
            return redirect('upload_books')
    else:
        form = UploadedFilesForm()

    uploaded_files = UploadedFiles.objects.filter(user=request.user)  # Show only files uploaded by the logged-in user # noqa
    return render(request, 'accounts/upload_books.html', {'form': form, 'uploaded_files': uploaded_files}) # noqa


class UserUploadedFilesView(generics.ListAPIView):
    serializer_class = UploadedFilesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only files uploaded by the logged-in user
        return UploadedFiles.objects.filter(user=self.request.user)


def my_books_dashboard(request):
    if request.user.is_authenticated:
        # Check if the user has uploaded any files
        uploaded_files = UploadedFiles.objects.filter(user=request.user)

        if uploaded_files.exists():
            # User has uploaded files, render the dashboard
            return render(request, 'accounts/my_books.html', {'uploaded_files': uploaded_files}) # noqa
        else:
            # No files uploaded, redirect to Upload Books
            return redirect('upload_books')
    else:
        # If the user is not authenticated, redirect to login
        return redirect('login')  # Adjust according to your login URL name


def send_email_view(request):
    subject = 'Test Email'
    message = 'This is a test email from Django!'
    recipient_list = ['sumitrajput5013@gmail.com']

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Failed to send email: {e}')


def generate_otp():
    """Function to generate a 6-digit OTP"""
    return random.randint(100000, 999999)

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Call the parent form_valid method to handle the login process
        response = super().form_valid(form)
        
        # Generate OTP after successful login
        otp = generate_otp()

        # Print the OTP to the console
        print(f"Generated OTP for {self.request.user.email}: {otp}")

        # Save OTP in session
        self.request.session['otp'] = otp

        # Prepare the HTML message with OTP
        subject = 'Your OTP Code - Social Book'
        message = ''  # Plain text message (optional, can be left blank)
        recipient_list = [self.request.user.email]

        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                
                <!-- Header Section -->
                <h1 style="font-size: 24px; color: #333; text-align: center;">Your OTP Code</h1>
                
                <!-- Body Section -->
                <p style="font-size: 16px; color: #555;">
                    Hi {self.request.user.name}, your OTP code for login is <strong>{otp}</strong>.
                </p>
                <p style="font-size: 16px; color: #555;">
                    Please enter this code to complete your login process.
                </p>

                <!-- Footer Section -->
                <section style="margin-top: 30px; padding: 10px 0; border-top: 1px solid #ccc; text-align: center;">
                    <p style="font-size: 12px; color: #888;">
                        &copy; 2024 Social Book. All Rights Reserved.
                    </p>
                    <p style="font-size: 12px; color: #888;">
                        Visit us at <a href="http://yoursite.com" style="color: #4CAF50; text-decoration: none;">www.socialbook.com</a>
                    </p>
                </section>

            </div>
        </body>
        </html>
        """

        # Send the OTP email with HTML content
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False,
            html_message=html_message  # Send as HTML email
        )

        # Redirect to OTP verification page
        return redirect('otp_verification')

@login_required
def otp_verification_view(request):
    """View for verifying the OTP"""
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if user_otp == str(session_otp):
            # Clear OTP from session after success
            del request.session['otp']

            # Send HTML email notification of successful login
            subject = 'Login Successful - Social Book'
            message = ''  # Plain text part of the email (optional)
            recipient_list = [request.user.email]

            html_message = """
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    
                    <!-- Header Section -->
                    <h1 style="font-size: 24px; color: #333; text-align: center;">Welcome to the Social Book platform!</h1>
                    
                    <!-- Body Section -->
                    <p style="font-size: 16px; color: #555;">
                        You have successfully logged in. Explore our amazing collection of books, authors, and sellers.
                    </p>

                    <!-- Footer Section -->
                    <section style="margin-top: 30px; padding: 10px 0; border-top: 1px solid #ccc; text-align: center;">
                        <p style="font-size: 12px; color: #888;">
                            &copy; 2024 Social Book. All Rights Reserved.
                        </p>
                        <p style="font-size: 12px; color: #888;">
                            Visit us at <a href="http://yoursite.com" style="color: #4CAF50; text-decoration: none;">www.socialbook.com</a>
                        </p>
                    </section>

                </div>
            </body>
            </html>
            """

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
                html_message=html_message
            )

            # Redirect to home page after OTP verification
            return redirect('home')

        else:
            return HttpResponse('Invalid OTP!')

    return render(request, 'accounts/otp_verification.html')
