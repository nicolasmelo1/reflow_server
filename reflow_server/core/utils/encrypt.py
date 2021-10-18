from django.conf import settings

from itsdangerous import URLSafeSerializer

class Encrypt:
    """
    This class is used so we can encrypt and decrypt the data passed to the url. This use a package called itsdangerous 
    for it`s usage.

    So in case we have a company_id in the url, on the url it shows something like ASQ.hu123iohu123HLIh1hl2i312, so the company_id
    can`t be easily guessed by a common user.

    When the function recieves a request it uses

    >>> encrypt = Encrypt()
    >>> encrypt.decrypt_pk(company_id)
    // 2 

    so it gets this string, decrypts and get a number. Finally it responds for the user encrypting the data that needs to be encrypted
    """
    @staticmethod
    def decrypt_pk(pk):
        encrypt = URLSafeSerializer(settings.SECRET_KEY)
        try:
            pk = encrypt.loads(pk)
        except Exception as e:
            pk = -1
        return pk

    @staticmethod
    def encrypt_pk(pk):
        encrypt = URLSafeSerializer(settings.SECRET_KEY)

        return encrypt.dumps(pk)
