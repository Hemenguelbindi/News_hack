from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .newscrawll.lenta import parser_lenta_hacker_news
from .newscrawll.habr import pick_all_titles_and_link_on_HABR


app = FastAPI()
script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")


BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))



@app.get("/", response_class=HTMLResponse)
async def all_news(request: Request):
	lenta_news = await parser_lenta_hacker_news()
	habr_news = await pick_all_titles_and_link_on_HABR()
	return templates.TemplateResponse(
		"index.html",
		{
			'request': request,
			'lenta': lenta_news,
			'habr': habr_news,
			}
		)


@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
	return templates.TemplateResponse('about.html', {'request': request,})