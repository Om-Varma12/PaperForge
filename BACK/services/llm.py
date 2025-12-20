import os
from openai import OpenAI
import json

def sendRequest(prompt):

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("HF_TOKEN"),
    )

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct:groq",
        messages=[
            {
                "role": "user",
                "content": "Take as much as time you need, but read the following things thoroughly and generate the required text: " + prompt
            }
        ],
    )
    # print(completion.choices[0].message.content)
    
    data = json.loads(completion.choices[0].message.content)
    return data
    
# sendRequest(' ')