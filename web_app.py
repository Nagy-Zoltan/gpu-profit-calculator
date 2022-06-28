from flask import Flask, send_file

from main import main


app = Flask(__name__)


@app.route('/')
def index():
    return 'Running'


@app.route('/excel')
def excel():
    main()
    return send_file('results.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@app.route('/csv')
def csv():
    main()
    return send_file('results.csv', mimetype='text/csv')
