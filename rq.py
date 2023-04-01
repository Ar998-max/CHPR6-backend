import requests



from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api', methods = ['Get'])
def index():

    d = {}
    inputpro = str(request.args['query'])
    url = f'http://ip-api.com/json/{inputpro}'
    
    r = requests.get(url).json()
    print(r)

    y= {'name':r['country'],'id': r['countryCode']}
    d['output'] = y
    

    return d


if __name__== '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)




