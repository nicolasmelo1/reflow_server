from django.db import transaction

from reflow_server.formulary.models import Field
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

    @transaction.atomic
    def __update_listing_selected_fields(self, listing_selected_fields):
        # checks if the lenght of ListingSelectedFields and Fields are equal, if not we update the listingSelectedField
        # since we checked the model.CASCADE in the delete, when we delete the field the ListingSelectedField for that field
        # is also deleted.
        if listing_selected_fields.count() != self.__fields.count():
            fields_not_in_selected_fields = self.__fields.exclude(
                id__in=listing_selected_fields.values_list('field_id', flat=True)
            )
            ListingSelectedFields.objects.bulk_create([
                ListingSelectedFields(user_id=self.user_id, field=field_not_in_selected_fields, is_selected=True) 
                for field_not_in_selected_fields in self.fields_not_in_selected_fields 
            ])
            return self.get_listing_selected_fields
        return listing_selected_fields

    @property
    def get_listing_selected_fields(self):
        listing_selected_fields = ListingSelectedFields.objects.filter(
            user_id=self.user_id, 
            field__form__depends_on__form_name=self.form_name
        )

        listing_selected_fields = self.__update_listing_selected_fields(listing_selected_fields)
        return listing_selected_fields
