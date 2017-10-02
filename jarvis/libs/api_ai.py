import requests

API_AI_HEADER_CLIENT_KEY = '936180ceb0e3495d955ee11b0859a000'

# well
API_AI_SESSION_ID_VALUE = '55f07b65-b3e6-42ce-8c2f-6b636d1011cd'

API_AI_BASE_URL = 'https://api.api.ai/v1/'
API_AI_QUERY_ENDPOINT = 'query'
API_AI_EVENT_ENDPOINT = 'event'
API_AI_CONTEXTS_ENDPOINT = 'contexts'

API_AI_VERSION_PARAMETER = 'v'
API_AI_VERSION_VALUE = '20150910'

API_AI_LANGUAGE_PARAMETER = 'lang'
API_AI_LANGUAGE_VALUE = 'it'

API_AI_TIMEZONE_PARAMETER = 'timezone'
API_AI_TIMEZONE_VALUE = 'Europe/Rome'


API_AI_HEADER_AUTH_PARAMETER = 'Authorization'
API_AI_HEADER_AUTH_VALUE = 'Bearer ' + API_AI_HEADER_CLIENT_KEY

API_AI_CONTENT_TYPE_HEADER = 'Content-Type'
API_AI_CONTENT_VALUE_HEADER = 'application/json; charset=utf-8'

API_AI_SESSION_ID_PARAMETER = 'sessionId'


API_AI_EVENT_PARAMETER = 'e'
API_AI_EVENT_PARAMETER_LONG = 'event'
API_AI_EVENT_WELCOME = 'welcome'

API_AI_QUERY_PARAMETER = 'query'

API_AI_CONTEXTS_PARAMETER = 'contexts'


def get_default_headers():

    return {
        API_AI_HEADER_AUTH_PARAMETER: API_AI_HEADER_AUTH_VALUE
    }


def get_default_headers_for_post():

    return {

        API_AI_HEADER_AUTH_PARAMETER: API_AI_HEADER_AUTH_VALUE,
        API_AI_CONTENT_TYPE_HEADER: API_AI_CONTENT_VALUE_HEADER

    }


def get_default_payload():

    return {
        API_AI_VERSION_PARAMETER: API_AI_VERSION_VALUE,
        API_AI_LANGUAGE_PARAMETER: API_AI_LANGUAGE_VALUE,
        API_AI_TIMEZONE_PARAMETER: API_AI_TIMEZONE_VALUE,
        API_AI_SESSION_ID_PARAMETER: API_AI_SESSION_ID_VALUE
    }


def get_default_payload_for_post():

    return {
        API_AI_LANGUAGE_PARAMETER: API_AI_LANGUAGE_VALUE,
        API_AI_TIMEZONE_PARAMETER: API_AI_TIMEZONE_VALUE,
        API_AI_SESSION_ID_PARAMETER: API_AI_SESSION_ID_VALUE
    }


def reset_contexts():

    url = API_AI_BASE_URL + API_AI_CONTEXTS_ENDPOINT

    headers = get_default_headers_for_post()
    payload = {API_AI_SESSION_ID_PARAMETER: API_AI_SESSION_ID_VALUE}

    r = requests.delete(url, params=payload, headers=headers)
    return r


def post_query(query):

    url = API_AI_BASE_URL + API_AI_QUERY_ENDPOINT + "?" + API_AI_VERSION_PARAMETER + "=" + API_AI_VERSION_VALUE

    headers = get_default_headers_for_post()

    payload = get_default_payload_for_post()
    payload.update({API_AI_QUERY_PARAMETER: query})

    r = requests.post(url, json=payload, headers=headers)
    json_response = r.json()

    # print json.dumps(json_response, indent=4, sort_keys=True)

    return json_response


def post_event(event):

    url = API_AI_BASE_URL + API_AI_QUERY_ENDPOINT + "?" + API_AI_VERSION_PARAMETER + "=" + API_AI_VERSION_VALUE
    headers = get_default_headers_for_post()

    payload = get_default_payload_for_post()

    event = {"name": event, "data": {}}
    payload.update({API_AI_EVENT_PARAMETER_LONG: event})

    r = requests.post(url, json=payload, headers=headers)

    json_response = r.json()

    # print json.dumps(json_response, indent=4, sort_keys=True)

    return json_response


def is_success(result):

    if result is not None:

        status = result['status']
        code = status['code']

        return code == 200

    else:

        return False


