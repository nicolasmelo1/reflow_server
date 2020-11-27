from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.billing.models import ChargeFrequencyType, ChargeType, IndividualChargeValueType, InvoiceDateType, PaymentMethodType
from reflow_server.authentication.models import CompanyType, ProfileType, VisualizationType
from reflow_server.formula.models import FormulaType
from reflow_server.formulary.models import SectionType, FieldType, FieldPeriodIntervalType, FieldNumberFormatType, \
    FieldDateFormatType, ConditionalType
from reflow_server.dashboard.models import AggregationType, ChartType
from reflow_server.rich_text.models import TextAlignmentType, TextBlockType
from reflow_server.theme.models import ThemeType


@method_decorator(csrf_exempt, name='dispatch')
class HealthCheckView(APIView):
    """
    Simple healthcheck to check if the application is up and running or not.

    Methods:
        GET: 
    """
    def get(self, request):
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class TypesView(APIView):
    def get(self, request):
        """
        Types are an important part of our application, they are the core data of our app that NEEDs to be defined
        in order for this hole application to work. They usually end with Type in the class model name and in the database
        name.
        """
       
        charge_frequency_type = list(ChargeFrequencyType.objects.all().values())
        charge_type = list(ChargeType.objects.all().values())
        individual_charge_value_type = list(IndividualChargeValueType.objects.all().values())
        invoice_date_type = list(InvoiceDateType.objects.all().values())
        payment_method_type = list(PaymentMethodType.objects.all().values())
        conditional_type = list(ConditionalType.objects.all().values())
        field_date_format_type = list(FieldDateFormatType.objects.all().values())
        field_number_format_type = list(FieldNumberFormatType.objects.all().values())
        field_period_interval_type = list(FieldPeriodIntervalType.objects.all().values())
        field_type = list(FieldType.objects.all().values())
        section_type = list(SectionType.objects.all().values())
        data_type = list(VisualizationType.objects.all().values())
        company_type = list(CompanyType.objects.all().values())
        theme_type = list(ThemeType.objects.all().values())
        profile_type = list(ProfileType.objects.all().values())
        aggregation_type = list(AggregationType.objects.all().values())
        chart_type = list(ChartType.objects.all().values())
        alignment_type = list(TextAlignmentType.objects.all().values()) 
        block_type = list(TextBlockType.objects.all().values())

        return Response({
           'status': 'ok',
           'data': {
               'billing': {
                    'charge_frequency_type': charge_frequency_type,
                    'charge_type': charge_type,
                    'individual_charge_value_type': individual_charge_value_type,
                    'invoice_date_type': invoice_date_type,
                    'payment_method_type': payment_method_type
               },
               'data': {
                   'conditional_type': conditional_type,
                   'field_date_format_type': field_date_format_type,
                   'field_number_format_type': field_number_format_type,
                   'field_period_interval_type': field_period_interval_type,
                   'field_type': field_type,
                   'form_type': section_type
               },
               'rich_text': {
                   'alignment_type': alignment_type,
                   'block_type': block_type
               },
               'defaults': {
                   'chart_type': chart_type,
                   'aggregation_type': aggregation_type,
                   'profile_type': profile_type,
                   'company_type': company_type,
                   'data_type': data_type,
                   'theme_type': theme_type,
               }
           }
        }, status=status.HTTP_200_OK)
