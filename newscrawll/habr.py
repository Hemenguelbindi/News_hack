import httpx
import asyncio

from lxml import etree

from fake_useragent import UserAgent

ua = UserAgent()
headers = {'User-Agent': str(ua.google)}
HABR_NEWS = "https://habr.com/ru/news/"


async def pick_all_titles_and_link_on_HABR():
    async with httpx.AsyncClient() as client:
        page_news = await client.get(HABR_NEWS, headers=headers)
        tree = etree.HTML(page_news.text)
        titles = tree.xpath("//*[@class='tm-articles-list__item']//h2/a/span/text()")
        links = ["https://habr.com" + link for link in tree.xpath("//*[@class='tm-articles-list__item']//h2/a/@href")]
        time_date = tree.xpath("//*[@class='tm-articles-list__item']//time/text()")
        news = {}
        for i in range(len(titles)):
            news[i+1] = {"title": titles[i], "link": links[i], "time": time_date[i]}
        return news


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pick_all_titles_and_link_on_HABR())
