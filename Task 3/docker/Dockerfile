FROM python:3.9

WORKDIR /app

COPY src/app/ /app/app/
COPY src/run.py /app/
COPY src/requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]