FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt && \
    useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

COPY --chown=appuser:appuser app.py .

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ping || exit 1

EXPOSE 5000

CMD ["python", "app.py"]