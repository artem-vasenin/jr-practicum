import os
import aiofiles

async def get_prompt(path: str):
    async with aiofiles.open(os.path.join('resources', 'prompts', path + '.txt')  , 'r', encoding='utf-8') as f:
        return await f.read()

async def get_msg(path: str):
    async with aiofiles.open(os.path.join('resources', 'messages', path + '.txt')  , 'r', encoding='utf-8') as f:
        return await f.read()