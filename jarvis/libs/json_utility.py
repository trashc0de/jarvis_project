
def is_success(json_response):

    result = json_response['status']
    return result['code'] == 200


def get_status(json_response):

    result = json_response['status']
    return result


def get_status_code(json_response):

    response_dict = get_status(json_response)
    return response_dict['code']


def get_speech(json_response):

    result = json_response['result']
    fullfillment = result['fulfillment']
    return fullfillment['speech']


def get_actions(json_response):

    result = json_response['result']
    if 'action' in result:
        return result['action']
    else:
        return []


def get_contexts(json_response):

    result = json_response['result']
    contexts = result['contexts']
    return contexts
