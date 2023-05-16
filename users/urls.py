from django.urls import path
from .views import RegisterView, LoginView, UserActivate,  RegisterView  # ,SignUpView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<str:uidb64>/<str:token>', UserActivate.as_view(), name='activate')
]