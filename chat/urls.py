from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>', views.ChatList.as_view()),
    path('<int:user_id>/<int:num>/', views.RetrieveChat.as_view()),
]


