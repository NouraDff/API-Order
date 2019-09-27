from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/',  methods=['GET'])
def index():
    uri = " https://caissy.dev/shops/products"
    try : 
        reponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    reponseJson = reponse.text
    data = json.loads(reponseJson)
    return data 


if __name__ == '__main__':
    app.run(debug=True)
