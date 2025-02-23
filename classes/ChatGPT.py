import os
import aiofiles
from openai import AsyncOpenAI
from aiogram.fsm.state import StatesGroup

from config import PROXY_API_TOKEN, PROXY_API

AI_MODEL = 'gpt-3.5-turbo' # 'gpt-4o' дорогой гад


class ChatGPT(StatesGroup):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._client = self._get_client()

    def _get_client(self):
        return AsyncOpenAI(api_key=PROXY_API_TOKEN,  base_url=PROXY_API)

    async def text_request(self, messages: list[dict[str, str]], prompt: str):
        msgs = [{'role': 'system', 'content': prompt}] + messages if prompt else messages
        cmp = await self._client.chat.completions.create(messages=msgs, model=AI_MODEL)
        return cmp.choices[0].message.content

    async def get_text(self, path: str, is_prompt: bool = False):
        url = os.path.join('resources', 'prompts', path + '.txt') if is_prompt else os.path.join('resources', 'messages', path + '.txt')
        async with aiofiles.open(url, 'r', encoding='utf-8') as f:
            return await f.read()