from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel

import bentoml
from bentoml import env, artifacts, api
from bentoml.adapters import JsonInput
from bentoml.frameworks.transformers import TransformersModelArtifact
from bentoml.service.artifacts.common import PickleArtifact
from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast, pipeline, AutoTokenizer, BertModel, AutoModel
import torch
import numpy as np
import pandas as pd
import sys
from decoder_only_ver import ask


@env(infer_pip_packages=True)
@artifacts([
    TransformersModelArtifact('dialoggpt'),
    ])
class SummaryService(bentoml.BentoService):
    @api(input=JsonInput(), batch=False)
    def dts(self, input):
        dts_tokenizer = self.artifacts.dialoggpt.get("tokenizer")
        cs_model = self.artifacts.dialoggpt.get("model")
        # input = {"chat_room": "KakaoTalk_Chat_IT개발자 구직_채용 정보교류방", "start_date": "2023-01-11","time_period": "1", "penalty": ["something","something2"]}
        # input이 위 형태로 들어오는데 get_DTS input으로 들어가기 위해 penalty를 따로 빼고 DataFrame으로 만들어서 get_DTS에 들어가게 된다.
        user_input = input.pop("user_input")
        # past_user_inputs = input.pop("past_user_inputs")
        # generated_responses = input.pop("generated_responses")
        response = ask(user_input)
        return response

if __name__ == "__main__":

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = PreTrainedTokenizerFast.from_pretrained('byeongal/Ko-DialoGPT')
    # dts_bert_model = BertModel.from_pretrained('/opt/ml/input/poc/BERT/bert_10').to(device)  

    model = GPT2LMHeadModel.from_pretrained('byeongal/Ko-DialoGPT').to(device)  

    bento_svc = SummaryService()

    artifact = {"model": model, "tokenizer": tokenizer}
    bento_svc.pack("dialoggpt", artifact)
    
    saved_path = bento_svc.save()
