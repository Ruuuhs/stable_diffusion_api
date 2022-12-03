from flask import Flask, request, abort
import ipaddress

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'


ALLOW_NETWORKS = [""]

@app.before_request
def before_request():
    remote_addr = ipaddress.ip_address(request.remote_addr)
    app.logger.info(remote_addr)

    for allow_network in ALLOW_NETWORKS:
        ip_network = ipaddress.ip_network(allow_network)
        if remote_addr in ip_network:
            app.logger.info(ip_network)
            return
    return abort(403, 'access denied from your IP address')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)
