FROM python:3.10

WORKDIR /news_hack

COPY ./requirements.txt /news_hack/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /news_hack/requirements.txt

COPY .  /news_hack/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]