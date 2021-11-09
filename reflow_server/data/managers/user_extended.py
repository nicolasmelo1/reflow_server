from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.contrib.auth.models import UserManager


class UserExtendedDataManager(UserManager):
    def users_active_by_company_id(self, company_id):
        """
        Gets the active users of a company. This gets a Queryset of
        UserExtended instances.

        Args:
            company_id (int): This is a Company instance id to filter the users

        Returns:
            django.db.models.QuerySet(reflow_server.authentication.models.UserExtended): 
            A queryset of active UserExtended instances.
        """
        return self.get_queryset().filter(company_id=company_id, is_active=True)

    def user_id_by_email_and_company_id(self, email, company_id):
        return self.get_queryset().filter(company_id=company_id, is_active=True, username=email).values_list('id', flat=True).first()


    def user_by_user_id(self, user_id):
        """
        Retrieves a user by its id.

        Args:
            user_id (int): An UserExtended instance id

        Returns:
            reflow_server.authentication.models.UserExtended: The found UserExtended instance.
        """
        return self.get_queryset().filter(id=user_id).first()

    def user_full_name_by_user_id(self, user_id):
        """
        Similar to `user_by_user_id` method but gets the full name of a user.

        Args:
            user_id (int): An UserExtended instance id

        Returns:
            str: Returns the full name of the user instance
        """
        instance = self.user_by_user_id(user_id)
        if instance:
            return instance.get_full_name()
        else:
            return ''

    def user_ids_for_search_by_search_dict_and_company_id(self, company_id, search_dict):
        """
        Here we filter the users from the `first_name` and `last_name` columns.
        We don't filter the users directly, since the value can be an ilike or not 
        we recieve a dict that we use as kwargs see here:
        https://docs.djangoproject.com/en/3.1/ref/models/querysets/#icontains

        So if you want to filter the user by the first name ilike you must 
        send the dict this way: 
        >>> {
            'first_name__icontains': <VALUE>
        }

        if you want to filter the first_name and last_name ilike your dict must be
        like the following:
        >>> {
            'first_name__icontains': <VALUE>,
            'last_name__icontains': <VALUE>
        }


        Args:
            company_id (int): This is a Company instance id to filter the users
            search_dict (dict): : This dict we will use as kwargs when we filter, 
            usualy this filter in the `first_name` or `last_name` column. We filter by two conditions
            it can be an ilike or not. So this dict should be like the following options:
            >>> {
                'first_name__icontains': <VALUE>
            }
            and:
            >>> {
                'first_name': <VALUE>
            }

            OR:
            >>> {
                'first_name__icontains': <VALUE>,
                'last_name__icontains': <VALUE>
            }
            and:
            >>> {
                'first_name': <VALUE>,
                'last_name': <VALUE>
            }

        Returns:
            django.db.models.QuerySet(int): Each integer is a UserExtended instance id.
        """
        return self.get_queryset().filter(
            company_id=company_id,
            **search_dict
        ).values_list('id', flat=True)

    def user_ids_for_sort_by_company_id(self, company_id, order_by_value):
        """
        Used for sorting the users, returns a Queryset of UserExtended instance ids
        sorted.

        Args:
            company_id (int): This is a Company instance id to filter the users
            order_by_value (enum('value', '-value')): This is the string to use in the order_by clause of the query. 
            https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
            It can be either `value` for ascending order or `-value` for descending order.

        Returns:
            django.db.models.QuerySet(int): Returns a SORTED queryset of user ids,
            each integer is a UserExtended instance id.
        """
        return self.get_queryset().filter(
            company_id=company_id, 
            is_active=True
        ) \
        .annotate(
            full_name=Concat('first_name', Value(' '), 'last_name', 
            output_field=CharField())
        ) \
        .order_by(order_by_value.replace('value', 'full_name')) \
        .values_list('id', flat=True)