import asyncio
import aiohttp
from lxml import etree
from fake_useragent import UserAgent
from newscrawll.const import LENTA_HACKER_NEWS

ua = UserAgent()

headers = {'User-Agent':str(ua.random)}



async def connect_site(session, url):
	async with session.get(url) as res:
		return await res.text()
	
	
async def parser_lenta_hacker_news():
	async with aiohttp.ClientSession(headers=headers) as session:
		page_news = await connect_site(session, LENTA_HACKER_NEWS)
		tree = etree.HTML(page_news)
		titles = tree.xpath("//*[@class='rubric-page']//h3/text()")
		links = ["https://lenta.ru" + link for link in tree.xpath("//*[@class='rubric-page']//li/a/@href")]
		time = tree.xpath("//*[@class='rubric-page']//time/text()")
		data = {}
		for i in range(len(titles)):
			data[i+1] = {"title": titles[i], "link": links[i], "data": time[i]}
		return data



	
if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(parser_lenta_hacker_news())
