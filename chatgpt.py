import openai
import config
# resuest for chatgpt api

openai.api_key = config.OPENAI_API_KEY
# https://platform.openai.com/docs/guides/chat
async def correct_message(message):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    # https://platform.openai.com/docs/guides/chat/introduction
    messages=[
        {"role": "user", 'content': f'以下のメッセージを添削してください。\n{message}'},
    ]
    )
    return response["choices"][0]["message"]["content"]