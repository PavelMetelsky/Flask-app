FROM python:3.9

WORKDIR /app

COPY src/app.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]