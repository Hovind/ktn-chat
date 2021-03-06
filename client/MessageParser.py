import json


class MessageParser:
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            # More key:values pairs are needed
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        # Decode the JSON object
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return payload['content']
            # Response not valid

    def parse_error(self, payload):
        return payload['content'];

    def parse_info(self, payload):
        return payload['timestamp'] + " " + payload['content']

# Include more methods for handling the different responses...

    def parse_message(self, payload):
        return payload['timestamp'] + " " + payload['sender'] + ": " + payload['content']
            
    def parse_history(self, payload):
        return "\n".join(map(self.parse_message, payload['content'])) 