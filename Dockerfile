FROM python:3.8

RUN pip install --no-cache-dir uvicorn gunicorn

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "app:app"]