# pip install -U torch transformers tokenizers accelerate
import torch
from transformers import pipeline, AutoModelForCausalLM

def ask(x, context='', is_input_full=False):
    ans = pipe(
        f"### 질문: {x}\n\n### 맥락: {context}\n\n### 답변:" if context else f"### 질문: {x}\n\n### 답변:", 
        do_sample=True, 
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        return_full_text=False,
        eos_token_id=2,
    )
    print(ans[0]['generated_text'])

if __name__ =='__main__':
    MODEL = 'beomi/KoAlpaca-Polyglot-5.8B'

    model = AutoModelForCausalLM.from_pretrained(
        MODEL,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    ).to(device=f"cuda", non_blocking=True)
    model.eval()

    pipe = pipeline(
        'text-generation', 
        model=model,
        tokenizer=MODEL,
        device=0
    )
    while True:
        ask_text = input('please ask something!')
        if ask_text != 'q':
            ask(ask_text)
