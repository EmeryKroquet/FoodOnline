from http.client import HTTPResponse

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import UserForm


def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been Registered successful!')
            return redirect('registerUser')
        else:
            messages.error(request, "There was an error with your submission.")
            messages.error(request, form.errors)
    else:
        form = UserForm()
    return render(request, 'accounts/registerUser.html', {'form': form})
