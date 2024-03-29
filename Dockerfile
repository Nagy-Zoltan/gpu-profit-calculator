FROM python

USER root

ENV APP_HOME="/gpu_profits"
WORKDIR $APP_HOME

ADD core core
ADD web_app web_app
ADD requirements.txt requirements.txt
ADD start.sh start.sh
ADD wsgi.py wsgi.py
RUN mkdir results

RUN pip install -r requirements.txt

RUN chmod 777 ./start.sh
CMD ["bash", "-c", "./start.sh"]
