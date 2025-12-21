import os
from openai import OpenAI
import json

def getLLMResponse(prompt):
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key="",
    )

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct:novita",
        messages=[
            {
                "role": "user",
                "content": "Take as much as time you need, but read the following things thoroughly and generate the required text: " + prompt
            }
        ],
    )
    
    return completion.choices[0].message.content

def sendRequest(prompt):
    sections = ['Abstract', 'Introduction', 'Literature Review', 'Methodology', 'Results']
    sectionParas = [1, 5, 7, 8, 7]
    text = {}
    
    llmPrompt = prompt + "\n\nNow, I want you to generate a normal one line of small TITLE based on the overview given to you."
    response = getLLMResponse(llmPrompt)
    text['Title'] = response
    
    for i in range(len(sections)):
        llmPrompt = prompt + f"\n\nI want you to generate {sectionParas[i]} paragraphs on the {sections[i]} section of the research paper, make sure you generate detailed content."
        response = getLLMResponse(llmPrompt)
        text[sections[i]] = response
        
    llmPrompt = prompt + "\n\nNow, I want you to generate a some References for the research paper based on the content generated above. Make sure the references are in IEEE format. And the references that you give must be in points, they must not in paragraphs."
    response = getLLMResponse(llmPrompt)
    text['References'] = response
    
    # print(type(text))
    # print(text)
    return text
    
# sendRequest(' ')