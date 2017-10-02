import json
import requests


def get_provider(param, config_file):

    # load config file
    config_data = get_config_data(config_file)

    # get providers
    providers = config_data['providers']

    # get provider
    if param in providers:

        provider = providers[param]

        if provider is not None and len(provider) > 0:
            provider_url = provider
        else:
            provider_url = None

        return provider_url

    return None


def get_config_data(config_file):

    json_data = open(config_file)
    data = json.load(json_data)

    return data


def invoke_executer(provider_url, contexts):

    r = requests.request('POST', provider_url, json=contexts)
    response = r.json()

    return response


def provider_is_success(result):

    if result is not None:

        if result['result'] is not None:

            if result['result'] == 'success':
                return True

    return False


def get_event_from_provider(result):

    return None


def run_provider(provider_url, contexts):

    r = requests.request('POST', provider_url, json=contexts)
    response = r.json()

    return response
