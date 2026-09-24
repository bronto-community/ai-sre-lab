FROM python:3.12-slim
WORKDIR /srv
RUN pip install --no-cache-dir fastapi==0.120.4 "uvicorn[standard]==0.38.0" httpx==0.28.1
COPY psp.py loadgen.py /srv/
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "psp:app", "--host", "0.0.0.0", "--port", "8000"]
