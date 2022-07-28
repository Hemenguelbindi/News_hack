import asyncio
import json

import aioredis

from newscrawll.habr import pick_all_titles_and_link_on_HABR
from newscrawll.lenta import pick_all_lenta_hacker_news


async def cached_habr_news():
    redis = aioredis.from_url("redis://redis_cache")
    cache_value = await redis.get("news_habr")
    if cache_value is not None:
        return json.loads(cache_value)
    habr_news = await pick_all_titles_and_link_on_HABR()
    await redis.set("news_habr", json.dumps(habr_news), ex=100)


async def cached_lenta_ru():
    redis = aioredis.from_url("redis://redis_cache")
    cache_value = await redis.get("news_lenta")
    if cache_value is not None:
        return json.loads(cache_value)
    lenta_news = await pick_all_lenta_hacker_news()
    await redis.set("news_lenta", json.dumps(lenta_news), ex=100)


async def main():
    await cached_habr_news()
    await cached_lenta_ru()

if __name__ == "__main__":
    asyncio.run(main())
