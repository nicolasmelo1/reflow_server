from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    LibraryStruct, retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class SMTPMessage(LibraryStruct):
    def __init__(self, settings, from_email, to_emails, message_string):
        self.from_email = from_email
        self.recipients = to_emails
        self.message_string = message_string
        super().__init__('SMTP', settings)


class SMTP(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope, [])
        return self
    
    @functionmethod
    def build_message(from_email, to_emails, subject, content, cc=[], **kwargs):
        from_email = retrieve_representation(from_email)
        to_emails = retrieve_representation(to_emails)
        subject = retrieve_representation(subject)
        content = retrieve_representation(content)

        if not isinstance(to_emails, list):
            to_emails = [to_emails]

        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = ', '.join(to_emails)
        message['Subject'] = subject
        
        if cc != '':
            cc = retrieve_representation(cc)
            message['Cc'] = ', '.join(cc)

        message.attach(MIMEText(content, 'plain'))

        return SMTPMessage(kwargs['__settings__'], from_email, to_emails, message.as_string())

    @functionmethod
    def send_email(server, port, user, password, message, **kwargs):
        server = retrieve_representation(server)
        port = retrieve_representation(port)
        user = retrieve_representation(user)
        password = retrieve_representation(password)
        print('teste')
        if not isinstance(message, SMTPMessage):
            flow_objects.Error(kwargs['__settings__'])._initialize_('AttributeError', 'Run `.build_message()` function first and send the result in the "message" parameter. Example:\n' 
                                                                    'message = SMTP.build_message("example@reflow.com.br", "example@example.com", "Test", "Content")\n'
                                                                    'SMTP.send_email("smtp.gmail.com", 587, "example@reflow.com.br", "Secret", message)')
        
        print('teste2')

        try:
            client = smtplib.SMTP(server, port)
            # validate TLS
            if port == 587:
                client.ehlo()
                client.starttls()
            client.ehlo()
            client.login(user, password)
            
            client.sendmail(message.from_email, message.recipients, message.message_string)
            client.close()
        except smtplib.SMTPAuthenticationError as smtpae:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', str(smtpae))
        except smtplib.SMTPSenderRefused as smtpsr:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', str(smtpsr))
        return flow_objects.Null(kwargs['__settings__'])._initialize_()
        

    def _documentation_(self):
        return {
            'description': 'Enables users to send SMTP by their personal e-mail through reflow, this way they don\'t need to rely on third party services like IFTTT, Zapier or others.',
            'methods': {
                'build_message': {
                    'description': 'Builds the message to send. Before sending the e-mail you need to build the message using this function. This is obligatory. Returns a SMTPMessage struct.',
                    'attributes': {
                        'from_email': {
                            'description': 'From what e-mail you are sending this message',
                            'is_required': True
                        },
                        'to_emails': {
                            'description': 'To what e-mails you are sending this message to. Send a list for multiple recipients like: ["example1@example.com", "example2@example.com"]',
                            'is_required': True
                        },
                        'subject': {
                            'description': 'The subject of your e-mail. What is the title of your e-mail.',
                            'is_required': True
                        },
                        'content': {
                            'description': 'The content of the e-mail. What message are you sending for your users, be aware some HTML is fine but not all.',
                            'is_required': True
                        },
                        'cc': {
                            'description': 'Do you want to send this to someone as copy of this e-mail so they can respond to the e-mail? Send the options as a list like ["example1@example.com", "example2@example.com"]',
                            'is_required': False
                        }
                    }
                },
                'send_email': {
                    'description': 'Sends the email message that you built using `.build_message()` function, through a SMTP server.',
                    'attributes': {
                        'server': {
                            'description': 'The server in which you want to send the smtp email. For example: "smtp.gmail.com" (check for the documentation of your e-mail provider)',
                            'is_required': True
                        }, 
                        'port': {
                            'description': 'The port of your server, at port 587 it defaults to tls encrypted by default.',
                            'is_required': True
                        }, 
                        'user': {
                            'description': 'The user of your smtp server, generally this will be your e-mail but make sure you have double checked with your e-mail provider first.',
                            'is_required': True
                        }, 
                        'password': {
                            'description': 'The password of your smtp server, normally this will be password of your e-mail.',
                            'is_required': True
                        }, 
                        'message': {
                            'description': 'The message to send, this is generated by `.build_message()` function. So use this before sending the message.',
                            'is_required': True
                        }
                    }
                }
            },
            'structs': {
                'SMTPMessage': {
                    'description': 'The struct generated by `.build_message()` function, this is used in the "message" parameter of `.send_email()` function.',
                    'attributes': {
                        'from_email': {
                            'description': 'From what e-mail this message will be sent.'
                        },
                        'recipients': {
                            'description': 'List of recipients of those who you want to send the email to.'
                        },
                        'message_string': {
                            'description': 'The actual message string, this might doesn\'t make any sense for you, but this is here so you can know what you are sending and how.'
                        }
                    }
                }
            }
        }