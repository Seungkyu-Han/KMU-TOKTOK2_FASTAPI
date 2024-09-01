FROM python:3.10-slim-bookworm

COPY . /src
WORKDIR /src

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
