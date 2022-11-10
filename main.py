from flask import Flask
 

app = Flask(__name__)
 

@app.route('/')

def hello_world():
    return 'Hello World v50'

if __name__ == '__main__':
    app.run("0.0.0.0", port=2222)