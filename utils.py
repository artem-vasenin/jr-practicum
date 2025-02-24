import os
import aiofiles


async def get_text(path: str, is_prompt: bool = False):
    url = os.path.join('resources', 'prompts', path + '.txt') if is_prompt else os.path.join('resources', 'messages', path + '.txt')
    async with aiofiles.open(url, 'r', encoding='utf-8') as f:
        return await f.read()