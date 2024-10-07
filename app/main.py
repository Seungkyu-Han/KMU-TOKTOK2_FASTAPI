import os
from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio

app = FastAPI()

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


class PostReq(BaseModel):
    content: str
    assistant_id: str


@app.post("/")
async def root(post_req: PostReq):
    client = OpenAI(api_key=OPENAI_API_KEY)

    # 스레드 생성
    run = client.beta.threads.create_and_run(
        assistant_id=post_req.assistant_id,
        thread={
            "messages": [
                {"role": "user", "content": post_req.content}
            ]
        }
    )

    count = 0

    while run.status == 'queued' or run.status == 'in_progress':
        run = client.beta.threads.runs.retrieve(
            thread_id=run.thread_id,
            run_id=run.id,
        )
        count += 1

        if count > 10:
            await delete_thread(client, run.thread_id)
            return "챗봇 요청 중에 에러가 발생했습니다."

        await asyncio.sleep(1)

    message = client.beta.threads.messages.list(run.thread_id)

    await delete_thread(client, run.thread_id)

    return message.data[0].content[0].text.value


async def delete_thread(client, thread_id):
    client.beta.threads.delete(thread_id)