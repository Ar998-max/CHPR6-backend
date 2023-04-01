import requests



from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api', methods = ['Get'])
def index():

    d = {}
    inputpro = str(request.args.get('query', None))
    ip = request.args.get('pro', None)
    d['item']=inputpro
    d['problem']=ip
    

    return d


if __name__== '__main__':
    app.run(host='0.0.0.0', port='10000', debug=True)




