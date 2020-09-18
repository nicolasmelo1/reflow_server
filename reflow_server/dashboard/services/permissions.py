from reflow_server.dashboard.models import DashboardChartConfiguration
from reflow_server.billing.models import CurrentCompanyCharge

class DashboardPermissionsService:
    @staticmethod
    def is_valid(company_id, form_name, dashboard_configuration_id):
        """
        Validates if the `dashboard_configuration_id` a user is trying to access exists for this company_id and this form_name.
        This way we prevent user trying to access charts of other companies and other people.

        Returns:
            bool: true if valid and false if invalid
        """
        return DashboardChartConfiguration.objects.filter(company_id=company_id, form__form_name=form_name, id=dashboard_configuration_id).exists()
    

    @staticmethod
    def is_valid_billing_charts(company_id, user_id, form_name, for_company=False, dashboard_configuration_id=None):
        """
        This method is used to check if the user already hit his maximum permission quantity for charts.
        
        Usually each chart is billed for a certain quantity for each page/formualary in the system. Some quantities are shared
        for the hole company and some are for each user.

        On this case, 'per_chart_company' are the quantity of charts ALL OF THE ADMINS OF A SINGLE company can create with
        the 'for_company' defined for each single formulary. The 'per_chart_user' are the quantity of charts a SINGLE USER
        of a company can create for himself for each single formulary.

        So we'll explain with an example:
        1 - Let's imagine the user `Charts Crazy Person` that is the ADMIN of the company `Charts Crazy Company`.
        2 - This user can create 2 and ONLY 2 'per_chart_company' and 1 and ONLY 1 'per_chart_user'
        3 - Now this user that is an admin will create a chart called `Proportion of charts people use` which is a Pie chart
        in the formulary called `Crazy Charts Form`. The chart in this example will have the `for_company` defined so all of
        the users in `Charts Crazy Company` can see this chart.
        4 - This user creates a new chart, this chart will be called `Charts sales revenue` and will be a line chart in the 
        formulary called `Crazy Charts Form`. Since this chart holds sensitive information he don't want the users of his company
        to be able to access this data. So it'll show just for him.
        5 - The user creates a new chart, this chart will be a bar type chart called `Chart Feature Request Votes` which will be
        a bar chart. He tries to create this to himself first (so with the 'for_company' option set to False). He will then recieve 
        an error.
        6 - He tries to save this chart with the 'for_company' defined and everything works as expected.

        WHY THIS HAPPENED?
        - This user can create 2 and ONLY 2 'per_chart_company' and 1 and ONLY 1 'per_chart_user'
        - On the item 3 the chart he created was with the `for_company` set to True, so it sums 1 in 'per_chart_company'
        - On the item 4 the chart he creates with the `for_company` set to false, sums 1 in 'per_chart_user'
        - On the item 5 he tries to create a new chart for 'per_chart_user' but he already have 1 and the limitation is 1
        so it throws an error.
        - On item 6 he sets the `for_company` to True, since the limit is 2 charts, he then can create a new chart.

        UNDERSTANDING HOW IT WORKS FOR MULTIPLE USERS
        Using the above example let's go with the following:
        1 - Let's imagine the user `Charts Crazy Person Assistant` that is the ADMIN of the company `Charts Crazy Company`.
        2 - The `Charts Crazy Person` already went through all of the steps in the example above so he have 2
        3 - After that, the user `Charts Crazy Person Assistant` creates a new chart in the formulary `Crazy Charts Form` called
        `Chart sales quantity`. This one will be just for him, so when he saves everything works fine.
        4 - Then this same user creates a new chart on the same formulary but for the hole company. When he does this he recieves
        an error.

        WHY?
        As i said earlier `per_chart_company` is shared inside of the company but 'per_chart_user' is a quantity for each user.

        It get's kinda confusing when we say that we bill each `per_chart_company` per the quantity of users. So if we bill $1,00
        for each `per_chart_company` the formula is simple: 1*quantity. BUT WE DON'T DO THAT, because each user individually
        consumes resources when they enter the page with charts. A company with 5 charts `for_company` and with 10 users will
        consume more resources than a company with 5 charts `for_company` and with 2 users(10 users will be consuming 5 charts 
        at the same time, so 10*5 = 50, where the second company is 2 users consuming 5 charts so 5*2=10). So we can't bill them equally.
        With the explanation above the formula becomes: 1 * quantity * quantity_of_users.
        
        Args:
            company_id (int): The id of the company you are working on
            user_id (int): For what user do you want to validate this
            form_name (str): For what formulary do you want to know if it reached the peak of the number of charts
            for_company (bool, optional): If you refer to reflow_server.dashboard.serializer.DashboardChartConfigurationSerializer
            you will see that the serializer actually recieves an object that can have the 'for_company' defined.
            You usually will intercept the request that contains this data so we can validate here if the user can add a new chart 
            or not. Defaults to False.
            dashboard_configuration_id (int, optional): When the user is editing a chart send the dashboard_configuration_id so
            we can validate. Defaults to None.

        Returns:
            bool: True if it is valid, and false if it is invalid.
        """
        charts_quantity_permission = CurrentCompanyCharge.objects.filter(company_id=company_id, user_id=user_id)
        charts_quantity_permission_for_company = charts_quantity_permission\
                                                .filter(individual_charge_value_type__name='per_chart_company')\
                                                .order_by('-quantity')\
                                                .values_list('quantity', flat=True).first()
        charts_quantity_permission_for_user = charts_quantity_permission\
                                    .filter(individual_charge_value_type__name='per_chart_user')\
                                    .order_by('-quantity')\
                                    .values_list('quantity', flat=True).first()

        current_charts_quantity_for_user = DashboardChartConfiguration.objects.filter(
            company_id=company_id, 
            form__form_name=form_name,
            user_id=user_id, 
            for_company=False
        ).exclude(id=dashboard_configuration_id).count()
        current_charts_quantity_for_company = DashboardChartConfiguration.objects.filter(
            company_id=company_id, 
            form__form_name=form_name,
            for_company=True
        ).exclude(id=dashboard_configuration_id).count()
        
        if not dashboard_configuration_id:
            if not for_company and current_charts_quantity_for_user + 1 > charts_quantity_permission_for_user:
                return False
            if for_company and current_charts_quantity_for_company + 1 > charts_quantity_permission_for_company:
                return False
        else:
            if not for_company and current_charts_quantity_for_user >= charts_quantity_permission_for_user:
                return False
            if for_company and current_charts_quantity_for_company >= charts_quantity_permission_for_company:
                return False
        return True