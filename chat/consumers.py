from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from chat.models import Chat
import requests, json 

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        raise StopConsumer

   
    async def receive(self, text_data):
      # 웹소켓으로부터 메시지 수신
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('Message:', message)
        # self.send(f"you said: {text_data}")

      #메시지를 챗봇 API에 전달하고 응답 받아오기
        response = await self.get_chatbot_response(message)
        # if response =='q':
        #     self.disconnect
        # else:
        #     # 클라이언트로 응답 전송
        #     user = self.scope["user"]
        
        # if user.is_authenticated: # 로그인이 되어있으면
        #     Chat.save_chat_to_database(user, message, response)
        
        await self.send(text_data=json.dumps({
            'message':response
        }))
        

# 사실 여기는 tasks.py 에 넣어주는게 나을듯
# 한성이가 만든 챗봇 api 불러오고 답변 받아오는 코드 넣기
    async def get_chatbot_response(self, message,past_user_inputs=[],generated_responses=[]):
        api_url = 'http://127.0.0.1:53931/dialog'  # 챗봇 API의 URL
        payload = {'user_input': message}
        # payload = {'user_input': message,'past_user_inputs' : past_user_inputs'generated_responses':generated_responses}
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            data = response.json()  # 응답 데이터를 JSON 형식으로 파싱
            return json.dumps(data, ensure_ascii = False)
        else:
            return 'Error'


# import json
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#         self.send(text_data=json.dumps({
#             'type': 'connection_established',
#             'message': 'You are now connected!'
#         }))

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         print('Message:', message)
    