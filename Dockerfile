FROM python:3

WORKDIR  C:/Users/Admin/Desktop/projekat

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./app.py" ]