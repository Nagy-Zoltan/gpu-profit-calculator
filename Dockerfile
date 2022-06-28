FROM python

ADD . .

RUN pip install -r requirements.txt

CMD ["bash", "-c", "./start.sh"]
