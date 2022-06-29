export PORT=${PORT:-80}

uwsgi --http 0.0.0.0:${PORT} --wsgi-file wsgi.py
