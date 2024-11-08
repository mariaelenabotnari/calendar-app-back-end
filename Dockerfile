FROM python
WORKDIR /app

COPY EventLink .
COPY requirements.txt /app
COPY *.py /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3","main.py"]