FROM python:3.11
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn==20.1.0

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ENV PYTHONUNBUFFERED=1

RUN chmod +x manage.py
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "collect_money.wsgi", "--timeout 120"]
