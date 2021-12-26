FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]