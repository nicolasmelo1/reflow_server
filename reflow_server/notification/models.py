from django.db import models




class NotificationConfiguration(AbstractNotificationConfiguration):
    field = models.ForeignKey(Field, models.CASCADE, db_index=True)
    form = models.ForeignKey(Form, models.CASCADE, db_index=True)
    user = models.ForeignKey(UserExtended, models.CASCADE, db_index=True, blank=True, null=True)

    class Meta:
        db_table = 'notification_configuration'


class NotificationConfigurationVariable(models.Model):
    notification_configuration = models.ForeignKey(NotificationConfiguration, models.CASCADE, db_index=True, related_name='notification_configuration_variables')
    field = models.ForeignKey(Field, models.CASCADE, db_index=True)
    order = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'notification_configuration_variable'
        ordering = ('order',)

class PreNotification(models.Model):
    when = models.DateTimeField()
    has_sent = models.BooleanField(default=False)
    is_sending = models.BooleanField(default=False)
    dynamic_form = models.ForeignKey(DynamicForm, models.CASCADE, db_index=True)
    user = models.ForeignKey(UserExtended, models.CASCADE, db_index=True)
    notification_configuration = models.ForeignKey(NotificationConfiguration, models.CASCADE, db_index=True)
    
    class Meta:
        db_table = 'pre_notification'


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notification = models.CharField(max_length=500)
    form = models.ForeignKey(DynamicForm, models.CASCADE, db_index=True)
    user = models.ForeignKey(UserExtended, models.CASCADE, db_index=True, blank=True, null=True)
    notification_configuration = models.ForeignKey(NotificationConfiguration, models.SET_NULL, db_index=True, blank=True, null=True)

    class Meta:
        db_table = 'notification'
        ordering = ('-updated_at',)


class UserNotification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notification = models.ForeignKey(Notification, models.CASCADE, db_index=True)
    user = models.ForeignKey(UserExtended, models.CASCADE, db_index=True, blank=True, null=True)
    is_new = models.BooleanField(default=True)
    has_read = models.BooleanField(default=False)
     
    class Meta:
        db_table = 'user_notification'
        ordering = ('-updated_at',)
