from flask import Flask, render_template, request
import random

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

# @app.route('/', methods=['POST'])
# def form():
#     ck = request.form.get('check')
#     rd = request.form.get('radio')
#     sel = request.form.getlist('sel')
#     return render_template('index.html',
#     title = "form sample",
#     message = [ck, rd, sel])

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')