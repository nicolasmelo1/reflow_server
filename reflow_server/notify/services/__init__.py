from django.db.models import QuerySet
from django.conf import settings


from reflow_server.notify.services.mail import MailService
from reflow_server.notify.services.push import PushService


class NotifyService:
    @staticmethod
    def send_welcome_mail(user_email, password, company_name, url):
        """
        Sends a welcome email when an admin registers a new user in the platform on his company.

        Args:
            user_email (str): The email of the added user, this is the e-mail we send the email
            password (str): His temporary password so he can change it the first time he logs in
            company_name (str): We use this because this is a required parameter for the template
            url (str): The front-end url, usually this is recieved from the front-end since it can change quite often.
        """
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
            notifications (django.db.models.QuerySet(reflow_server.notification.models.Notification)): a query set of the created notifications.
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
    def send_change_password(user_email, user_first_name, temporary_password, url):
        """
        Sends an email for the user with a link for him to change his password.

        Args:
            user_email (str): The email of the added user, this is the e-mail we send the email
            user_first_name (str): The first name of the user to add on the subject of the email, this makes it more personal.
            temporary_password (str): His temporary password so he can change it the first time he logs in
            url (str): The front-end url, usually this is recieved from the front-end since it can change quite often.
        """
        template_name = 'change_password'
        subject = user_first_name + ", aqui está o link para alterar sua senha",

        MailService.send_mail(
            settings.FROM_EMAIL, 
            template_name, 
            [
                MailService(
                    subject, 
                    user_email, 
                    [{
                        'name': 'password',
                        'value': temporary_password
                    }, {
                        'name': 'platform_url',
                        'value': url
                    }]
                )
            ]
        )
