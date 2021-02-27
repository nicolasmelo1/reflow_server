from reflow_server.kanban.managers import field_options
from django.db import transaction

from reflow_server.formulary.models import Field, FieldOptions, Form, OptionAccessedBy
from reflow_server.kanban.services.kanban_card import KanbanCardService
from reflow_server.kanban.models import KanbanCard, KanbanCardField, KanbanDefault, KanbanCollapsedOption


class KanbanValidationError(AttributeError):
    pass


class KanbanService(KanbanCardService):
    def __init__(self, user_id, company_id, form_name=None, form=None):
        """
        Handy class with lots of methods and functions for the kanban configuration and retrival.

        Args:
            user_id (int): The UserExtended instance id of the user who is editing or retrieving the kanban data.
            company_id (int): The Company instance id of the company where this user is making editions for
            form_name (str, optional): The name of the page/formulary the user is currently in. So we are loading the kanban
            for which formulary. Defaults to None.
            form (reflow_server.formulary.models.Form, optional): A form instance, used on some other use cases like
            for themes for example.. Defaults to None.
        """
        self.user_id = user_id
        self.company_id = company_id
        self.form = Form.objects.filter(
            depends_on__group__company_id=company_id,
            form_name=form_name, 
            depends_on__isnull=True
        ).first() if form_name != None else form

        print('BREAKPOINT')
        print(form_name)
        print(company_id)
        print(self.form)
        print(Form.objects.filter(
            depends_on__group__company_id=company_id,
            form_name=form_name, 
            depends_on__isnull=True
        ).first())
        print(Form.objects.filter(
            depends_on__group__company_id=company_id,
            form_name=form_name 
        ))
        print(Form.objects.filter(
            company_id=company_id,
            form_name=form_name 
        ))
        
        self.__fields = Field.objects.filter(
            form__depends_on__group__company_id=company_id,
            form__depends_on=self.form,
        ).order_by('order')

        print('BREAKPOINT')
        print(self.__fields)
    @staticmethod
    def copy_defaults_to_company_user(company_id, from_user_id, to_user_id):
        """
        When you are CREATING a new user you need to set the defaults of YOU (the user who is adding this new user)
        to the user you are creating. This method helps with that, so we copy all of the KanbanDefault data to this new user
        (this way when he opens the kanban for the first time, it'll show it already built for him).

        Since each KanbanCard is bounded to a user, we need to copy the KanbanCard also for this new user.

        Args:
            company_id (int): The Company instance  that is creating this new user
            from_user_id (int): The UserExtended instance id that is CREATING this new user, so we copy the data FROM this user
            to_user_id (int): The UserExtended instance id of the user that was created so we will add the new data TO this user.
        """
        kanban_defaults = KanbanDefault.objects.filter(
            user_id=from_user_id,
            company_id=company_id
        )
        for kanban_default in kanban_defaults:
            if kanban_default.kanban_card:
                default_kanban_card = KanbanCard.objects.create(
                    form=kanban_default.kanban_card.form,
                    company_id=company_id,
                    user_id=to_user_id
                )
                for kanban_card_fields_to_copy in KanbanCardField.objects.filter(kanban_card=kanban_default.kanban_card):
                    KanbanCardField.objects.create(
                        field=kanban_card_fields_to_copy.field,
                        kanban_card=default_kanban_card,
                        order=kanban_card_fields_to_copy.order
                    )
            else:
                default_kanban_card = kanban_default.kanban_card
            
            KanbanDefault.objects.create(
                form=kanban_default.form,
                company_id=company_id,
                user_id=to_user_id,
                kanban_card=default_kanban_card,
                kanban_dimension=kanban_default.kanban_dimension
            )

    def are_defaults_valid(self, kanban_card_id, kanban_dimension_id):
        """
        Check if the default values you are trying to set are valid before saving.

        Args:
            kanban_card_id (int): A KanbanCard instance id that will be used as default when the user tries to open the kanban again
            kanban_dimension_id (int): A Field instance id that we will use as the dimension for him. We only accept `option` field_types
            as dimension right now.

        Returns:
            bool: Returns True or False if the defaults are valid or not
        """

        if kanban_card_id != None and not self.get_kanban_cards.filter(id=kanban_card_id).exists() :
            self._was_defaults_validated = False
        if kanban_dimension_id != None and not self.get_possible_dimension_fields.filter(id=kanban_dimension_id).exists():
            self._was_defaults_validated = False
        self._was_defaults_validated =  True

        return self._was_defaults_validated

    @transaction.atomic
    def save_defaults(self, kanban_card_id, kanban_dimension_id):
        """
        This saves the default configurations so when the user opens the kanban again on a certain formulary 
        the data is loaded automatically for him.

        Args:
            kanban_card_id (int): A KanbanCard instance id that will be used as default when the user tries to open the kanban again
            kanban_dimension_id (int): A Field instance id that we will use as the dimension for him. We only accept `option` field_types
            as dimension right now.

        Returns:
            reflow_server.kanban.models.KanbanDefault: The KanbanDefault instance that was updated or created when he saved the defaults.
            The defaults are UNIQUE for a specific form, a specific user and a specific company_id.
        """
        if not hasattr(self, '_was_defaults_validated'):
            raise KanbanValidationError('You need to validate the defaults using `.are_defaults_valid()` method before saving.')
        instance = KanbanDefault.objects.update_or_create(
            form=self.form,
            user_id=self.user_id,
            company_id=self.company_id,
            defaults={
                'kanban_card_id': kanban_card_id,
                'kanban_dimension_id': kanban_dimension_id
            }
        )

        return instance

    @transaction.atomic
    def save_collapsed_dimension_phases(self, collapsed_field_option_ids):
        all_kanban_collapsed_option_instances = KanbanCollapsedOption.objects.filter(user_id=self.user_id, company_id=self.company_id, field_option__field__form__depends_on=self.form)
        all_kanban_collapsed_option_instances.exclude(field_option_id__in=collapsed_field_option_ids).delete()

        already_existing_field_option_ids = all_kanban_collapsed_option_instances.values_list('field_option_id', flat=True)
        new_field_option_ids = [collapsed_field_opion_id for collapsed_field_opion_id in collapsed_field_option_ids if collapsed_field_opion_id not in already_existing_field_option_ids]
        for new_field_option_id in new_field_option_ids:
            KanbanCollapsedOption.objects.create(
                user_id=self.user_id, 
                company_id=self.company_id,
                field_option_id=new_field_option_id
            )

        return True

    @property
    def get_fields(self):
        """
        Retrieves all of the fields the user can select when making filters in the kanban, it also retrieves all of the field options
        the user can select when building kanban cards

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.Field): A queryset of all of the fields of a single formulary
        """
        return self.__fields
    
    @property
    def get_possible_dimension_fields(self):
        """
        Retrieves all of the possible fields that the user can select as a dimension. Right now supports only `option` field types. Other types
        of fields are not supported for creating a kanban.

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.Field): A queryset of all of the fields of a single formulary that is of type `option`
        """
        return self.__fields.filter(type__type='option')

    def get_dimension_phases(self, dimension_id):
        """
        Retrieves all of the possible dimension phases, dimension phases is another name for field_options.
        We retrieve all of the FieldOptions respecting the ones that the user have access.

        Args:
            dimension_id (int): The field instance id the user had select as dimension so we can get the options of this field

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.FieldOptions): A queryset of the FieldOptions the user has access to.
        """
        field_option_ids = OptionAccessedBy.kanban_.field_options_by_user_id_and_field_id(self.user_id, dimension_id)
        return FieldOptions.kanban_.field_options_by_field_option_ids_and_company_id(field_option_ids, self.company_id)

    @property
    def get_kanban_cards(self):
        """
        Retrieves all of the KanbanCard instances of the user for this particular form and for a particular company.

        Returns:
            django.db.models.QuerySet(reflow_server.kanban.models.KanbanCard): Retrieves a queryset of all of the KanbanCard instances for this particular
            form.
        """
        # get kanban card ids of this form_name and this user
        kanban_card_ids = KanbanCardField.objects.filter(
            field__form__depends_on=self.form, 
            field__form__depends_on__group__company_id=self.company_id,
            kanban_card__user_id=self.user_id
        ).values_list('kanban_card', flat=True).distinct()
        return KanbanCard.objects.filter(id__in=kanban_card_ids)

    