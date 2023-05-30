from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatList.as_view()),
    path('<int:chat_id>/', views.RetrieveChat.as_view()),
]


