FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir uvicorn gunicorn

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . /
WORKDIR /

ENV PYTHONPATH=/

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "app:app"]
