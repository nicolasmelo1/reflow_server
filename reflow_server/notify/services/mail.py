class MailService:
    def __init__(self, subject, recipient, variables=[]):
        """
        This service is used to create each e-mail data individually for each recipient and also send the
        e-mails to a group of recipients.

        Args:
            subject (str): What's the e-mail subject?
            recipient (list): for which e-mail you are sending?
            variables (list, optional): the variables on the template. Defaults to list().
        """
        self.subject = subject
        self.recipient = recipient
        self.variables = variables
    
    @staticmethod
    def add_variable(variable_name, variable_value):
        return {
            'name': variable_name,
            'value': variable_value
        }
    
    @staticmethod
    def send_mail(from_mail, template_name, mails):
        """
        Handy function to forward emails to reflow_worker so reflow_worker can take care of the 
        email sending.

        Arguments:
            from_mail {str} -- string of email to send
            template_name {str} -- name of the email template in reflow_worker
            mails {list(MailService)} -- List of MailService objects
        """
        from reflow_server.notify.externals import MailerExternal

        MailerExternal().send_mail(from_mail, template_name, mails)

