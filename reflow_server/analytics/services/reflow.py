from django.conf import settings
from django.utils import timezone

from reflow_server.core.utils.asynchronous import RunAsyncFunction
from reflow_server.analytics.models import CompanyAnalytics
from reflow_server.authentication.models import Company, UserExtended

from datetime import timedelta


class ReflowAnalyticsService:
    def __init__(self, user_id, company_id):
        """
        You need to talk to Lucas for reference. At the current time, what lucas want is that when the user first onboards on the reflow app
        that we create on his comercial pipeline, a new company as a `new lead`. So we can enter in contact with the user.

        Whatsapp: https://wa.me/5511942622321
        Email: reflow@reflow.com.br

        Args:
            user_id (int): The id of the user we want to create a new lead for.
            company_id (int): The id of the company we want to create a new lead for.
        """
        self.user = UserExtended.analytics_.user_by_id(user_id)
        self.company = Company.analytics_.company_by_id(company_id)

    def create_record_in_sales_funnel(self):
        """
        This is responsible for async creating a new record in the sales funnel of reflow for Lucas.

        It will only run when in production environment.
        """
        def async_create_record():
            sector = CompanyAnalytics.analytics_.sector_by_company_id(self.company.id)

            company_name = self.company.name
            closing_forecast = (timezone.now() + timedelta(days=15)).isoformat()
            value = 0
            responsible = 'Lucas Melo'
            status= 'Novo Lead'
            partner = self.company.partner if self.company.partner != None else ''
            contact_name = f'{self.user.first_name} {self.user.last_name}'
            contact_email = self.user.email
            contact_phone = self.user.phone
            market = sector if sector != None else ''
            next_follow_up = (timezone.now() + timedelta(days=2)).isoformat()

            from reflow_server.analytics.externals import ReflowExternal
            ReflowExternal().create_new_record(
                company_name, 
                closing_forecast, 
                value, 
                responsible, 
                status, 
                contact_name, 
                contact_email, 
                contact_phone, 
                market, 
                next_follow_up, 
                partner
            )
        
        if settings.ENV == 'server':
            async_task = RunAsyncFunction(async_create_record)
            async_task.delay()