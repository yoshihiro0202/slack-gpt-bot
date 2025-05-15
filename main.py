from fastapi import FastAPI, Form
import openai
import os
import requests

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

@app.post("/ask-gpt")
async def ask_gpt(
    text: str = Form(...),
    user_name: str = Form(...),
    response_url: str = Form(...)
):
    prompt = f"{user_name}さんからの質問です：\n{text}"

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        answer = f"エラーが発生しました: {e}"

    requests.post(response_url, json={"text": answer})
    return "OK"
