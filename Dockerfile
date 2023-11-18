FROM python:3.10

RUN pip install fastapi uvicorn black radon

WORKDIR /evaluator_code

COPY evaluator_code .

EXPOSE 8000

ENTRYPOINT  [ "python", "main/main.py"]
