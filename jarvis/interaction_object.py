EVENT = 'event'
ACTION = 'action'
QUERY = 'query'


class Interaction:

    interaction_type = ''
    interaction_data = ''
    interaction_quit_on_fail = False

    def __init__(self):
        pass

    @classmethod
    def event_with_data(cls, event):

        result = Interaction()
        result.interaction_type = EVENT
        result.interaction_data = event

        return result

    @classmethod
    def query_with_data(cls, query):
        result = Interaction()
        result.interaction_type = QUERY
        result.interaction_data = query

        return result

    @classmethod
    def action_with_data(cls, action):
        result = Interaction()
        result.interaction_type = ACTION
        result.interaction_data = action

        return result

    def is_event(self):

        return self.interaction_type == EVENT

    def is_query(self):

        return self.interaction_type == QUERY

    def is_action(self):

        return self.interaction_type == ACTION
