import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from write_in_redis import cached_lenta_ru, cached_habr_news


app = FastAPI()
script_dir = os.path.dirname(__file__)
st_abs_file_path = os.path.join(script_dir, "static/")
app.mount("/static", StaticFiles(directory=st_abs_file_path), name="static")


BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@app.get("/", response_class=HTMLResponse)
async def all_news(request: Request):
    lenta_news = await cached_lenta_ru()
    habr_news = await cached_habr_news()
    print(type(habr_news))
    return templates.TemplateResponse("index.html",
                                      {
                                          'request': request,
                                          'lenta': lenta_news,
                                          'habr': habr_news,
                                          })


@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})
