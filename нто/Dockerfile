FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . . 

RUN pip install -r requirements.txt

CMD ["python", "api.py"]