FROM python

RUN pip install aiogram google-api-python-client google-auth-httplib2 google-auth-oauthlib environs

COPY . .

CMD python main.py