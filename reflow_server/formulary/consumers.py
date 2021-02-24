import json


class FormularyConsumer:
    """
    Refer to `reflow_server.core.consumers.py` for proper explanation on why
    and how we write consumers.

    It's important to also read django channels documentation https://channels.readthedocs.io/en/latest/
    for further explanation.
    """
    async def send_formulary_created_or_updated(self, event):
        await self.send(text_data=json.dumps(event))
