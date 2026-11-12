from django.template import loader
from django.shortcuts import render, redirect   
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm

def members(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())



### Sign-in, Sign-out, Sign-up
def sign_in(request):
    if request.method == "GET":
        form = LoginForm(request.GET)
        


def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})

