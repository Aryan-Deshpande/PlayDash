FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN \
python3 -m pip install -r requirements.txt --no-cache-dir
COPY . /app 

#CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]