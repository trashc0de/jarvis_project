from flask import Flask
from flask import request
import json

from commons import interactions

app = Flask(__name__)


def get_context(param, json_context):
    if not isinstance(json_context, list):
        return None
    else:

        for contx in json_context:

            if contx['name'] == param:
                return contx

        return None


@app.route('/providers/door_opener', methods=['POST'])
def index():
    success_event = interactions.EVENT_PREFIX + "-password-ok"
    fail_event = interactions.EVENT_PREFIX + "-password-ko"

    content = request.data

    json_context = json.loads(content)
    pswd_context = get_context('request-password-followup', json_context)
    if pswd_context is not None:

        pswd_parameters = pswd_context['parameters']
        password = pswd_parameters['password']

        if password == 'password':
            response = '{ "result": "success", "event": "' + success_event + '" }'
        else:
            response = '{ "result": "fail", "event": "' + fail_event + '" }'

        return response


app.run(host='0.0.0.0')
