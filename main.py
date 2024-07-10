from flask import Flask, render_template, request
import sys

app = Flask(__name__)


@app.route('/')
def index():
    param = sys.argv[1] if len(sys.argv) > 1 else "No parameter provided"
    return render_template('index.html', param=param)


@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['user_input']
    param = sys.argv[1] if len(sys.argv) > 1 else "No parameter provided"
    return render_template('index.html', user_input=user_input, param=param)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
