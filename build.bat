docker container stop gunicorn
docker build -t gunicorn/test --network maintesoft .
docker run --rm --name gunicorn -p 8000:8000 gunicorn/test
