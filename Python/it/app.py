from flask import Flask, render_template
from database import get_all_history

app = Flask(__name__)

@app.route('/')
def index():
    data = get_all_history()
    return render_template('index.html', history=data)

if __name__ == '__main__':
    app.run(debug=True)