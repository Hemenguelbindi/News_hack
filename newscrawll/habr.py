import asyncio
import aiohttp
from lxml import etree
from newscrawll.lenta import connect_site, headers
from newscrawll.const import HABR_NEWS


async def pick_all_titles_and_link_on_HABR():
	async with aiohttp.ClientSession(headers=headers) as session:
		page_news = await connect_site(session, HABR_NEWS)
		tree = etree.HTML(page_news)
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