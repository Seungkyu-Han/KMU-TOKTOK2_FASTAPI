import os

from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv

app = FastAPI()

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


@app.get("/")
async def root():
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    thread_messages = client.beta.threads.messages.list("thread_6jbOIyZi6qe1PIPBnoOE01vo")
    print(thread_messages)
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
