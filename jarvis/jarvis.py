from config import constants
from libs import api_ai
from interaction_object import Interaction
from libs import providers_interaction
from commons import interactions


# return bot response
def process_event(interaction):
    result = api_ai.post_event(interaction.interaction_data)

    if api_ai.is_success(result):

        # grab speech and contexts
        data = result['result']

        contexts = data['contexts']

        actions = data['action']

        fullfillment = data['fulfillment']
        speech = fullfillment['speech']

        return {
            'speech': speech,
            'contexts': contexts,
            'actions': actions
        }

    else:

        return None


# return bot response
def process_query(interaction):
    result = api_ai.post_query(interaction.interaction_data)

    if api_ai.is_success(result):

        data = result['result']

        contexts = data['contexts']

        if dict_contains('action', data):
            actions = data['action']
        else:
            actions = ''

        fullfillment = data['fulfillment']
        speech = fullfillment['speech']

        return {

            'speech': speech,
            'contexts': contexts,
            'actions': actions
        }

    else:

        return None


# return bot response AND (actionS OR event)
def process_action(interaction, actual_contexts):
    # route request to xctr
    provider_url = providers_interaction.get_provider(interaction.interaction_data, 'config/' + constants.CONFIG_FILE)
    if provider_url is not None:

        result = providers_interaction.run_provider(provider_url, actual_contexts)

        if not dict_contains('result', result):
            return {'result', 'fail'}

        if dict_contains('event', result):
            event = result['event']
        else:
            event = None

        if dict_contains('actions', result):
            actions = result['actions']
        else:
            actions = None

        if dict_contains('query', result):
            query = result['query']
        else:
            query = None

        if dict_contains('speech', result):
            speech = result['speech']
        else:
            speech = None

        provider_response = {}

        if event is not None:
            provider_response['event'] = event

        if actions is not None:
            provider_response['actions'] = actions

        if query is not None:
            provider_response['query'] = query

        if speech is not None:
            provider_response['speech'] = speech

        return provider_response

    else:

        return None


def process_interaction(interaction, actual_contexts):
    if interaction.is_event():

        return process_event(interaction)

    elif interaction.is_query():

        return process_query(interaction)

    elif interaction.is_action():

        return process_action(interaction, actual_contexts)


def dict_contains(param, result):
    if result is None:
        return False

    if param is None:
        return False

    if param in result:
        return True

    return False


def main():
    interaction_queue = []
    api_ai.reset_contexts()
    actual_contexts = {}
    will_quit = False

    # call default welcome event
    welcome_event = Interaction.event_with_data(api_ai.API_AI_EVENT_WELCOME)
    interaction_queue.append(welcome_event)

    while not will_quit:

        if len(interaction_queue) > 0:

            # process interaction
            interaction = interaction_queue.pop(0)
            result = process_interaction(interaction, actual_contexts)

            # if speech -> talk
            if dict_contains('speech', result):
                print constants.PROMPT_OUT + result['speech']

            # update actual contexts
            if dict_contains('contexts', result):
                actual_contexts = result['contexts']

            # if immediate action -> perform it (jarvis quit)
            if dict_contains('actions', result):

                # for now is a single action. will check for multiple actions
                action = result['actions']
                if len(action) > 0:

                    if action == interactions.JARVIS_QUIT:
                        will_quit = True
                        continue

                    # if actions append them
                    action_interaction = Interaction.action_with_data(action)
                    interaction_queue.append(action_interaction)

            # if event append it
            if dict_contains('event', result):
                event = result['event']
                event_interaction = Interaction.event_with_data(event)
                interaction_queue.append(event_interaction)

        else:

            # wait for user request
            command = raw_input(constants.PROMPT_IN)

            user_interaction = Interaction.query_with_data(command)
            interaction_queue.append(user_interaction)

    print 'jarvis terminated.'


# ############### ENTRY POINT ######################
if __name__ == '__main__':
    main()
