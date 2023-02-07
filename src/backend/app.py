from flask import Flask, request
import json
app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)