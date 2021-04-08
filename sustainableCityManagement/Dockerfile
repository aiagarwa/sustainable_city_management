FROM python:3.8.2
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

RUN echo "DATABASE_URI=mongodb://ase-sustainable-city-management:lVebZcxWBUEbDzGdPUEre66q4gpPIMvbw2WOFX2NF9aNJsp57HJyBdHT8P9eEG0ihyKhMFqxKNYqPRX44X0bBw==@ase-sustainable-city-management.mongo.cosmos.azure.com:10255/default-db?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@ase-sustainable-city-management@" > /code/.env
RUN echo "DATABASE_ALIAS=default" >> /code/config/prod.env

EXPOSE 8000
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]