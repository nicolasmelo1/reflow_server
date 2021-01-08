from rest_framework import serializers

from reflow_server.draft.services import DraftService


class DraftValueSerializer(serializers.Serializer):
    value = serializers.CharField()
    
    def save(self, company_id, user_id):
        draft_service = DraftService(company_id=company_id, user_id=user_id)
        return draft_service.save_new_draft(draft_value=self.validated_data.get('value', None))
