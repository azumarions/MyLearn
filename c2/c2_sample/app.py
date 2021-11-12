from flask import Flask, render_template, request, session, url_for, redirect
from flask.views import MethodView
import random

from werkzeug.utils import redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    n = random.randrange(5, 10)
    data = []
    for n in range(n):
        data.append(random.randrange(0, 100))
    return render_template('index.html',
    title = 'Template sample',
    message = 'calculate sum',
    data = data)

@app.route('/next')
def next():
    return render_template('next.html',
    title = 'next page',
    message = 'this is another page sample.',
    data = ['one', 'two', 'three'])

@app.template_filter('sum')
def sum_filter(data):
    total = 0
    for item in data:
        total += item
    return total

app.jinja_env.filters['sum'] = sum_filter

@app.context_processor
def sample_processor():
    def total(n):
        total = 0
        for i in range(n + 1):
            total += i
        return total
    return dict(total = total)

# @app.route('/', methods=['POST'])
# def form():
#     ck = request.form.get('check')
#     rd = request.form.get('radio')
#     sel = request.form.getlist('sel')
#     return render_template('index.html',
#     title = "form sample",
#     message = [ck, rd, sel])

app.secret_key = b'*********************'

class HelloAPI(MethodView):
    send = ''

    def get(self):
        if 'send' in session:
            msg = 'send: ' + session['send']
            send = session['send']
        else:
            msg = 'please write something'
            send = ''
        return render_template('next.html',
        title = 'next page',
        message = msg,
        send = send)

    def post(self):
        session['send'] = request.form['send']
        return redirect('/hello/')

app.add_url_rule('/hello/', view_func=HelloAPI.as_view('hello'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5001)