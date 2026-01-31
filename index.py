from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    with open("index.html", 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content

if __name__ == '__main__':
    app.run(debug=True, port=5001)