import sys
import logging
import os
import datetime
import json
import traceback
import socket
from waitress import serve
from flask import Flask, jsonify, request
app = Flask(__name__)

# sys.path.insert(0, "/code")


@app.route('/execute/<method>', methods=['POST'])
def execute(method):
    logging.info("executing ...")
    events = request.get_json()
    logging.info("processing %s events ..." % len(events))

    if True:
        try:
            dltk_code = __import__("dltk_code")
        except:
            return "Error importing algo:\n%s" % traceback.format_exc(), 500

        if not hasattr(dltk_code, method):
            return "Method '%s' not found:\n%s" % method, 400
        method_impl = getattr(dltk_code, method)

        try:
            result = method_impl(events)
        except:
            return "Error calling algo method:\n%s" % traceback.format_exc(), 500
    else:
        result = []

    logging.info("execute finished")
    return jsonify(result)


if __name__ == '__main__':
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO"),
        format='%(asctime)s %(levelname)-8s %(message)s',
    )

    hostname = socket.gethostname()
    last_dash_index = hostname.rfind("-")
    worker_index = int(hostname[last_dash_index+1:])
    worker_prefix = hostname[:last_dash_index]
    worker_suffix = os.getenv("TF_WORKER_SUFFIX")
    worker_count = int(os.getenv("TF_WORKER_COUNT"))
    worker_port = int(os.getenv("TF_WORKER_PORT"))

    tf_config = json.dumps({
        "cluster": {
            "worker": [
                "%s-%s.%s:%s" % (
                    worker_prefix,
                    i,
                    worker_suffix,
                    worker_port
                )
                for i in range(worker_count)
            ],
        },
        "task": {
            "index": worker_index,
            "type": "worker",
        }
    })
    logging.info(tf_config)
    os.environ["TF_CONFIG"] = tf_config

    serve(
        app,
        host="0.0.0.0",
        port=5002,
        channel_timeout=100000,
    )
