import openai
import base64
import time
import cv2
import os
import json
from pathlib import Path
from diseases import disease_info
import streamlit as st
import json

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def validate_result(api_result,threshold=70):
    '''
    This function ensure a minimal score and print result
    '''
    first_category = list(api_result.keys())[0]
    secund_category = list(api_result.keys())[1]
    third_category = list(api_result.keys())[2]
    first_value_accuracy = round(list(api_result.values())[0]*100,2)
    if first_category == 'Background without leaves':
        return "Sorry, no leaf detected.  Please try again."
    if first_category.endswith('ealthy') and first_value_accuracy > threshold :
        return "Diagnosis:" + f' **{first_category}** '+  " ( "+ str(first_value_accuracy) +"% )"
    if first_value_accuracy > threshold :
        return "Diagnosis:" + f' **{first_category}** '+  " ( "+ str(first_value_accuracy) +"% ) : " + f' disease infos here 👉[link]({disease_info(first_category)})' + "!"
    else:
        return f"I'm hesitating between **{first_category}**, {secund_category} and {third_category}. Please try again OR  **Most probable** disease infos here 👉[link]({disease_info(first_category)})"


def chat_with_chatgpt(prompt, model="text-davinci-003"):
    '''
    send a prompt to chatGPT api.  Reply with a str()
    '''
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message


def loading_message():
    '''
    This function display a progress bar with custom messages
    '''
    message_list = [
            '## Loading image',
            '## Guillaume is finetuning the model ... :dna:',
            '## Guillaume is finetuning the model ... :dna:',
            '## Raphaël is checking if the prediction makes sense...:passport_control:',
            '## Raphaël is checking if the prediction makes sense...:passport_control:',
            '## Alice is looking into a dictionary about the detected disease... :leaves:',
            '## Alice is looking into a dictionary about the detected disease... :leaves:',
            '## Open a ticket.. :admission_tickets:',
            '## Open a ticket.. :admission_tickets:',
            '## Trust the process 	:sunglasses:',
            '## DONE ! :white_check_mark:'
        ]


    my_bar = st.progress(0, text=message_list[0])

    for percent_complete in range(1,100):
        time.sleep(0.07)
        message_id=int(percent_complete/len(message_list)+1)
        my_bar.progress(percent_complete + 1, text=message_list[message_id])
    return None
