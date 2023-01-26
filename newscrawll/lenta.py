import httpx
import asyncio

from lxml import etree

from fake_useragent import UserAgent

ua = UserAgent()
headers = {'User-Agent': str(ua.google)}
LENTA_HACKER_NEWS = "https://lenta.ru/rubrics/media/hackers/"


async def pick_all_lenta_hacker_news():
    async with httpx.AsyncClient() as client:
        page_news = await client.get(LENTA_HACKER_NEWS, headers=headers)
        tree = etree.HTML(page_news.text)
        titles = tree.xpath("//*[@class='rubric-page']//h3/text()")
        links = ["https://lenta.ru" + link for link in tree.xpath("//*[@class='rubric-page']//li/a/@href")]
        time = tree.xpath("//*[@class='rubric-page']//time/text()")
        news = {}
        for i in range(len(titles)):
            if i <= 20:
                news[i+1] = {"title": titles[i], "link": links[i], "time": time[i]}
        return news


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pick_all_lenta_hacker_news())
