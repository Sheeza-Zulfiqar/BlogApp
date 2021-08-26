from django.urls import path
from .views import signup,login_request,UserRegisterView



urlpatterns = [
    path('register/', UserRegisterView.as_view(redirect_authenicated_user=True), name='register',),
    path('register/', signup, name='register',),
    path('login/', login_request, name='login'),

]