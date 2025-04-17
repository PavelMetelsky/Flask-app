FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN useradd -m appuser
USER appuser

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]