# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Message
from cryptography.fernet import Fernet
from django.contrib import messages
import os

# Generate a key for encryption (in production, store it securely)
key = os.environ.get('FERNET_KEY', Fernet.generate_key())
cipher = Fernet(key)





def user_login(request):
    next_url = request.GET.get('next', 'send_message')  # Default redirect URL
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Attempting to log in user: {username}")  # Debugging line
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"User {user.username} logged in successfully.")
            login(request, user)
            return redirect(next_url)
        else:
            print("Invalid credentials.")  # Debugging line
            messages.error(request, "Invalid credentials.")
    return render(request, 'messaging/login.html')



@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST['content']
        if content:  # Check if the content is not empty
            encrypted_content = cipher.encrypt(content.encode())
            Message.objects.create(sender=request.user, encrypted_content=encrypted_content)
            messages.success(request, "Message sent!")
            return redirect('inbox')  # Redirect to an inbox view instead of sending the same message
        else:
            messages.error(request, "Message content cannot be empty.")
    
    return render(request, 'messaging/send_message.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponse('login')

from django.http import HttpResponse

def welcome_view(request):
    return HttpResponse("<h1>Welcome to the Secure Messaging App</h1><a href='/login/'>Login</a>")
    


@login_required
def inbox_view(request):
    messages = Message.objects.filter(recipient=request.user)  # Adjust as needed
    return render(request, 'messaging/inbox.html', {'messages': messages})











