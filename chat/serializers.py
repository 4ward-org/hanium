from rest_framework import serializers
from .models import Chat

from users.serializers import UserInfoSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    # user = UserInfoSerializer(read_only=True) # DRF Serializer에서 owner(Room모델안에 있는)를 가지고 올때 TinyUserSerializer에서 데이터를 가져옴
    title = serializers.SerializerMethodField() # title 뽑아내기

    class Meta:
        model = Chat
        fields = ('title',)    

    def get_title(self, chat): #SerializerMethodField 를 사용하면 꼭 get_변수이름 이름 함수를 지정해줘야 함.
        return chat.input[0] if chat.input else ''
    
class RetrieveChatSerializer(serializers.ModelSerializer):

    class Meta:
        model=Chat
        fields = ('input', 'output')


