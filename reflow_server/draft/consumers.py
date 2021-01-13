import json

class DraftConsumer:
    """
    Refer to `reflow_server.core.consumers.py` for proper explanation on why
    and how we write consumers.

    It's important to also read django channels documentation https://channels.readthedocs.io/en/latest/
    for further explanation.
    """
    async def send_removed_draft(self, event):
        await self.send(text_data=json.dumps(event))
