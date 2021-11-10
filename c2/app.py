from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    data = ['windows', 'macOS', 'linuxOS', 'chromeOS']
    return render_template('index.html',
    title = 'this is jinja template!',
    message = data,
    data = data)

@app.route('/next')
def next():
    return render_template('next.html')

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