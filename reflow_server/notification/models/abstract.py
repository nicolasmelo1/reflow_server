from django.db import models


class AbstractNotificationConfiguration(models.Model):
    """
    This abstract holds notification configuration data for notifications. As the name suggests, NotificationConfiguration is the 
    configuration of a notification. He can set a name for this notification, set if the notification is for the hole company or 
    not (IF HE IS AN ADMIN OF THE COMPANY), set the difference between date (60 days after the date or 60 days before the date), etc.

    It's important to differentiate: This notification is something that the user has total control of. 
    He can create the text and the condition on when and how to fire this notification. It's not something like Facebook
    or Twitter that has some default notifications that the user has no control of.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    for_company = models.BooleanField(default=False)
    name = models.CharField(max_length=500)
    text = models.CharField(max_length=500)
    days_diff = models.CharField(max_length=100, db_index=True)

    class Meta:
        abstract = True