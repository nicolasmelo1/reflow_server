from django.conf import settings

from reflow_server.authentication.models import Company
from reflow_server.authentication.events import AuthenticationEvents
from reflow_server.core.utils import replace_dumb_characters_from_str
from reflow_server.core.utils.storage import Bucket

import random
import unicodedata
import string


class CompanyService:
    def _company_name_generator(self):
        """
        Creates a random company_name if the company_name is not specified

        Returns:
            str -- Custom and random company name
        """
        prefix_options = ['Ice', 'Hot', 'Cold', 'Fire', 'Earth', 'Light', 'Air', 'Windy', 'Nightly', 
                        'Dark', 'White', 'Brown', 'Orange', 'Pink', 'Red', 'Cyan', 'Grey', 'Beautiful',
                        'Nice', 'Cool', 'Perfect', 'Kind', 'Cute', 'Long', 'Quick', 'Fast', 'Rapid']

        suffix_options = ['Fox', 'Hound', 'Dog', 'Cat', 'Chetah', 'Lion', 'Horse', 'Seagul', 'Pingeon', 'Turtle',
                        'Fish', 'Caterpilar', 'Giraffe', 'Zebra', 'Rhino', 'Rabbit', 'Crocodile', 'Flamingo',
                        'Sealion', 'Horsesea', 'Whale', 'Bee', 'Nest', 'Tiger', 'Peixe-Boi', 'Boto', 'Jacaré', 'Narwall']

        return random.choice(prefix_options) + ' ' + random.choice(suffix_options)

    def _create_company_endpoint(self, company_name):
        """
        Recieves a company_name and creates an endpoint, endpoints must be url friendly and JSON notation friendly
        and also needs to be unique for each company.

        Arguments:
            company_name {str} -- The company name, all endpoints are based on the company name to be created.

        Returns:
            str -- Unique endpoint to be used for the company
        """
        return self._check_if_endpoint_exists(
            replace_dumb_characters_from_str(
                unicodedata.normalize(
                    'NFKD',
                    company_name.lower().replace(' ', '_'))\
                    .encode('ascii', 'ignore').decode('utf-8').translate(str.maketrans('', '', string.punctuation))
            )
        )

    def _check_if_endpoint_exists(self, endpoint):
        """
        The name says it all, it just checks if the endpoint exists already in a company then creates a random int if it exists
        it just goes on and on on a loop until one is valid.

        Arguments:
            endpoint {str} -- The endpoint to check if its valid

        Returns
            str -- A valid and unique endpoint for a company
        """
        company = Company.authentication_.company_by_endpoint(endpoint)
        count = random.randint(1,100001)
        while company:
            endpoint = endpoint + '{}{}'.format(endpoint, count)
            count = random.randint(1,100001)
            company = Company.authentication_.company_by_endpoint(endpoint)
        return endpoint
    
    def update_company(self, company_id, name, company_logo=None):
        """
        Updates the company based on a company_id. This just updates the name of the company and sets a image file for the logo.

        Args:
            company_id (int): The company id to edit and update
            name (str): The new name of the company
            company_logo (list(django.core.files.uploadedFile.InMemoryUploadedFile), optional): The file data of the image uploaded. Defaults to None.

        Returns:
            reflow_server.authentication.models.Company: The Company instance updated.
        """
        bucket = Bucket()
        instance = Company.authentication_.company_by_company_id(company_id)
        instance.name = name
        if company_logo:
            key_path= "{company_logo_path}/{company_id}/".format(
                company_id=str(company_id),
                company_logo_path=settings.S3_COMPANY_LOGO_PATH
            )
            if instance.logo_image_url:
                file_name = instance.logo_image_url.split(key_path)[1]
                bucket.delete(
                    key=key_path+file_name
                )
            url = bucket.upload(
                key=key_path + str(company_logo[0].field_name).replace(' ', '-'),
                file=company_logo[0],
                is_public=True
            )
            instance.logo_image_url = url

        instance.save()
        
        # sends the events to the clients
        AuthenticationEvents.send_updated_company(instance.id)
        return instance

    def get_company_logo_url(self, company_id):
        """
        Gets a temporary url for the logo of the company so we can display it to the user.

        Args:
            company_id (int): The company id to retrieve the logo for

        Returns:
            str: A url of the company logo
        """
        bucket = Bucket()
        instance = Company.authentication_.company_by_company_id(company_id)
        
        """if instance.logo_image_url not in ['', None]:
            key_path= "{company_logo_path}/{company_id}/".format(
                company_id=str(company_id),
                company_logo_path=instance.logo_image_path
            )
            file_name = instance.logo_image_url.split(key_path)[1]
            return bucket.get_temp_url(key_path+file_name)
        """
        return instance.logo_image_url