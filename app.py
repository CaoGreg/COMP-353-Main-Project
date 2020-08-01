from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return "hello world!"

if __name__ == "__main__":
    app.run(debug=True)

