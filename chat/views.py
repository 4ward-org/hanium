from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Chat
from .serializers import ChatRoomSerializer, RetrieveChatSerializer



# 유저별 채팅방 제목 목록 보여주기
class ChatList(APIView):

    permission_classes = [IsAuthenticated]  # 로그인 한 유저만 이용가능.

    def get(self, request):
        user = request.user # url을 요청한 유저
        user_chatlist = user.chat # user의 chat(related_name)으로 역참조 
        serializer = ChatRoomSerializer(user_chatlist, many=True)
        return Response(serializer.data)


# 유저별 and 채팅id (유저별 채팅방 하나씩 내용 보여주기)

class RetrieveChat(APIView):
    
    permission_classes = [IsAuthenticated]  # 로그인 한 유저만 이용가능.

    def get(self, request, chat_id):
        user = request.user # url을 요청한 유저 -> 로그인된 유저
        try:
            user_chat = user.chat.get(id=chat_id)  # chat_id에 해당하는 채팅방 객체 조회
            serializer = RetrieveChatSerializer(user_chat)
            return Response(serializer.data)
        except Chat.DoesNotExist:
            return Response({'message': 'Chat does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    # def get_object(self, user_id, num):
    #     chat_list = Chat.objects.filter(user=user_id)
    #     chat = chat_list[num]
    #     return chat
    

    # def get(self, request, user_id, num):
    #     user_chat = self.get_object(user_id, num)
    #     serializer = RetrieveChatSerializer(user_chat)
    #     return Response(serializer.data)
    

