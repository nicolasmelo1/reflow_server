from django.conf import settings

from reflow_server.core import externals
from reflow_server.notify.serializers import MailSerializer, PushSerializer


class MailerExternal(externals.External):
    host = settings.EXTERNAL_APPS['reflow_worker'][0]

    def send_mail(self, from_mail, template_name, mails):
        serializer = MailSerializer(data={
            'from_email': from_mail,
            'template': template_name,
            'recipients': [{
                'subject': mail.subject,
                'recipient': mail.recipient,
                'variables': mail.variables
            } for mail in mails]
        })
        self.post('/notify/external/mail/', data=serializer.data)


class PusherExternal(externals.External):
    host = settings.EXTERNAL_APPS['reflow_worker'][0]

    def send_push(self, template_name, pushs):
        serializer = PushSerializer(data={
            'template': template_name,
            'recipients': [{
                'tokens': [{
                    'token': token['token'].replace('"', '\\"'),
                    'type': token['push_notification_tag_type__name']
                } for token in push.tokens],
                'variables': {
                    'title': push.title_variables,
                    'body': push.body_variables
                }
            } for push in pushs]
        })

        self.post('/notify/external/push/', data=serializer.data)
