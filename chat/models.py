from django.db import models
from users.models import User

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat')
    input = models.JSONField()
    output = models.JSONField()

    # @classmethod
    # def update_or_create_chat(Chat, chat_id, input_message, output_message):
    #     try:
    #         chat = Chat.objects.get(id=chat_id)
    #         chat.input.append(input_message)  # 기존 input에 새로운 내용 추가
    #         chat.output.append(output_message)  # 기존 output에 새로운 내용 추가
    #         chat.save()
    #     except Chat.DoesNotExist:
    #         user_id = Chat.user
    #         user = User.objects.get(user=user_id)  # 사용자 정보 가져오기
    #         Chat.objects.create(user=user, input=[input_message], output=[output_message])
