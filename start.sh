export PORT=${PORT:-80}
export APP_HOME=${APP_HOME:-/gpu_profits}

uwsgi --http 0.0.0.0:${PORT} --wsgi-file ${APP_HOME}/wsgi.py
