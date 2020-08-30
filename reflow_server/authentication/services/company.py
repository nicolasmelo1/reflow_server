from reflow_server.authentication.models import Company
from reflow_server.core.utils import replace_dumb_characters_from_str

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