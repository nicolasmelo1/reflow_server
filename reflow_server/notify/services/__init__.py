from django.db.models import QuerySet
from django.conf import settings


from reflow_server.notify.services.mail import MailService
from reflow_server.notify.services.push import PushService


class NotifyService:
    @staticmethod
    def send_welcome_mail(user_email, password, company_name, url):
        template_name = 'welcome_user'
        subject = 'Bem vindo a Reflow!'

        MailService.send_mail(
            settings.FROM_EMAIL, 
            template_name, 
            [
                MailService(
                    subject, 
                    user_email,
                    [
                        {
                            'name': 'password',
                            'value': password
                        }, {
                            'name': 'company_name',
                            'value': company_name
                        }, {
                            'name': 'platform_url',
                            'value': url
                        }
                    ]
                )
            ]
        )

    @staticmethod
    def send_new_notifications(notifications): 
        """
        Notify the user with push notification and by email that there are new notifications for him in the platform

        Args:
            notifications: django.db.models.QuerySet(reflow_server.notification.models.Notification): a query set of the created notifications.
            This uses all of the notifications created from every user and from every company in the platform.
        """       
        template_name = 'notifications'
        subject = 'Veja aqui suas ultimas notificações!'
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
            [MailService(subject, recipient,
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
