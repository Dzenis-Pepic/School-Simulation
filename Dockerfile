FROM python:3

WORKDIR  C:/Users/Admin/Desktop/projekat

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN flask db init
RUN flask db migrate
RUN flask db upgrade

COPY . .

CMD [ "python", "./app.py" ]