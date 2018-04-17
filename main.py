from flask import Flask,request,render_template,url_for
from flask_restful import Resource, Api
import requests
from cachecontrol import CacheControl
from flask.ext.jsonpify import jsonify

app = Flask(__name__)
api = Api(app)


sess = requests.session()
cached_sess = CacheControl(sess)

@app.route('/')
@app.route('/index')
def index():
    return "Good"

class Goelocation(Resource):
    def get(self):
        return request.data # Fetches first

    def post(self,key):
        
        arr = request.json
        a = []
        for i in arr:
            b = {"wifiAccessPoints":[]}
            for j in i['apscan_data']:
                b['wifiAccessPoints'].append({"macAddress":j['bssid']})
            url = "https://www.googleapis.com/geolocation/v1/geolocate?key="+key
            r = cached_sess.post(url,json=b)
            a.append(r.text)
        return jsonify(a)

api.add_resource(Goelocation, '/goelocation/<key>')

if __name__ == "__main__":
    app.run(debug=True,port=5002)