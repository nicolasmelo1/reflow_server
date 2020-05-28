from reflow_server.notification.models.abstract import AbstractNotificationConfiguration
from django.db import models

class NotificationConfiguration(AbstractNotificationConfiguration):
    """
    Further explanation on `reflow_server.notification.models.abstract.AbstractNotificationConfiguration`

    This is the configuration of a notification. Notifications on reflow works differently from notifications
    on plataforms like Facebook or Twitter. On those plataforms you can control whether you recieve the notification
    or not. Otherwise you cannot configure them much. You can't change the text of the notification or which of them
    you wish to recieve.

    Notifications in our platform works differently. The user has total control of the notification. Right now 
    notifications works only as Reminders, but we want to change it for other parts of the platform for stuff like events.
    If a change on the formulary has been made, and other stuff. (This doesn't work right now, its just for reminders)

    Okay, so how does notifications as reminders works? You need to select a formulary that contains a field with `field_type`
    `date` than based on the date of this field we send a notification or not.

    It's important to understand this is based on single users. So any user can create his own notifications, we don't strict
    it to admins only. The only difference is that ONLY ADMINS can create notifications for the hole company.
    """
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True)
    form = models.ForeignKey('formulary.Form', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True, blank=True, null=True)

    class Meta:
        db_table = 'notification_configuration'


class NotificationConfigurationVariable(models.Model):
    """
    These are the variables of a notification, this way it becomes easier for our programs to delete or add variables 
    accordingly on the notification.

    Don't understand what are variables in a notification? No problem

    As it was written in `reflow_server.notification.models.NotificationConfiguration`, notifications are based on a
    field of a formulary, also the user can write his own text on the notification. But let's go with the following example
    notification:

    - "The user needs to be contacted today"

    Imagine we want to change 'user' to the name of our user, or better yet, the email, so we can easily contact him.
    We do this adding variables.

    Variables are placeholders (`{{}}`) that contains the name of the field you want to use as a variable.

    So in our example you would write the text something like the following: 

    - "The {{user_email}} needs to be contacted today" - `user_email` is the name of the field inside of the formulary being used
    on the notification

    Read `reflow_server.formulary.models.Field` for explanation on fields and what are field names.
    """
    notification_configuration = models.ForeignKey('notification.NotificationConfiguration', models.CASCADE, db_index=True, related_name='notification_configuration_variables')
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True)
    order = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'notification_configuration_variable'
        ordering = ('order',)

class PreNotification(models.Model):
    """
    Pre notifications are an important part of our architecture on notifications, to explain why this model exists i need
    to explain you the architecture:

    - Notifications as i said in `reflow_server.notification.models.Notification` are usually reminders based on a date of a 
    formulary
    - With this in mind you need to understand how notifications work. We have an application called `reflow_worker` that
    has celery and celery beat inside of it. It asks from minute to minute if there are new notifications to send in this application.
    - The problem is, if everytime we needed to verify ALL of the data to see if there is a new notification to be built and send
    it would be too costly for this application.

    Because of this we create pre_notification, this holds really simple data: 
    - For what form (DynamicForm) this notification is being created, for what user and based on what notification configuration
    and finally when this notification must be sent.
    - With this model, we then check minute over minute if there are any new notifications to be sent. 
    - With this we create and build the notification ONLY WHEN WE SEND them to the user.

    Okay, you understood now. But let's see. When do you think we have to update the pre_notifications?

    If you responded when you change a user, when you changed the data of a form and when you change a notification configuration you
    are absolutely right.

    Since this are the only variables that we hold here we need to be aware when any of this change.
    - If the data of form has been created or updated we need to update the date of `when` we need to send the notification
    - if the permissions of a user have changed, he then might be able to see some formularies that he was not able to, or he might
    doesn't have the right to see some formularies that he used to see.
    - if the notification configuration has changed, now probably you don't need to notify me on the same day but 10 days earlier
    that i need to call this client.
    """
    when = models.DateTimeField()
    has_sent = models.BooleanField(default=False)
    is_sending = models.BooleanField(default=False)
    dynamic_form = models.ForeignKey('formulary.DynamicForm', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)
    notification_configuration = models.ForeignKey('notification.NotificationConfiguration', models.CASCADE, db_index=True)
    
    class Meta:
        db_table = 'pre_notification'


class Notification(models.Model):
    """
    I don't have much to say but this model is the built notification. 

    `notification` holds the text with the variables. The variables here are changed. Instead of being the field_name
    between {{}} here is the of the variable between {{}}. It's important to understand the varibles on here are all 
    static. So if you change the name of the client on the form, the variable here will not update.

    Besides that this just represents a simple notification.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notification = models.CharField(max_length=500)
    form = models.ForeignKey('formulary.DynamicForm', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True, blank=True, null=True)
    notification_configuration = models.ForeignKey('notification.NotificationConfiguration', models.SET_NULL, db_index=True, blank=True, null=True)

    class Meta:
        db_table = 'notification'
        ordering = ('-updated_at',)


class UserNotification(models.Model):
    # TODO: delete this
    """
    This is still used but because of the new architecture we don't need it anymore, move everything from here to notification

    this holds the data of the notification for each user. If the user has read, if it is a new notification and etc. it is all
    saved and stored here.

    This can be deleted later.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notification = models.ForeignKey('notification.Notification', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True, blank=True, null=True)
    is_new = models.BooleanField(default=True)
    has_read = models.BooleanField(default=False)
     
    class Meta:
        db_table = 'user_notification'
        ordering = ('-updated_at',)
