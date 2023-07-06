# imports
from flask import Flask, render_template, request, redirect, make_response
import libbasic, libdatabase, libgateway
import json


# initialize flask
app = Flask(__name__)


### VIEWS ###
@app.route('/', methods=['GET'])
def main():
    ip_attr = {}
    IPs = libdatabase.get_IP_list()

    for ip in IPs:
        ip_attr[ip] = libdatabase.get_IP_attributes(ip)

    return render_template('index.html', 
        money=libbasic.get_money(), 
        action_points=libbasic.get_AP(),
        ips=ip_attr,
        current_connection=libgateway.get_current_connection(),
        name="TBD",
        my_ip=libgateway.get_my_IP(),
    )

@app.route('/logs', methods=['GET'])
def logs():
    return render_template('logs.html', 
        logs=libgateway.get_logs(),
        current_connection=libgateway.get_current_connection(),
        name="TBD"
    )

@app.route('/static/<path:path>', methods=['GET'])
def static_files(path):
    return app.send_static_file(path)



### API ###
@app.route('/api/sync_db', methods=['GET'])
def sync_db():
    libdatabase.IPDB_to_localDB()
    resp = make_response(json.dumps({}))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/api/vote', methods=['GET'])
def vote():
    resp = make_response(json.dumps({'HPD': libbasic.vote()}))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/api/update', methods=['GET'])
def update():
    # update localhost and remote host
    libgateway.update_internal_info()
    libgateway.update_internal_info(libgateway.get_current_connection())

    resp = make_response(json.dumps({}))
    resp.headers['Content-Type'] = 'application/json'
    return resp



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, threaded=True, debug=True)