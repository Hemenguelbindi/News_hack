from typing import List, Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from newscrawll.lenta import parser_lenta_hacker_news
from newscrawll.habr import pick_all_titles_and_link_on_HABR

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def all_news(request: Request):
	lenta_news = await parser_lenta_hacker_news()
	habr_news = await pick_all_titles_and_link_on_HABR()
	return templates.TemplateResponse(
		"main.html",
		{
			'request': request,
			'lenta': lenta_news,
			}
		)
