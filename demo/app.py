import os

import flask
from flask_session_azure import storage_account_interface

app = flask.Flask(__name__)
app.debug = True
app.secret_key = 'some very good and long secret with ümäuteàe%&'

# set this to true if you are behind on HTTPS
app.config['SESSION_COOKIE_SECURE'] = False

CONNECTION_STRING = os.environ.get("AzureWebJobsStorage")
app.session_interface = storage_account_interface(CONNECTION_STRING)

@app.route("/")
def set_settion():
    flask.session["some-key"] = ["data", "other-data"]
    return 'Session stored goto <a href="read">read</a>'

@app.route("/read")
def read_settion():
    values = flask.session["some-key"]
    return flask.jsonify(values)

if __name__ == "__main__":
    app.run()
