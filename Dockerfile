FROM python:3.8-slim

WORKDIR /myapp
COPY requirements.txt /myapp/requirements.txt
RUN pip3 install -r requirements.txt
COPY database.db /myapp
COPY src /myapp
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]