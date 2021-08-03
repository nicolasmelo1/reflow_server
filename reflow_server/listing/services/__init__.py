from django.db import transaction

from reflow_server.core.events import Event
from reflow_server.formulary.models import Field, Form
from reflow_server.listing.models import ListingSelectedFields


class ListingService:
    def __init__(self, user_id, company_id, form_name):
        self.user_id = user_id
        self.company_id = company_id
        self.form_name = form_name
    
        self.__fields = Field.objects.filter(
            form__depends_on__group__company_id=company_id,
            form__depends_on__form_name=form_name,
        ).order_by('form__order','order')

    def __remove_listing_selected_fields(self, listing_selected_fields):
        """
        Removes a ListingSelectedFields object from a field that does not exist
        """
        selected_fields_not_in_fields = listing_selected_fields.exclude(
            field_id__in=self.__fields.values_list('id', flat=True)
        )
        for selected_field_not_in_fields in selected_fields_not_in_fields:
            ListingSelectedFields.objects.filter(user_id=self.user_id, field=selected_field_not_in_fields).delete()

    def __create_listing_selected_fields(self, listing_selected_fields):
        """
        Adds a new ListingSelectedFields object if a field is newly created
        """
        fields_not_in_selected_fields = self.__fields.exclude(
            id__in=listing_selected_fields.values_list('field_id', flat=True)
        )
        for field_not_in_selected_fields in fields_not_in_selected_fields:
            ListingSelectedFields.objects.create(user_id=self.user_id, field=field_not_in_selected_fields, is_selected=True)
            
    def __remove_duplicate_listing_selected_fields(self, listing_selected_fields):
        """
        Removes duplicate listing selected fields (let's not pretend the data is always perfect)
        """
        listing_selected_field_ids = list()
        for listing_selected_field in listing_selected_fields:
            if listing_selected_field.field_id in listing_selected_field_ids:
                listing_selected_field.delete()
            else:
                listing_selected_field_ids.append(listing_selected_field.field_id)
        

    @transaction.atomic
    def __update_listing_selected_fields(self, listing_selected_fields):
        # checks if the lenght of ListingSelectedFields and Fields are equal, if not we update the listingSelectedField
        # since we checked the model.CASCADE in the delete, when we delete the field the ListingSelectedField for that field
        # is also deleted.
        if listing_selected_fields.count() != self.__fields.count():
            self.__remove_duplicate_listing_selected_fields(listing_selected_fields)
            self.__remove_listing_selected_fields(listing_selected_fields)
            self.__create_listing_selected_fields(listing_selected_fields)
            return self.get_listing_selected_fields()
        return listing_selected_fields

    def get_listing_selected_fields(self, is_loading_the_listing_view=False):
        listing_selected_fields = ListingSelectedFields.objects.filter(
            user_id=self.user_id, 
            field__form__depends_on__form_name=self.form_name
        )

        listing_selected_fields = self.__update_listing_selected_fields(listing_selected_fields)

        # sends the event that the listing is being loaded to the user.
        if is_loading_the_listing_view:
            form_id = Form.listing_.form_id_by_company_id_and_form_name(self.company_id, self.form_name)
            Event.register_event('listing_loaded', {
                'user_id': self.user_id,
                'company_id': self.company_id,
                'form_id': form_id
            })
        return listing_selected_fields.order_by('field__form__order', 'field__order')
