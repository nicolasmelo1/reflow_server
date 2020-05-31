import json

class NotificationReadConsumer:
    """
    Refer to `reflow_server.core.consumers.py` for proper explanation on why
    and how we write consumers.

    It's important to also read django channels documentation https://channels.readthedocs.io/en/latest/
    for further explanation.
    """
    def send_notification(self, event):
        self.send(text_data=json.dumps(event))
