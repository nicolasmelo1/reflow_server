from django.conf import settings
from reflow_server.notify.services.mail import MailService
from reflow_server.notify.services.push import PushService


class NotifyService:
    @staticmethod
    def send_welcome_mail(user_id):
        pass

    @staticmethod
    def send_new_notifications(notifications):        
        template_name = 'notifications'
        users_to_notify = dict()
        user_ids = list()
        for notification in notifications:
            user_ids.append((notification.user.id, notification.form.company.id, notification.user.first_name))
            users_to_notify[notification.user.email] = users_to_notify[notification.user.email] + [notification.notification] \
                if notification.user.email in users_to_notify else [notification.notification]
        
        # send email
        MailService.send_mail(
            settings.FROM_EMAIL, 
            template_name, 
            [MailService("Veja aqui suas ultimas notificações!", recipient,
                [
                    MailService.add_variable(
                    'notification',
                     notification.replace(r'{{', "<strong style='color: #0dbf7e'>").replace(r'}}',  "</strong>")
                    ) for notification in recipient_notifications[:10]
                ] + [
                    MailService.add_variable(
                        'platform_url', 
                        settings.EXTERNAL_APPS['reflow_front'][0] if settings.EXTERNAL_APPS['reflow_front'] else ''
                    )
                ]
            )
            for recipient, recipient_notifications in users_to_notify.items()]
        )
        
        # send push notification
        PushService.send_push(
            template_name,
            [PushService(user_id, [
                PushService.add_variable(
                    'username',
                    first_name
                )
            ])
            for user_id, company_id, first_name in list(set(user_ids))]
        )

    @staticmethod
    def send_change_password(user_id):
        pass
