from django.db import models

class PushNotificationTagType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table='push_notification_tag_type'


class PushNotification(models.Model):
    """
    You might be thinking why this is not on the `notifications` app. Notifications are usually set when the user makes login and are
    totally bound to the user_id, so it makes sense it here. `notifications` is a app that hold the Reflow business logic about notifications.
    Tokens are usually json, but each of them has it's own implementation, to make it easier, saves everything as CharField()
    """
    user = models.ForeignKey('authentication.UserExtended', on_delete=models.CASCADE, default=None)
    token = models.CharField(max_length=1000)
    push_notification_tag_type = models.ForeignKey('notify.PushNotificationTagType', on_delete=models.CASCADE, default=None)
    # we always need to send push to a certain endpoint
    endpoint = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'push_notification'
