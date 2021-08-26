from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sessions.models import Session
# Create your views here.

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            success_url = reverse_lazy('login')
            return redirect(success_url)

    # def post(self, request):
    #     form = self.form_class(request.POST)
    #
    #     if form.is_valid():
    #
    #         # storing the data but NOT SAVING them to db yet
    #         user = form.save(commit=False)
    #
    #         # cleaning and normalizing data
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         user.set_password(password)
    #         # saving to db
    #         user.save()
    #
    #         # if credentials are correct, this returns a user object
    #         user = authenticate(username=username, password=password)
    #
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #                 return redirect('login')
    #
    #     return render(request, self.template_name, {'form': form})

def signup(request):
    if not request.user.is_authenticated:

        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful." )
                return redirect("login")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = SignUpForm()
        return render(request=request, template_name="registration/register.html", context={"form":form})
    elif request.user.is_authenticated:
        return redirect('home')


def login_request(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    # request.session['is_logged'] = True
                    return redirect("home")
                else:
                    messages.error(request,"Invalid username or password.")
            else:
                messages.error(request,"Invalid username or password.")
        form = AuthenticationForm()
        return render(request=request, template_name="registration/login.html", context={"login_form":form})


# def signup(request):
#     form_class = SignUpForm()
#     return render(request,'registration/register.html',{'form': form_class})

