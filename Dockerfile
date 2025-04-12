FROM python:3.9

WORKDIR /home

COPY requirements.txt app/

RUN pip install --upgrade pip
RUN pip install -r /home/app/requirements.txt

COPY app app/
COPY static static/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]