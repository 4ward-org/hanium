from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Chat
from rest_framework.exceptions import NotFound
from .serializers import ChatRoomSerializer, RetrieveChatSerializer
from rest_framework.response import Response


# 유저별 채팅방 제목 목록 보여주기
class ChatList(APIView):

    # permission_classes = [IsAuthenticated]  # 로그인 한 유저만 이용가능.

    def get_object(self, user_id):
        try:
            return Chat.objects.filter(user = user_id)
        except Chat.DoesNotExist:
            return NotFound

    def get(self, request, user_id):
        all_chat = self.get_object(user_id)
        serializer = ChatRoomSerializer(all_chat, many=True)
        return Response(serializer.data)
    



# 유저별 and 채팅id (유저별 채팅방 하나씩 내용 보여주기)
class RetrieveChat(APIView):
    
    def get_object(self, user_id, num):
        chat_list = Chat.objects.filter(user=user_id)
        chat = chat_list[num]
        return chat
    

    def get(self, request, user_id, num):
        user_chat = self.get_object(user_id, num)
        serializer = RetrieveChatSerializer(user_chat)
        return Response(serializer.data)
    

